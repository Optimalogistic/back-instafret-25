from posixpath import splitext
import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import EmailValidator
import os
# Add these imports at the top of your models.py
from djmoney.models.fields import MoneyField
from decimal import Decimal


###### nouvelle users avec wallet ###

class users(models.Model):
    company=models.ForeignKey("companies", on_delete=models.CASCADE,null=True,blank=True)
    usertype=models.ForeignKey("usertypes",on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=255)
    gender=models.ForeignKey("genders",on_delete=models.CASCADE,null=True,blank=True)
    firstname=models.CharField(max_length=100,null=True,blank=True)
    lastname=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    birthdate=models.DateField(null=True,blank=True)
    address=models.CharField(max_length=255,null=True,blank=True)

    def unique_file_path_P(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('profiles/image', newname)

    image=models.FileField(upload_to=unique_file_path_P,max_length=255,null=True,blank=True)
    permissions=models.ForeignKey("permissions",on_delete=models.CASCADE,null=True,blank=True)
    status=models.ForeignKey("statuses",on_delete=models.CASCADE,null=True,blank=True)
    account_status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_exp_permi=models.DateField(null=True,blank=True)
    date_exp_inscri=models.DateField(null=True,blank=True)
    CIN=models.CharField(max_length=100,null=True,blank=True)

    def unique_file_path_Per(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('profiles/Permit', newname)

    image_permit=models.FileField(upload_to=unique_file_path_Per,max_length=255,null=True,blank=True)

    def unique_file_path_CIN(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('profiles/CIN', newname)

    image_CIN=models.FileField(upload_to=unique_file_path_CIN,max_length=255,null=True,blank=True)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('profiles/patent', newname)

    patent=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)
    country=models.ForeignKey("countries",on_delete=models.CASCADE,null=True,blank=True)
    mat=models.CharField(max_length=255,null=True,blank=True)
    lang=models.ForeignKey("languages",on_delete=models.CASCADE,null=False)
    bonus=models.IntegerField(null=True)
    referal_code=models.CharField(max_length=8,null=True,blank=True)
    referee_code=models.CharField(max_length=8,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.username)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # Votre logique existante pour nettoyer les champs vides
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        
        # Sauvegarder l'utilisateur d'abord
        super(users, self).save(*args, **kwargs)
        
        # Créer un wallet pour les nouveaux utilisateurs
        if is_new:
            self._create_wallet_for_new_user()

    def _create_wallet_for_new_user(self):
        """Crée un wallet pour un nouvel utilisateur"""
        try:
            from .services.wallet_service import EnhancedWalletService
            
            service = EnhancedWalletService()
            
            # Déterminer la devise basée sur le pays (ou USD par défaut)
            currency_code = self._get_user_currency_code()
            
            # Créer le wallet
            wallet = service.create_wallet(self, currency_code)
            
            if wallet:
                print(f"✓ Wallet créé pour {self.username} avec la devise {currency_code}")
            else:
                print(f"✗ Erreur lors de la création du wallet pour {self.username}")
                
        except Exception as e:
            print(f"Erreur lors de la création du wallet pour {self.username}: {e}")

    def _get_user_currency_code(self):
        """Détermine le code de devise pour l'utilisateur"""
        # Mapping simple pays -> devise (vous pouvez l'adapter)
        country_currency_mapping = {
            'Algeria': 'DZD',
            'United States': 'USD',
            'France': 'EUR',
            'Germany': 'EUR',
            'Spain': 'EUR',
            'Italy': 'EUR',
            'Tunisia': 'TND',
            'Senegal': 'CFA',
            'Libya': 'LYD',
            'Mali': 'CFA',
            'Morocco': 'MAD',
            'Egypt': 'EGP',
            'Mauritania': 'MRU'
            # Ajoutez d'autres mappings selon vos besoins
        }
        
        try:
            if self.country and self.country.label:
                return country_currency_mapping.get(self.country.label, 'USD')
            return 'USD'  # Devise par défaut
        except:
            return 'USD'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

##### fin users wallet ######

class usertypes(models.Model):
    label=models.CharField(max_length=50)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(usertypes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User type"
        verbose_name_plural = "User types"

class tokens(models.Model):
    user=models.ForeignKey("users", on_delete=models.CASCADE)

    def unique_rand():
        while True:
            token = str(uuid.uuid4())[0:32]
            if not tokens.objects.filter(token=token).exists():
                return token

    token=models.CharField(max_length=32,default=unique_rand)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.token)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(tokens, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

class permissions(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(permissions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

class genders(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(genders, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"

class statuses(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(statuses, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

class VAT(models.Model):
    value=models.IntegerField(null=False)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.value)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(VAT, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "VAT"
        verbose_name_plural = "VAT"

class companies(models.Model):
    type=models.ForeignKey("companytypes",on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    mat=models.CharField(max_length=255,null=True,blank=True)
    Gname=models.CharField(max_length=255,null=True,blank=True)
    phone=models.CharField(max_length=255,null=True,blank=True)
    email=models.CharField(max_length=255,null=True,blank=True)
    website=models.CharField(max_length=255,null=True,blank=True)
    country=models.ForeignKey("countries",on_delete=models.CASCADE,null=True,blank=True)
    city=models.ForeignKey("cities",on_delete=models.CASCADE,null=True,blank=True)
    postalcode=models.CharField(max_length=50,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    VAT=models.IntegerField(null=True,blank=True)

    def unique_file_path_logo(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('company/logo', newname)

    logo=models.FileField(upload_to=unique_file_path_logo,max_length=255,null=True,blank=True)

    def unique_file_path_banner(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('company/banner', newname)

    banner=models.FileField(upload_to=unique_file_path_banner,max_length=255,null=True,blank=True)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('company/patent', newname)

    patent=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def unique_file_path_RC(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('company/RC', newname)

    RC=models.FileField(upload_to=unique_file_path_RC,max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def unique_rand():
        while True:
            share_code = str(uuid.uuid4())[0:7]
            if not companies.objects.filter(share_code=share_code).exists():
                return share_code

    share_code=models.CharField(max_length=7,default=unique_rand)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.name)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(companies, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class companytypes(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/companytypes', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(companytypes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Company type"
        verbose_name_plural = "Company types"

class currencies(models.Model):
    label=models.CharField(max_length=6)
    code=models.CharField(max_length=1,null=True,blank=True)
    rate=models.FloatField()
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(currencies, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

class banner(models.Model):
    title=models.TextField()
    pos=models.TextField(null=True,blank=True)
    url=models.TextField()
    description=models.TextField(null=True,blank=True)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('banner', newname)

    image=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.title)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(banner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

class countries(models.Model):
    label=models.CharField(max_length=50)
    country_code=models.CharField(max_length=3)
    phone_code=models.CharField(max_length=5)
    flag=models.CharField(max_length=5)
    currency=models.ForeignKey("currencies",on_delete=models.CASCADE)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(countries, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class cities(models.Model):
    country=models.ForeignKey("countries",on_delete=models.CASCADE)
    label=models.CharField(max_length=255)
    active=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(cities, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class companyservices(models.Model):
    company=models.ForeignKey("companies",on_delete=models.CASCADE)
    service=models.ForeignKey("companyallservices",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.service)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(companyservices, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Company service"
        verbose_name_plural = "Company services"

class companyallservices(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/companyallservices', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(companyallservices, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "A company service"
        verbose_name_plural = "All company services"

class vehiclecategories(models.Model):
    label=models.CharField(max_length=50)
    percentage=models.IntegerField(null=False)
    upper=models.ForeignKey("vehiclecategories",on_delete=models.CASCADE,null=True,blank=True)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/vehiclecategories', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(vehiclecategories, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Vehicle category"
        verbose_name_plural = "Vehicle categories"

class vehicles(models.Model):
    company=models.ForeignKey("companies", on_delete=models.CASCADE)
    category=models.ForeignKey("vehiclecategories",on_delete=models.CASCADE)
    mat=models.CharField(max_length=50)
    mat2=models.CharField(max_length=50,null=True,blank=True)
    mark=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    length=models.IntegerField(null=True,blank=True)
    width=models.IntegerField(null=True,blank=True)
    height=models.IntegerField(null=True,blank=True)
    max_weight=models.IntegerField(null=True,blank=True)
    terrestrial_height=models.IntegerField(null=True,blank=True)
    year=models.IntegerField(null=True,blank=True)
    km_t=models.IntegerField(null=True,blank=True)
    max_speed=models.IntegerField(null=True,blank=True)
    date_exp_assur=models.DateField(null=True,blank=True)
    date_exp_inscri=models.DateField(null=True,blank=True)
    vehicle_status=models.BooleanField(default=True)

    def unique_file_path_image(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('vehicles/image', newname)

    image=models.FileField(upload_to=unique_file_path_image,max_length=255,null=True,blank=True)

    def unique_file_path_CG(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('vehicles/CG', newname)

    image_CG=models.FileField(upload_to=unique_file_path_CG,max_length=255,null=True,blank=True)

    def unique_file_path_CGP(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('vehicles/CGP', newname)

    image_CGP=models.FileField(upload_to=unique_file_path_CGP,max_length=255,null=True,blank=True)

    def unique_file_path_insurance(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('vehicles/insurance', newname)

    image_insurance=models.FileField(upload_to=unique_file_path_insurance,max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    co2_coef_req=models.FloatField(null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.mat)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(vehicles, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

class vehiclesoptions(models.Model):
    vehicle=models.ForeignKey("vehicles",on_delete=models.CASCADE,related_name='vehicle_options')
    option=models.ForeignKey("vehiclesalloptions",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.option)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(vehiclesoptions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Vehicle option"
        verbose_name_plural = "Vehicle options"

class vehiclesalloptions(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/vehiclesalloptions', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(vehiclesalloptions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "A vehicle option"
        verbose_name_plural = "All vehicle options"

class attributions(models.Model):
    company=models.ForeignKey("companies", on_delete=models.CASCADE,blank=True)
    user=models.ForeignKey("users", on_delete=models.CASCADE,related_name='attribution',blank=True)
    vehicle=models.ForeignKey("vehicles", on_delete=models.CASCADE,related_name='attribution',blank=True)
    request=models.ForeignKey("requests", on_delete=models.CASCADE,related_name='attribution',null=True,blank=True)
    mission=models.ForeignKey("missions", on_delete=models.CASCADE,related_name='attribution',null=True,blank=True)
    state=models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_rating=models.IntegerField(null=True,blank=True)
    user_rating=models.IntegerField(null=True,blank=True)
    vehicle_rating=models.IntegerField(null=True,blank=True)
    review=models.TextField(null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) "

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(attributions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Attribution"
        verbose_name_plural = "Attributions"

class palettype(models.Model):
    label=models.CharField(max_length=50)
    length=models.IntegerField(null=True,blank=True)
    width=models.IntegerField(null=True,blank=True)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/palettype', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(palettype, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Palet type"
        verbose_name_plural = "Palet types"

class merchnature(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/merchnature', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(merchnature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Merch nature"
        verbose_name_plural = "Merch natures"

class paymenttype(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/paymenttype', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(paymenttype, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Payment type"
        verbose_name_plural = "Payment types"

class requests(models.Model):
    user=models.ForeignKey("users", on_delete=models.CASCADE,null=False)
    category=models.ForeignKey("vehiclecategories",on_delete=models.CASCADE,null=False)
    Rref=models.CharField(max_length=50,null=False)
    count_type=models.IntegerField(null=False)
    count=models.IntegerField(null=True,blank=True)
    budget_type=models.IntegerField(null=False)
    budget=models.IntegerField(null=True,blank=True)
    charge_date=models.DateField(null=False)
    discharge_date=models.DateField(null=False)
    payment_type=models.ForeignKey("paymenttype",on_delete=models.CASCADE,null=False)
    state=models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company=models.ForeignKey("companies", on_delete=models.CASCADE,null=True,blank=True)
    report=models.TextField(null=True,blank=True)
    VAT=models.IntegerField(null=True,blank=True)
    P_invoice=models.ForeignKey("P_invoices", on_delete=models.CASCADE,null=True,blank=True)
    C_invoice=models.ForeignKey("C_invoices", on_delete=models.CASCADE,null=True,blank=True)
    qrcode_inv=models.CharField(max_length=255,null=True,blank=True)
    qrcode_track=models.CharField(max_length=255,null=True,blank=True)
    qrcode_ok=models.CharField(max_length=255,null=True,blank=True)
    validation_code=models.IntegerField(null=True,blank=True)
    backhaul_type=models.IntegerField(null=True,blank=True)
    co2_coef_req=models.FloatField(null=True,blank=True)
    co2_consom=models.CharField(max_length=255,null=True,blank=True)
    co2_tax=models.CharField(max_length=255,null=True,blank=True)
    currency_code=models.ForeignKey("currencies", on_delete=models.CASCADE,null=False)

    def __str__(self):
        return self.Rref+" #"+str(self.id)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(requests, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

class requestsoptions(models.Model):
    request=models.ForeignKey("requests",on_delete=models.CASCADE,related_name='request_options')
    option=models.ForeignKey("vehiclesalloptions",on_delete=models.CASCADE)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.option)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(requestsoptions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Request option"
        verbose_name_plural = "Request options"

class missions(models.Model):
    request=models.ForeignKey("requests",on_delete=models.CASCADE,related_name='request_missions')
    palette_type=models.ForeignKey("palettype",on_delete=models.CASCADE)
    merch_nature=models.ForeignKey("merchnature",on_delete=models.CASCADE)
    count=models.IntegerField(null=False)
    weight=models.IntegerField(null=False)
    width=models.IntegerField(null=False)
    length=models.IntegerField(null=False)
    height=models.IntegerField(null=False)
    ref=models.CharField(max_length=255,null=True,blank=True)
    requester=models.CharField(max_length=255,null=True,blank=True)
    vendor=models.CharField(max_length=255,null=True,blank=True)
    PO=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    dep_address=models.ForeignKey("usersaddresses",on_delete=models.CASCADE,null=False,related_name='mission_dep_address')
    arr_address=models.ForeignKey("usersaddresses",on_delete=models.CASCADE,null=False,related_name='mission_arr_address')
    dep_address_start=models.DateTimeField(null=False)
    dep_address_end=models.DateTimeField(null=False)
    arr_address_start=models.DateTimeField(null=False)
    arr_address_end=models.DateTimeField(null=False)
    CRval=models.IntegerField(null=False)
    insuranceval=models.IntegerField(null=False)
    RPval=models.IntegerField(null=False)
    CR_status=models.BooleanField(null=False)
    RP_status=models.BooleanField(null=False)
    CR=models.IntegerField(null=True,blank=True)
    insurance=models.IntegerField(null=True,blank=True)
    RP=models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state=models.IntegerField(null=False)
    charge_S=models.DateTimeField(null=True,blank=True)
    charge_E=models.DateTimeField(null=True,blank=True)
    trip_S=models.DateTimeField(null=True,blank=True)
    trip_E=models.DateTimeField(null=True,blank=True)
    discharge_S=models.DateTimeField(null=True,blank=True)
    discharge_E=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) +" )"

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(missions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mission"
        verbose_name_plural = "Missions"

class missionsoptions(models.Model):
    mission=models.ForeignKey("missions",on_delete=models.CASCADE,related_name='mission_options')
    option=models.ForeignKey("missionsalloptions",on_delete=models.CASCADE)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.option)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(missionsoptions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mission option"
        verbose_name_plural = "Mission options"

class missionsalloptions(models.Model):
    label=models.CharField(max_length=50)
    active=models.BooleanField(default=False)

    def unique_file_path_patent(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('icons/missionsalloptions', newname)

    icon=models.FileField(upload_to=unique_file_path_patent,max_length=255,null=True,blank=True)
    id_cat_parent=models.ForeignKey("vehiclecategories",on_delete=models.CASCADE)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.label)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(missionsalloptions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "A mission option"
        verbose_name_plural = "All mission options"

class usersaddresses(models.Model):
    user=models.ForeignKey("users", on_delete=models.CASCADE,null=False)
    label=models.TextField(null=False)
    Lat=models.CharField(max_length=25,null=False)
    Lng=models.CharField(max_length=25,null=False)
    active=models.IntegerField(null=False)
    enterprise=models.CharField(max_length=255,null=False)
    Rname=models.CharField(max_length=25,null=False)
    tel=models.CharField(max_length=25,null=False)
    tel1=models.CharField(max_length=25,null=True,blank=True)
    tel2=models.CharField(max_length=25,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.enterprise)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(usersaddresses, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User addresse"
        verbose_name_plural = "User addresses"

class requestoffers(models.Model):
    request=models.ForeignKey("requests",on_delete=models.CASCADE,related_name='request_offers')
    company=models.ForeignKey("companies", on_delete=models.CASCADE)
    value=models.IntegerField(null=False)
    active=models.IntegerField(null=False)
    options=models.CharField(max_length=255,null=True,blank=True)
    charge_date=models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.company) +":" +str(self.value)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(requestoffers, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Request offer"
        verbose_name_plural = "Request offers"

class missions_tracker(models.Model):
    mission=models.ForeignKey("missions",on_delete=models.CASCADE,related_name='mission_tracker')
    Lat=models.CharField(max_length=25,null=False)
    Lng=models.CharField(max_length=25,null=False)
    Accuracy=models.CharField(max_length=25,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.Lat) +"/" +str(self.Lng)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(missions_tracker, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Missions tracker"
        verbose_name_plural = "Missions trackers"

class mission_files(models.Model):
    mission=models.ForeignKey("missions",on_delete=models.CASCADE,related_name='mission_files')

    def unique_file_path_P(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('mission/files', newname)

    file=models.FileField(upload_to=unique_file_path_P,max_length=255,null=False)

    def __str__(self):
        return "( "+str(self.id) + " ) "

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(mission_files, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mission file"
        verbose_name_plural = "Mission files"

class language_pack(models.Model):
    code=models.ForeignKey("languages",on_delete=models.CASCADE,null=False)
    ref=models.CharField(max_length=100)
    value=models.TextField()

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.ref)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(language_pack, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Language pack"
        verbose_name_plural = "Language packs"

class languages(models.Model):
    code=models.CharField(max_length=20)
    active=models.BooleanField(default=False)
    default=models.BooleanField(default=False)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.code)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(languages, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

class P_invoices(models.Model):
    payment_status=models.BooleanField(default=False,null=False)
    stamp=models.IntegerField(null=False)
    payment_type=models.ForeignKey("paymenttype",on_delete=models.CASCADE,null=False)
    O_name=models.TextField(null=False)
    O_address=models.TextField(null=False)
    O_phone=models.TextField(null=False)
    O_mat=models.TextField(null=False)
    C_name=models.TextField(null=False)
    C_address=models.TextField(null=False)
    C_phone=models.TextField(null=False)
    C_mat=models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.payment_status)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(P_invoices, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Provider invoice"
        verbose_name_plural = "Provider invoices"

class C_invoices(models.Model):
    payment_status=models.BooleanField(default=False,null=False)
    stamp=models.IntegerField(null=False)
    payment_type=models.ForeignKey("paymenttype",on_delete=models.CASCADE,null=False)
    O_name=models.TextField(null=False)
    O_address=models.TextField(null=False)
    O_phone=models.TextField(null=False)
    O_mat=models.TextField(null=False)
    C_name=models.TextField(null=False)
    C_address=models.TextField(null=False)
    C_phone=models.TextField(null=False)
    C_mat=models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.payment_status)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(C_invoices, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Client invoice"
        verbose_name_plural = "Client invoices"

class settings(models.Model):
    code=models.CharField(max_length=100)
    value=models.TextField(null=True,blank=True)

    def unique_file_path_P(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('settings', newname)

    file=models.FileField(upload_to=unique_file_path_P,max_length=255,null=True,blank=True)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.code)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(settings, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

class requestcodes(models.Model):
    request=models.ForeignKey("requests",on_delete=models.CASCADE,related_name='request_codes')
    code=models.CharField(max_length=7)

    def __str__(self):
        return "( "+str(self.id) + " ) " + str(self.request)

    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(requestcodes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Request code"
        verbose_name_plural = "Request codes"

# ============================================
# NEW SHIPMENT TRACKING SYSTEM MODELS
# ============================================

class carriers(models.Model):
    """Shipping carriers like MSC, CGM, MAERSK, etc."""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    
    # Logo field added
    def unique_file_path_carrier_logo(instance, filename):
        instance.original_file_name = filename
        base, ext = splitext(filename)
        newname = "%s%s" % (uuid.uuid4(), ext)
        return os.path.join('carriers/logos', newname)
    
    logo = models.FileField(upload_to=unique_file_path_carrier_logo, max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"({self.id}) {self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(carriers, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Carrier"
        verbose_name_plural = "Carriers"

class shipment_tags(models.Model):
    """Tags for organizing shipments - linked to broker user"""
    broker_user = models.ForeignKey("users", on_delete=models.CASCADE, related_name='broker_shipment_tags')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"({self.id}) {self.name}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(shipment_tags, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Shipment Tag"
        verbose_name_plural = "Shipment Tags"
        unique_together = ['broker_user', 'name']

class shipments(models.Model):
    """Enhanced shipment tracking system - Independent"""
    TRACKING_TYPE_CHOICES = [
        ('MBL', 'MBL/Booking Number'),
        ('CONTAINER', 'Container Number'),
        ('VEHICLE', 'Vehicle Number'),
    ]
    
    # Updated STATUS_CHOICES with Delayed and Canceled
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('BOOKED', 'Booked'),
        ('GATE_IN', 'Gate In'),
        ('LOADED', 'Loaded'),
        ('DEPARTED', 'Departed'),
        ('IN_TRANSIT', 'In Transit'),
        ('ARRIVED', 'Arrived'),
        ('DISCHARGED', 'Discharged'),
        ('GATE_OUT', 'Gate Out'),
        ('DELIVERED', 'Delivered'),
        ('DELAYED', 'Delayed'),      # New status added
        ('CANCELED', 'Canceled'),    # New status added
        ('EXCEPTION', 'Exception'),
    ]
    
    # Link only to users model (broker)
    broker_user = models.ForeignKey("users", on_delete=models.CASCADE, related_name='broker_shipments')
    carrier = models.ForeignKey("carriers", on_delete=models.CASCADE)
    
    # Tracking information with vehicle option
    tracking_type = models.CharField(max_length=20, choices=TRACKING_TYPE_CHOICES)
    mbl_booking_number = models.CharField(max_length=100, blank=True, null=True)
    container_number = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Classification
    internal_reference = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("shipment_tags", blank=True, related_name='tagged_shipments')
    
    # Shipment details
    origin_port = models.CharField(max_length=255, blank=True)
    destination_port = models.CharField(max_length=255, blank=True)
    vessel_name = models.CharField(max_length=255, blank=True)
    voyage_number = models.CharField(max_length=100, blank=True)
    etd = models.DateField(null=True, blank=True)  # Estimated Time of Departure
    eta = models.DateField(null=True, blank=True)  # Estimated Time of Arrival
    
    # Customer information (independent from companies model)
    customer_name = models.CharField(max_length=255, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    customer_address = models.TextField(blank=True)
    
    # Status
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    last_updated = models.DateTimeField(auto_now=True)
    
    # Additional fields for delayed/canceled shipments
    delay_reason = models.TextField(blank=True, null=True)  # Reason for delay
    cancellation_reason = models.TextField(blank=True, null=True)  # Reason for cancellation
    new_eta = models.DateField(null=True, blank=True)  # New ETA for delayed shipments
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def tracking_number(self):
        if self.tracking_type == 'MBL':
            return self.mbl_booking_number
        elif self.tracking_type == 'CONTAINER':
            return self.container_number
        elif self.tracking_type == 'VEHICLE':
            return self.vehicle_number
        return None
    
    def __str__(self):
        tracking_info = self.tracking_number or "No tracking number"
        return f"({self.id}) {self.carrier.code} - {tracking_info}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(shipments, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

class shipment_followers(models.Model):
    """Email followers for shipment notifications"""
    shipment = models.ForeignKey("shipments", on_delete=models.CASCADE, related_name='followers')
    email = models.EmailField(validators=[EmailValidator()])
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"({self.id}) {self.shipment} - {self.email}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(shipment_followers, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Shipment Follower"
        verbose_name_plural = "Shipment Followers"
        unique_together = ['shipment', 'email']

class shipment_status_updates(models.Model):
    """Detailed status updates for shipments"""
    shipment = models.ForeignKey("shipments", on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True)
    vessel_name = models.CharField(max_length=255, blank=True)
    voyage_number = models.CharField(max_length=100, blank=True)
    estimated_date = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, default='SYSTEM')
    
    def __str__(self):
        return f"({self.id}) {self.shipment} - {self.status}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(shipment_status_updates, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Shipment Status Update"
        verbose_name_plural = "Shipment Status Updates"
        ordering = ['-timestamp']

class notification_logs(models.Model):
    """Log all notification attempts"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('BOUNCED', 'Bounced'),
    ]
    
    shipment = models.ForeignKey("shipments", on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    notification_type = models.CharField(max_length=20, default='EMAIL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"({self.id}) {self.shipment} - {self.recipient_email} - {self.status}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(notification_logs, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
        ordering = ['-created_at']

class broker_profiles(models.Model):
    """Extended broker profile information"""
    user = models.OneToOneField(
        "users", 
        on_delete=models.CASCADE, 
        related_name='broker_profile'
    )
    company_name = models.CharField(max_length=255, blank=True)
    brand_color = models.CharField(max_length=7, default='#007bff')
    website = models.URLField(blank=True)
    business_address = models.TextField(blank=True)
    tax_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"({self.id}) {self.user.username} - {self.company_name}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(broker_profiles, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Broker Profile"
        verbose_name_plural = "Broker Profiles"

# Update the wallet models in your models.py

class supported_currencies(models.Model):
    """Supported currencies in the system"""
    code = models.CharField(max_length=3, unique=True)  # USD, EUR, TND, DZD
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    exchange_rate_to_usd = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"({self.id}) {self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(supported_currencies, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Supported Currency"
        verbose_name_plural = "Supported Currencies"

class user_wallets(models.Model):
    """Enhanced multi-currency user wallet"""
    user = models.OneToOneField("users", on_delete=models.CASCADE, related_name='wallet')
    
    def unique_wallet_id():
        return str(uuid.uuid4()).replace('-', '')[:16]
    
    wallet_id = models.CharField(max_length=16, unique=True, default=unique_wallet_id)
    
    # Main currency selected by user
    main_currency = models.ForeignKey("supported_currencies", on_delete=models.CASCADE, related_name='main_wallets')
    
    # Points balance (virtual currency)
    points_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Conversion rate: 1 USD = 3 Points (adjustable per currency)
    POINTS_PER_USD = Decimal('3.00')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_frozen = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_balance_in_currency(self, currency_code):
        """Get balance in specific currency"""
        try:
            currency_wallet = self.currency_balances.get(currency__code=currency_code)
            return currency_wallet.balance
        except wallet_currency_balances.DoesNotExist:
            return Decimal('0.00')
    
    def get_total_balance_in_main_currency(self):
        """Get total balance converted to main currency"""
        total = Decimal('0.00')
        for currency_balance in self.currency_balances.all():
            if currency_balance.currency.code == self.main_currency.code:
                total += currency_balance.balance
            else:
                # Convert to main currency
                converted_amount = currency_balance.balance * currency_balance.currency.exchange_rate_to_usd
                if self.main_currency.code != 'USD':
                    converted_amount = converted_amount / self.main_currency.exchange_rate_to_usd
                total += converted_amount
        return total
    
    def add_credits(self, amount, currency_code):
        """Add credits to wallet in specific currency"""
        currency = supported_currencies.objects.get(code=currency_code)
        currency_wallet, created = wallet_currency_balances.objects.get_or_create(
            wallet=self,
            currency=currency,
            defaults={'balance': 0}
        )
        currency_wallet.balance += amount
        currency_wallet.save()
        return currency_wallet.balance
    
    def deduct_credits(self, amount, currency_code):
        """Deduct credits from wallet in specific currency"""
        try:
            currency_wallet = self.currency_balances.get(currency__code=currency_code)
            if currency_wallet.balance >= amount:
                currency_wallet.balance -= amount
                currency_wallet.save()
                return True
            return False
        except wallet_currency_balances.DoesNotExist:
            return False
    
    def convert_credits_to_points(self, credit_amount, currency_code):
        """Convert credits to points"""
        if self.deduct_credits(credit_amount, currency_code):
            currency = supported_currencies.objects.get(code=currency_code)
            # Convert to USD first, then to points
            usd_amount = credit_amount * currency.exchange_rate_to_usd
            points_to_add = usd_amount * self.POINTS_PER_USD
            self.points_balance += points_to_add
            self.save()
            return points_to_add
        return None
    
    def __str__(self):
        return f"({self.id}) {self.user.username} - Main: {self.main_currency.code} | {self.points_balance} pts"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(user_wallets, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "User Wallet"
        verbose_name_plural = "User Wallets"

class wallet_currency_balances(models.Model):
    """Individual currency balances for each wallet"""
    wallet = models.ForeignKey("user_wallets", on_delete=models.CASCADE, related_name='currency_balances')
    currency = models.ForeignKey("supported_currencies", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"({self.id}) {self.wallet.user.username} - {self.balance} {self.currency.code}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(wallet_currency_balances, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Wallet Currency Balance"
        verbose_name_plural = "Wallet Currency Balances"
        unique_together = ['wallet', 'currency']

class wallet_transactions(models.Model):
    """Enhanced wallet transaction history"""
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('CONVERSION', 'Currency Conversion'),
        ('POINTS_CONVERSION', 'Credit to Points Conversion'),
        ('PAYMENT', 'Payment'),
        ('REFUND', 'Refund'),
        ('BONUS', 'Bonus'),
        ('ADMIN_CREDIT', 'Admin Credit'),
        ('ADMIN_DEBIT', 'Admin Debit'),
        ('COUPON', 'Coupon Credit'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    wallet = models.ForeignKey("user_wallets", on_delete=models.CASCADE, related_name='transactions')
    currency = models.ForeignKey("supported_currencies", on_delete=models.CASCADE, null=True, blank=True)
    
    # Transaction details
    transaction_id = models.CharField(max_length=32, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Amounts
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Points transaction (if applicable)
    points_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    points_balance_before = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    points_balance_after = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(blank=True)
    reference_id = models.CharField(max_length=255, blank=True)
    admin_user = models.ForeignKey("users", on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_transactions')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4()).replace('-', '')[:32]
        
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(wallet_transactions, self).save(*args, **kwargs)
    
    def __str__(self):
        currency_info = f"{self.currency.code}" if self.currency else "POINTS"
        return f"({self.id}) {self.wallet.user.username} - {self.transaction_type} - {self.amount} {currency_info}"
    
    class Meta:
        verbose_name = "Wallet Transaction"
        verbose_name_plural = "Wallet Transactions"
        ordering = ['-created_at']

class wallet_coupons(models.Model):
    """Coupon system like ShipsGo"""
    COUPON_TYPES = [
        ('PERCENTAGE', 'Percentage Discount'),
        ('FIXED_AMOUNT', 'Fixed Amount'),
        ('BONUS_CREDITS', 'Bonus Credits'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES)
    
    # Discount/Bonus values
    percentage_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # For percentage
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For fixed amount
    currency = models.ForeignKey("supported_currencies", on_delete=models.CASCADE, null=True, blank=True)
    
    # Usage limits
    max_uses = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    max_uses_per_user = models.IntegerField(default=1)
    
    # Conditions
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users", on_delete=models.CASCADE, related_name='created_coupons')
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_until and 
                self.used_count < self.max_uses)
    
    def calculate_discount(self, amount):
        if self.coupon_type == 'PERCENTAGE':
            discount = amount * (self.percentage_value / 100)
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
            return discount
        elif self.coupon_type == 'FIXED_AMOUNT':
            return min(self.fixed_amount, amount)
        elif self.coupon_type == 'BONUS_CREDITS':
            return self.fixed_amount
        return 0
    
    def __str__(self):
        return f"({self.id}) {self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(wallet_coupons, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Wallet Coupon"
        verbose_name_plural = "Wallet Coupons"

class wallet_coupon_usage(models.Model):
    """Track coupon usage by users"""
    coupon = models.ForeignKey("wallet_coupons", on_delete=models.CASCADE, related_name='usage_records')
    user = models.ForeignKey("users", on_delete=models.CASCADE)
    wallet_transaction = models.ForeignKey("wallet_transactions", on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"({self.id}) {self.user.username} used {self.coupon.code}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(wallet_coupon_usage, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Coupon Usage"
        verbose_name_plural = "Coupon Usage Records"
        unique_together = ['coupon', 'user']

# Keep your existing payment_methods and wallet_top_ups models but update them for multi-currency

class payment_methods(models.Model):
    """User payment methods (credit cards) - Updated"""
    CARD_TYPES = [
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
        ('AMEX', 'American Express'),
        ('DISCOVER', 'Discover'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey("users", on_delete=models.CASCADE, related_name='payment_methods')
    
    # Card details (encrypted/tokenized)
    stripe_payment_method_id = models.CharField(max_length=255)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    last_four_digits = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    
    # Currency support
    supported_currency = models.ForeignKey("supported_currencies", on_delete=models.CASCADE, default=1)
    
    # Metadata
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"({self.id}) {self.user.username} - {self.card_type} ****{self.last_four_digits}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            payment_methods.objects.filter(user=self.user, is_default=True).update(is_default=False)
        
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(payment_methods, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
        
class wallet_top_ups(models.Model):
    """Wallet top-up transactions via credit card"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    wallet = models.ForeignKey("user_wallets", on_delete=models.CASCADE, related_name='top_ups')
    payment_method = models.ForeignKey("payment_methods", on_delete=models.CASCADE)
    
    # Transaction details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    points_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Payment processing
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    failure_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"({self.id}) {self.wallet.user.username} - {self.amount} - {self.status}"
    
    def save(self, *args, **kwargs):
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(wallet_top_ups, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Wallet Top-up"
        verbose_name_plural = "Wallet Top-ups"
        ordering = ['-created_at']
