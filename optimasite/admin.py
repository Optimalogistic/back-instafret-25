from django import forms
from django.contrib import admin
from optimasite import models
from django.core.validators import EmailValidator
from decimal import Decimal

# Admin site customization
admin.site.site_header = "Optima Freight Management"
admin.site.site_title = "Optima Admin"
admin.site.index_title = "Welcome to Optima Administration"

###################################################################################
# PROVIDER THEME - Companies and Services
###################################################################################

class companies(admin.ModelAdmin):
    model = models.companies
    list_display = ["id","name","mat","Gname","phone","website","city","country","type"]
    list_filter = ["city","country","type"]
    search_fields = ["name", "mat", "Gname", "phone"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "mat", "Gname", "type")
        }),
        ("Contact Information", {
            "fields": ("phone", "email", "website")
        }),
        ("Location", {
            "fields": ("country", "city", "postalcode", "address")
        }),
        ("Business Details", {
            "fields": ("description", "VAT", "logo", "banner", "patent", "RC")
        }),
    )

admin.site.register(models.companies, companies)

class companytypes(admin.ModelAdmin):
    model = models.companytypes
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.companytypes, companytypes)

class companyallservices(admin.ModelAdmin):
    model = models.companyallservices
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.companyallservices, companyallservices)

class companyservices(admin.ModelAdmin):
    model = models.companyservices
    list_display = ["id","company","service"]
    search_fields = ["company__name"]
    list_filter = ["service"]

admin.site.register(models.companyservices, companyservices)

###################################################################################
# CLIENTS THEME - Users and Related
###################################################################################

class users(admin.ModelAdmin):
    model = models.users
    list_display = ["username","CIN","firstname","lastname","usertype","permissions","status","account_status","get_wallet_status"]
    list_filter = ["usertype","permissions","account_status","status"]
    search_fields = ["username", "firstname", "lastname", "email", "phone"]
    actions = ['create_wallet_action']
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("username", "password", "usertype", "company")
        }),
        ("Personal Details", {
            "fields": ("firstname", "lastname", "gender", "birthdate", "CIN")
        }),
        ("Contact Information", {
            "fields": ("email", "phone", "address", "country")
        }),
        ("Documents", {
            "fields": ("image", "image_permit", "image_CIN", "patent")
        }),
        ("Permissions & Status", {
            "fields": ("permissions", "status", "account_status", "date_exp_permi", "date_exp_inscri")
        }),
        ("Settings", {
            "fields": ("lang", "bonus", "referal_code", "referee_code", "mat")
        }),
    )
    
    def get_wallet_status(self, obj):
        try:
            wallet = obj.wallet
            return f"✓ {wallet.main_currency.code}"
        except:
            return "✗ No Wallet"
    get_wallet_status.short_description = "Wallet Status"
    
    def create_wallet_action(self, request, queryset):
        """Action admin pour créer des wallets pour les utilisateurs sélectionnés"""
        from .services.wallet_service import EnhancedWalletService
        
        service = EnhancedWalletService()
        created_count = 0
        
        for user in queryset:
            try:
                if not hasattr(user, 'wallet'):
                    currency_code = user._get_user_currency_code()
                    wallet = service.create_wallet(user, currency_code)
                    if wallet:
                        created_count += 1
            except Exception as e:
                self.message_user(request, f"Erreur pour {user.username}: {e}", level='ERROR')
        
        self.message_user(request, f"{created_count} wallets créés avec succès")
    
    create_wallet_action.short_description = "Créer des wallets pour les utilisateurs sélectionnés"

admin.site.register(models.users, users)

class usertypes(admin.ModelAdmin):
    model = models.usertypes
    list_display = ["id","label"]
    search_fields = ["label"]

admin.site.register(models.usertypes, usertypes)

class usersaddresses(admin.ModelAdmin):
    model = models.usersaddresses
    list_display = ["id","user","enterprise","label","active"]
    search_fields = ["user__username", "enterprise", "label"]
    list_filter = ["active"]

admin.site.register(models.usersaddresses, usersaddresses)

class tokens(admin.ModelAdmin):
    model = models.tokens
    list_display = ["id","user","token","created_at"]
    search_fields = ["user__username", "token"]
    readonly_fields = ["created_at", "updated_at"]

admin.site.register(models.tokens, tokens)

###################################################################################
# WALLET SYSTEM - Enhanced Wallet Administration
###################################################################################

@admin.register(models.supported_currencies)
class supported_currencies(admin.ModelAdmin):
    list_display = ["id", "code", "name", "symbol", "exchange_rate_to_usd", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["code", "name", "symbol"]
    list_editable = ["exchange_rate_to_usd", "is_active"]
    readonly_fields = ["created_at", "updated_at"]

@admin.register(models.user_wallets)
class user_wallets(admin.ModelAdmin):
    list_display = ["wallet_id", "get_user_info", "main_currency", "points_balance", "is_active", "is_frozen", "created_at"]
    list_filter = ["main_currency", "is_active", "is_frozen", "created_at"]
    search_fields = ["wallet_id", "user__username", "user__email", "user__firstname", "user__lastname"]
    readonly_fields = ["wallet_id", "created_at", "updated_at"]
    actions = ['credit_wallet_usd_10', 'credit_wallet_eur_10', 'freeze_wallets', 'unfreeze_wallets']
    
    def get_user_info(self, obj):
        return f"{obj.user.username} ({obj.user.firstname} {obj.user.lastname})"
    get_user_info.short_description = "User"
    
    def credit_wallet_usd_10(self, request, queryset):
        from .services.wallet_service import EnhancedWalletService
        service = EnhancedWalletService()
        
        for wallet in queryset:
            try:
                result = service.admin_credit_wallet(
                    user=wallet.user,
                    amount=Decimal('10.00'),
                    currency_code='USD',
                    admin_user=request.user,
                    description="Admin credit: $10 USD"
                )
                if result['success']:
                    self.message_user(request, f"✓ {wallet.user.username}: +$10 USD")
            except Exception as e:
                self.message_user(request, f"✗ Error for {wallet.user.username}: {e}", level='ERROR')
    
    credit_wallet_usd_10.short_description = "Credit $10 USD to selected wallets"
    
    def credit_wallet_eur_10(self, request, queryset):
        from .services.wallet_service import EnhancedWalletService
        service = EnhancedWalletService()
        
        for wallet in queryset:
            try:
                result = service.admin_credit_wallet(
                    user=wallet.user,
                    amount=Decimal('10.00'),
                    currency_code='EUR',
                    admin_user=request.user,
                    description="Admin credit: €10 EUR"
                )
                if result['success']:
                    self.message_user(request, f"✓ {wallet.user.username}: +€10 EUR")
            except Exception as e:
                self.message_user(request, f"✗ Error for {wallet.user.username}: {e}", level='ERROR')
    
    credit_wallet_eur_10.short_description = "Credit €10 EUR to selected wallets"
    
    def freeze_wallets(self, request, queryset):
        updated = queryset.update(is_frozen=True)
        self.message_user(request, f"{updated} wallets frozen")
    
    freeze_wallets.short_description = "Freeze selected wallets"
    
    def unfreeze_wallets(self, request, queryset):
        updated = queryset.update(is_frozen=False)
        self.message_user(request, f"{updated} wallets unfrozen")
    
    unfreeze_wallets.short_description = "Unfreeze selected wallets"

@admin.register(models.wallet_currency_balances)
class wallet_currency_balances(admin.ModelAdmin):
    list_display = ["get_user", "get_wallet_id", "currency", "balance", "updated_at"]
    list_filter = ["currency", "updated_at"]
    search_fields = ["wallet__user__username", "wallet__wallet_id", "currency__code"]
    readonly_fields = ["updated_at"]
    
    def get_user(self, obj):
        return obj.wallet.user.username
    get_user.short_description = "User"
    
    def get_wallet_id(self, obj):
        return obj.wallet.wallet_id
    get_wallet_id.short_description = "Wallet ID"

@admin.register(models.wallet_transactions)
class wallet_transactions(admin.ModelAdmin):
    list_display = ["transaction_id", "get_user", "transaction_type", "amount", "currency", "status", "created_at"]
    list_filter = ["transaction_type", "currency", "status", "created_at"]
    search_fields = ["transaction_id", "wallet__user__username", "description", "reference_id"]
    readonly_fields = ["transaction_id", "created_at", "updated_at"]
    
    def get_user(self, obj):
        return obj.wallet.user.username
    get_user.short_description = "User"

@admin.register(models.wallet_coupons)
class wallet_coupons(admin.ModelAdmin):
    list_display = ["code", "name", "coupon_type", "is_active", "valid_from", "valid_until", "used_count", "max_uses"]
    list_filter = ["coupon_type", "is_active", "currency"]
    search_fields = ["code", "name", "description"]
    readonly_fields = ["used_count", "created_at"]  # Supprimé 'updated_at' car il n'existe pas
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("code", "name", "description", "coupon_type")
        }),
        ("Discount/Bonus Settings", {
            "fields": ("percentage_value", "fixed_amount", "currency", "minimum_amount", "maximum_discount")
        }),
        ("Usage Limits", {
            "fields": ("max_uses", "max_uses_per_user")
        }),
        ("Validity", {
            "fields": ("is_active", "valid_from", "valid_until")
        }),
    )

@admin.register(models.payment_methods)
class payment_methods(admin.ModelAdmin):
    list_display = ["get_user", "card_type", "last_four_digits", "is_default", "is_active", "created_at"]
    list_filter = ["card_type", "is_default", "is_active", "created_at"]
    search_fields = ["user__username", "last_four_digits", "stripe_payment_method_id"]
    readonly_fields = ["created_at", "updated_at"]
    
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = "User"

@admin.register(models.wallet_top_ups)
class wallet_top_ups(admin.ModelAdmin):
    list_display = ["get_user", "amount", "status", "created_at", "completed_at"]  # Supprimé 'currency'
    list_filter = ["status", "created_at", "completed_at"]  # Supprimé 'currency'
    search_fields = ["wallet__user__username", "stripe_payment_intent_id", "stripe_charge_id"]
    readonly_fields = ["stripe_payment_intent_id", "stripe_charge_id", "created_at", "updated_at"]
    
    def get_user(self, obj):
        return obj.wallet.user.username
    get_user.short_description = "User"
    

@admin.register(models.device_tokens)
class device_tokens_admin(admin.ModelAdmin):
    list_display  = ["id", "user", "token", "created_at"]
    search_fields = ["token", "user__username"]
    list_filter   = ["created_at"]


###################################################################################
# VEHICLES THEME - Vehicles and Categories
###################################################################################

class vehicles(admin.ModelAdmin):
    model = models.vehicles
    list_display = ["id","company","mat","category","mark","model","vehicle_status"]
    list_filter = ["category","vehicle_status","company"]
    search_fields = ["mat", "mat2", "mark", "model"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("company", "category", "mat", "mat2")
        }),
        ("Vehicle Details", {
            "fields": ("mark", "model", "year", "km_t", "max_speed")
        }),
        ("Dimensions", {
            "fields": ("length", "width", "height", "max_weight", "terrestrial_height")
        }),
        ("Documents & Images", {
            "fields": ("image", "image_CG", "image_CGP", "image_insurance")
        }),
        ("Status & Dates", {
            "fields": ("vehicle_status", "date_exp_assur", "date_exp_inscri", "co2_coef_req")
        }),
    )

admin.site.register(models.vehicles, vehicles)

class vehiclecategories(admin.ModelAdmin):
    model = models.vehiclecategories
    list_display = ["id","label","percentage","upper","active"]
    list_filter = ["active","upper"]
    search_fields = ["label"]

admin.site.register(models.vehiclecategories, vehiclecategories)

class vehiclesalloptions(admin.ModelAdmin):
    model = models.vehiclesalloptions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.vehiclesalloptions, vehiclesalloptions)

class vehiclesoptions(admin.ModelAdmin):
    model = models.vehiclesoptions
    list_display = ["id","vehicle","option"]
    list_filter = ["option"]
    search_fields = ["vehicle__mat"]

admin.site.register(models.vehiclesoptions, vehiclesoptions)

###################################################################################
# SHIPMENT TRACKING THEME - New Shipment System
###################################################################################

class carriers(admin.ModelAdmin):
    model = models.carriers
    list_display = ["id", "code", "name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["code", "name"]
    readonly_fields = ["created_at"]

admin.site.register(models.carriers, carriers)

class shipments(admin.ModelAdmin):
    model = models.shipments
    list_display = ["id", "tracking_number", "carrier", "broker_user", "tracking_type", "current_status", "created_at"]
    list_filter = ["tracking_type", "current_status", "carrier", "broker_user"]
    search_fields = ["mbl_booking_number", "container_number", "vehicle_number", "internal_reference"]
    readonly_fields = ["created_at", "updated_at", "last_updated"]
    filter_horizontal = ["tags"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("broker_user", "carrier", "internal_reference")
        }),
        ("Tracking Information", {
            "fields": ("tracking_type", "mbl_booking_number", "container_number", "vehicle_number")
        }),
        ("Shipment Details", {
            "fields": ("origin_port", "destination_port", "vessel_name", "voyage_number", "etd", "eta")
        }),
        ("Customer Information", {
            "fields": ("customer_name", "customer_email", "customer_phone", "customer_address")
        }),
        ("Status & Classification", {
            "fields": ("current_status", "tags", "delay_reason", "cancellation_reason", "new_eta")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "last_updated"),
            "classes": ("collapse",)
        })
    )

admin.site.register(models.shipments, shipments)

class shipment_tags(admin.ModelAdmin):
    model = models.shipment_tags
    list_display = ["id", "name", "broker_user", "color", "created_at"]
    list_filter = ["broker_user"]
    search_fields = ["name"]
    readonly_fields = ["created_at"]

admin.site.register(models.shipment_tags, shipment_tags)

class shipment_followers(admin.ModelAdmin):
    model = models.shipment_followers
    list_display = ["id", "shipment", "email", "name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["email", "name"]
    readonly_fields = ["created_at"]

admin.site.register(models.shipment_followers, shipment_followers)

class shipment_status_updates(admin.ModelAdmin):
    model = models.shipment_status_updates
    list_display = ["id", "shipment", "status", "location", "timestamp", "created_by"]
    list_filter = ["status", "created_by"]
    search_fields = ["shipment__mbl_booking_number", "shipment__container_number", "shipment__vehicle_number", "location"]
    readonly_fields = ["timestamp"]
    fieldsets = (
        ("Status Information", {
            "fields": ("shipment", "status", "location", "notes")
        }),
        ("Vessel Information", {
            "fields": ("vessel_name", "voyage_number")
        }),
        ("Dates", {
            "fields": ("estimated_date", "actual_date")
        }),
        ("Metadata", {
            "fields": ("created_by", "timestamp"),
            "classes": ("collapse",)
        })
    )

admin.site.register(models.shipment_status_updates, shipment_status_updates)

class broker_profiles(admin.ModelAdmin):
    model = models.broker_profiles
    list_display = ["id", "user", "company_name", "website", "created_at"]
    search_fields = ["company_name", "user__username", "user__email"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("User Information", {
            "fields": ("user",)
        }),
        ("Company Information", {
            "fields": ("company_name", "website", "business_address", "tax_number")
        }),
        ("Branding", {
            "fields": ("brand_color",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

admin.site.register(models.broker_profiles, broker_profiles)

class notification_logs(admin.ModelAdmin):
    model = models.notification_logs
    list_display = ["id", "shipment", "recipient_email", "notification_type", "status", "sent_at", "created_at"]
    list_filter = ["status", "notification_type"]
    search_fields = ["recipient_email", "shipment__mbl_booking_number", "shipment__container_number", "shipment__vehicle_number"]
    readonly_fields = ["created_at", "sent_at"]

admin.site.register(models.notification_logs, notification_logs)

###################################################################################
# OPERATIONS THEME - Requests, Missions, Attributions
###################################################################################

class requests(admin.ModelAdmin):
    model = models.requests
    list_display = ["id","user","Rref","category","charge_date","discharge_date","state","budget","payment_type","company","C_invoice","P_invoice"]
    list_filter = ["state","category","payment_type"]
    search_fields = ["Rref", "user__username"]

admin.site.register(models.requests, requests)

class missions(admin.ModelAdmin):
    model = models.missions
    list_display = ["id","request","merch_nature","palette_type","dep_address","arr_address","state"]
    list_filter = ["merch_nature","palette_type","state"]
    search_fields = ["request__Rref", "ref"]

admin.site.register(models.missions, missions)

class attributions(admin.ModelAdmin):
    model = models.attributions
    list_display = ["id","request","company","user","vehicle","state"]
    search_fields = ["request__Rref", "company__name", "user__username"]
    list_filter = ["state"]

admin.site.register(models.attributions, attributions)

class requestoffers(admin.ModelAdmin):
    model = models.requestoffers
    list_display = ["id","request","company","value","charge_date","active"]
    list_filter = ["active"]
    search_fields = ["request__Rref", "company__name"]

admin.site.register(models.requestoffers, requestoffers)

class missions_tracker(admin.ModelAdmin):
    model = models.missions_tracker
    list_display = ["id","mission","Lat","Lng","created_at"]
    search_fields = ["mission__request__Rref"]

admin.site.register(models.missions_tracker, missions_tracker)

class mission_files(admin.ModelAdmin):
    model = models.mission_files
    list_display = ["id","mission"]
    search_fields = ["mission__request__Rref"]

admin.site.register(models.mission_files, mission_files)

class requestsoptions(admin.ModelAdmin):
    model = models.requestsoptions
    list_display = ["id","request","option"]
    list_filter = ["option"]
    search_fields = ["request__Rref"]

admin.site.register(models.requestsoptions, requestsoptions)

class missionsoptions(admin.ModelAdmin):
    model = models.missionsoptions
    list_display = ["id","mission","option"]
    list_filter = ["option"]
    search_fields = ["mission__request__Rref"]

admin.site.register(models.missionsoptions, missionsoptions)

class requestcodes(admin.ModelAdmin):
    model = models.requestcodes
    list_display = ["id","request","code"]
    search_fields = ["request__Rref", "code"]

admin.site.register(models.requestcodes, requestcodes)

###################################################################################
# SETTINGS THEME - Geographic and Language Settings
###################################################################################

class countries(admin.ModelAdmin):
    model = models.countries
    list_display = ["id","label","country_code","phone_code","currency","active"]
    list_filter = ["active","currency"]
    search_fields = ["label", "country_code"]

admin.site.register(models.countries, countries)

class cities(admin.ModelAdmin):
    model = models.cities
    list_display = ["id","label","country","active"]
    list_filter = ["country","active"]
    search_fields = ["label"]

admin.site.register(models.cities, cities)

class currencies(admin.ModelAdmin):
    model = models.currencies
    list_display = ["id","label","code","rate","active"]
    list_filter = ["active"]
    search_fields = ["label", "code"]

admin.site.register(models.currencies, currencies)

class languages(admin.ModelAdmin):
    model = models.languages
    list_display = ["id","code","active","default"]
    list_filter = ["active","default"]
    search_fields = ["code"]

admin.site.register(models.languages, languages)

class language_pack(admin.ModelAdmin):
    model = models.language_pack
    list_display = ["id","ref","value","code"]
    list_filter = ["code"]
    search_fields = ["ref", "value"]

admin.site.register(models.language_pack, language_pack)

###################################################################################
# CONFIGURATION THEME - System Configuration
###################################################################################

class permissions(admin.ModelAdmin):
    model = models.permissions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.permissions, permissions)

class statuses(admin.ModelAdmin):
    model = models.statuses
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.statuses, statuses)

class genders(admin.ModelAdmin):
    model = models.genders
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.genders, genders)

class paymenttype(admin.ModelAdmin):
    model = models.paymenttype
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.paymenttype, paymenttype)

class palettype(admin.ModelAdmin):
    model = models.palettype
    list_display = ["id","label","length","width","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.palettype, palettype)

class merchnature(admin.ModelAdmin):
    model = models.merchnature
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.merchnature, merchnature)

class missionsalloptions(admin.ModelAdmin):
    model = models.missionsalloptions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["label"]

admin.site.register(models.missionsalloptions, missionsalloptions)

class settings(admin.ModelAdmin):
    model = models.settings
    list_display = ["id","code","value","file"]
    search_fields = ["code"]

admin.site.register(models.settings, settings)

class VAT(admin.ModelAdmin):
    model = models.VAT
    list_display = ["id","value","active"]
    list_filter = ["active"]
    search_fields = ["value"]

admin.site.register(models.VAT, VAT)

class banner(admin.ModelAdmin):
    model = models.banner
    list_display = ["id","title","url","description","active"]
    list_filter = ["active"]
    search_fields = ["title"]

admin.site.register(models.banner, banner)

###################################################################################
# FINANCIAL THEME - Invoices
###################################################################################

class C_invoices(admin.ModelAdmin):
    model = models.C_invoices
    list_display = ["id","payment_type","stamp","payment_status","created_at"]
    list_filter = ["payment_type","payment_status"]
    search_fields = ["O_name", "C_name"]

admin.site.register(models.C_invoices, C_invoices)

class P_invoices(admin.ModelAdmin):
    model = models.P_invoices
    list_display = ["id","payment_type","stamp","payment_status","created_at"]
    list_filter = ["payment_type","payment_status"]
    search_fields = ["O_name", "C_name"]

admin.site.register(models.P_invoices, P_invoices)
