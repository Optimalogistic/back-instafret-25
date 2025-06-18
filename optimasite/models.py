from posixpath import splitext
import uuid
from django.db import models
from django.template.defaultfilters import slugify
import os

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
        for var in vars(self):
            if not var.startswith('_'):
                if self.__dict__[var] == '':
                    self.__dict__[var] = None
        super(users, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

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
            token = token = str(uuid.uuid4())[0:32]
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
            share_code = share_code = str(uuid.uuid4())[0:7]
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