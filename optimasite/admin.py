from django import forms
from django.contrib import admin
from optimasite import models

class attributions(admin.ModelAdmin):
    model = models.attributions
    list_display = ["id","request","company","user","vehicle"]
    search_fields = ["id"]

admin.site.register(models.attributions, attributions)
###################################################################################
class cities(admin.ModelAdmin):
    model = models.cities
    list_display = ["id","label","country"]
    list_filter = ["country"]
    search_fields = ["id"]

admin.site.register(models.cities, cities)
###################################################################################
class companies(admin.ModelAdmin):
    model = models.companies
    list_display = ["id","name","mat","Gname","phone","website","city","country","type"]
    list_filter = ["city","country","type"]
    search_fields = ["id"]

admin.site.register(models.companies, companies)
###################################################################################
class companyallservices(admin.ModelAdmin):
    model = models.companyallservices
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.companyallservices, companyallservices)
###################################################################################
class companyservices(admin.ModelAdmin):
    model = models.companyservices
    list_display = ["id","company","service"]
    search_fields = ["company"]

admin.site.register(models.companyservices, companyservices)
###################################################################################
class companytypes(admin.ModelAdmin):
    model = models.companytypes
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.companytypes, companytypes)
###################################################################################
class countries(admin.ModelAdmin):
    model = models.countries
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.countries, countries)
###################################################################################
class C_invoices(admin.ModelAdmin):
    model = models.C_invoices
    list_display = ["id","payment_type","stamp","payment_status"]
    list_filter = ["payment_type","payment_status"]
    search_fields = ["id"]

admin.site.register(models.C_invoices, C_invoices)
###################################################################################
class genders(admin.ModelAdmin):
    model = models.genders
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.genders, genders)
###################################################################################
class languages(admin.ModelAdmin):
    model = models.languages
    list_display = ["id","code","active","default"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.languages, languages)
###################################################################################
class language_pack(admin.ModelAdmin):
    model = models.language_pack
    list_display = ["id","ref","value","code"]
    list_filter = ["code"]
    search_fields = ["ref"]

admin.site.register(models.language_pack, language_pack)
###################################################################################
class merchnature(admin.ModelAdmin):
    model = models.merchnature
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.merchnature, merchnature)
###################################################################################
class missions(admin.ModelAdmin):
    model = models.missions
    list_display = ["id","request","merch_nature","palette_type","dep_address","arr_address"]
    list_filter = ["merch_nature","palette_type"]
    search_fields = ["id"]

admin.site.register(models.missions, missions)
###################################################################################
class missionsalloptions(admin.ModelAdmin):
    model = models.missionsalloptions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.missionsalloptions, missionsalloptions)
###################################################################################
class missionsoptions(admin.ModelAdmin):
    model = models.missionsoptions
    list_display = ["id","mission","option"]
    list_filter = ["option"]
    search_fields = ["id"]

admin.site.register(models.missionsoptions, missionsoptions)
###################################################################################
class missions_tracker(admin.ModelAdmin):
    model = models.missionsoptions
    list_display = ["id","mission","Lat","Lng"]
    search_fields = ["mission"]

admin.site.register(models.missions_tracker, missions_tracker)
###################################################################################
class mission_files(admin.ModelAdmin):
    model = models.mission_files
    list_display = ["id","mission"]
    search_fields = ["mission"]

admin.site.register(models.mission_files, mission_files)
###################################################################################
class palettype(admin.ModelAdmin):
    model = models.palettype
    list_display = ["id","label","length","width","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.palettype, palettype)
###################################################################################
class paymenttype(admin.ModelAdmin):
    model = models.paymenttype
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.paymenttype, paymenttype)
###################################################################################
class permissions(admin.ModelAdmin):
    model = models.permissions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.permissions, permissions)
###################################################################################
class P_invoices(admin.ModelAdmin):
    model = models.P_invoices
    list_display =  ["id","payment_type","stamp","payment_status"]
    list_filter = ["payment_type","payment_status"]
    search_fields = ["id"]

admin.site.register(models.P_invoices, P_invoices)
###################################################################################
class requestoffers(admin.ModelAdmin):
    model = models.requestoffers
    list_display = ["id","request","company","value","charge_date","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.requestoffers, requestoffers)
###################################################################################
class requests(admin.ModelAdmin):
    model = models.requests
    list_display = ["id","user","Rref","category","charge_date","discharge_date","state","budget","payment_type","company","C_invoice","P_invoice"]
    list_filter = ["state","category"]
    search_fields = ["id"]

admin.site.register(models.requests, requests)
###################################################################################
class requestsoptions(admin.ModelAdmin):
    model = models.requests
    list_display = ["id","request","option"]
    list_filter = ["option"]
    search_fields = ["id"]

admin.site.register(models.requestsoptions, requestsoptions)
###################################################################################
class settings(admin.ModelAdmin):
    model = models.requests
    list_display = ["id","code","value","file"]
    search_fields = ["code"]

admin.site.register(models.settings, settings)
###################################################################################
class statuses(admin.ModelAdmin):
    model = models.requests
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.statuses, statuses)
###################################################################################
class tokens(admin.ModelAdmin):
    model = models.tokens
    list_display = ["id","user","token"]
    search_fields = ["id"]

admin.site.register(models.tokens, tokens)
###################################################################################
class users(admin.ModelAdmin):
    usertype=models.usertypes.label
    model = models.users
    list_display = ["username","CIN","firstname","lastname","usertype","permissions","status","account_status"]
    list_filter = ["usertype","permissions","account_status"]
    search_fields = ["username"]

admin.site.register(models.users, users)
###################################################################################
class usersaddresses(admin.ModelAdmin):
    model = models.usersaddresses
    list_display = ["id","user","enterprise"]
    search_fields = ["id"]

admin.site.register(models.usersaddresses, usersaddresses)
################################################################################### 
class usertypes(admin.ModelAdmin):
    model = models.usertypes
    list_display = ["id","label"]
    search_fields = ["id"]

admin.site.register(models.usertypes, usertypes)
################################################################################### 
class VAT(admin.ModelAdmin):
    model = models.VAT
    list_display = ["id","value","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.VAT, VAT)
################################################################################### 
class vehiclecategories(admin.ModelAdmin):
    model = models.vehiclecategories
    list_display = ["id","label","percentage","upper","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.vehiclecategories, vehiclecategories)
################################################################################### 
class vehicles(admin.ModelAdmin):
    model = models.vehicles
    list_display = ["id","company","mat","category","vehicle_status"]
    list_filter = ["category","vehicle_status"]
    search_fields = ["id"]

admin.site.register(models.vehicles, vehicles)
################################################################################### 
class vehiclesalloptions(admin.ModelAdmin):
    model = models.vehiclesalloptions
    list_display = ["id","label","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.vehiclesalloptions, vehiclesalloptions)
################################################################################### 
class vehiclesoptions(admin.ModelAdmin):
    model = models.vehiclesoptions
    list_display = ["id","vehicle","option"]
    list_filter = ["option"]
    search_fields = ["id"]

admin.site.register(models.vehiclesoptions, vehiclesoptions)
################################################################################### 
class currencies(admin.ModelAdmin):
    model = models.currencies
    list_display = ["id","label","code","rate","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.currencies, currencies)
###################################################################################
class banner(admin.ModelAdmin):
    model = models.banner
    list_display = ["id","title","url","description","active"]
    list_filter = ["active"]
    search_fields = ["id"]

admin.site.register(models.banner, banner)
###################################################################################
class requestcodes(admin.ModelAdmin):
    model = models.requestcodes
    list_display = ["id","request","code"]
    search_fields = ["request"]

admin.site.register(models.requestcodes, requestcodes)
################################################################################### 