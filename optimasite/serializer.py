from rest_framework import serializers
from .models import *

class S_currencies_get(serializers.ModelSerializer):
    class Meta:
        model = currencies
        fields = '__all__'

class S_countries_get(serializers.ModelSerializer):
    currency=S_currencies_get(many=False)
    class Meta:
        model = countries
        fields = '__all__'

class S_companies_get(serializers.ModelSerializer):
    country=S_countries_get(many=False)
    class Meta:
        model = companies
        fields = '__all__'

class S_companies_post(serializers.ModelSerializer):
    class Meta:
        model = companies
        fields = '__all__'

class S_users_flat(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'

class S_users_count(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['id']

class S_users(serializers.ModelSerializer):
    company=S_companies_get(many=False)
    country=S_countries_get(many=False)
    class Meta:
        model = users
        fields = '__all__'

class S_users_is_name(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['username']

class S_tokens_post(serializers.ModelSerializer):
    class Meta:
        model = tokens
        fields = ['token','user']

class S_tokens_get(serializers.ModelSerializer):
    user=S_users(many=False)
    class Meta:
        model = tokens
        fields = ['token','user']
        
class S_cities_get(serializers.ModelSerializer):
    class Meta:
        model = cities
        fields = '__all__'

class S_company_all_services_get(serializers.ModelSerializer):
    class Meta:
        model = companyallservices
        fields = '__all__'

class S_company_services_get(serializers.ModelSerializer):
    class Meta:
        model = companyservices
        fields = '__all__'

class S_company_types_get(serializers.ModelSerializer):
    class Meta:
        model = companytypes
        fields = '__all__'

class S_genders_get(serializers.ModelSerializer):
    class Meta:
        model = genders
        fields = '__all__'

class S_permissions_get(serializers.ModelSerializer):
    class Meta:
        model = permissions
        fields = '__all__'

class S_statuses_get(serializers.ModelSerializer):
    class Meta:
        model = statuses
        fields = '__all__'

class S_managers_get(serializers.ModelSerializer):
    permissions=S_permissions_get(many=False)
    gender=S_genders_get(many=False)
    status=S_statuses_get(many=False)
    class Meta:
        model = users
        fields = '__all__'

class S_vehiclecategories_get(serializers.ModelSerializer):
    class Meta:
        model = vehiclecategories
        fields = '__all__'

class S_vehiclesalloptions_get(serializers.ModelSerializer):
    class Meta:
        model = vehiclesalloptions
        fields = '__all__'

class S_vehicles(serializers.ModelSerializer):
    category=S_vehiclecategories_get
    class Meta:
        model = vehicles
        fields = '__all__'

class S_vehicle_with_cat(serializers.ModelSerializer):
    category=S_vehiclecategories_get(many=False)
    class Meta:
        model = vehicles
        fields = '__all__'

class S_vehiclesoptions_get(serializers.ModelSerializer):
    class Meta:
        model = vehiclesoptions
        fields = '__all__'

class S_vehiclesoptions_sub(serializers.ModelSerializer):
    option=S_vehiclesalloptions_get(many=False)
    class Meta:
        model = vehiclesoptions
        fields = '__all__'

class S_request_get_1(serializers.ModelSerializer):
    currency_code=S_currencies_get(many=False)
    class Meta:
        model = requests
        fields = ['id','Rref','company','count_type','count','budget_type','budget','charge_date','discharge_date','state','category','payment_type','user','created_at','updated_at','request_missions','VAT','currency_code']

class S_missions_tracker_get(serializers.ModelSerializer):
    class Meta:
        model = missions_tracker
        fields = '__all__'   

class S_missions_get_1(serializers.ModelSerializer):
    class Meta:
        model = missions
        fields = '__all__'        

class S_attributions_get_forV(serializers.ModelSerializer):
    user=S_users(many=False)
    request=S_request_get_1(many=False)
    mission=S_missions_get_1(many=False)
    class Meta:
        model = attributions
        fields = '__all__'

class S_vehicles_get(serializers.ModelSerializer):
    vehicle_options = S_vehiclesoptions_sub(many=True, read_only=True)
    attribution=S_attributions_get_forV(many=True)
    class Meta:
        model = vehicles
        fields = ['id','mat','mat2','mark','model','length','width','height','max_weight','terrestrial_height','year','km_t','max_speed','date_exp_assur','date_exp_inscri','vehicle_status','image','image_CG','image_CGP','image_insurance','created_at','updated_at','category','company','vehicle_options','attribution']

class S_companies_C(serializers.ModelSerializer):
    country=S_countries_get(many=False)
    city=S_cities_get(many=False)
    class Meta:
        model = companies
        fields = '__all__'

class S_vehicles_search_get(serializers.ModelSerializer):
    category=S_vehiclecategories_get(many=False)
    company=S_companies_C(many=False)
    vehicle_options = S_vehiclesoptions_sub(many=True, read_only=True)
    class Meta:
        model = vehicles
        fields = ['id','mark','model','year','vehicle_status','image','updated_at','category','company','vehicle_options']

class S_last_vehicles_get(serializers.ModelSerializer):
    attribution=S_attributions_get_forV(many=True)
    category=S_vehiclecategories_get(many=False)
    company=S_companies_C(many=False)
    class Meta:
        model = vehicles
        fields = ['id','image','updated_at','category','company','attribution']

class S_vehicles_count(serializers.ModelSerializer):
    class Meta:
        model = vehicles
        fields = ['id']

class S_vehicles_get_A(serializers.ModelSerializer):
    vehicle_options = S_vehiclesoptions_sub(many=True, read_only=True)
    attribution=S_attributions_get_forV(many=True)
    category=S_vehiclecategories_get(many=False)
    class Meta:
        model = vehicles
        fields = ['id','mat','mat2','mark','model','length','width','height','max_weight','terrestrial_height','year','km_t','max_speed','date_exp_assur','date_exp_inscri','vehicle_status','image','image_CG','image_CGP','image_insurance','created_at','updated_at','category','company','vehicle_options','attribution']

class S_attributions_get_forD(serializers.ModelSerializer):
    vehicle=S_vehicle_with_cat(many=False)
    request=S_request_get_1(many=False)
    mission=S_missions_get_1(many=False)
    class Meta:
        model = attributions
        fields = '__all__'

class S_drivers_get(serializers.ModelSerializer):
    permissions=S_permissions_get(many=False)
    gender=S_genders_get(many=False)
    status=S_statuses_get(many=False)
    attribution=S_attributions_get_forD(many=True)
    class Meta:
        model = users
        fields = ['id','permissions','gender','status','username','password','firstname','lastname','email','phone','birthdate','address','image','account_status','created_at','updated_at','date_exp_permi','date_exp_inscri','CIN','image_permit','image_CIN','company','usertype','attribution','lang']

class S_attributions_post(serializers.ModelSerializer):
    class Meta:
        model = attributions
        fields = '__all__'

class S_palettype_get(serializers.ModelSerializer):
    class Meta:
        model = palettype
        fields = '__all__'
    
class S_merchnature_get(serializers.ModelSerializer):
    class Meta:
        model = merchnature
        fields = '__all__'

class S_paymenttype_get(serializers.ModelSerializer):
    class Meta:
        model = paymenttype
        fields = '__all__'

class S_missionsalloptions_get(serializers.ModelSerializer):
    class Meta:
        model = missionsalloptions
        fields = '__all__'

class S_requests_post(serializers.ModelSerializer):
    class Meta:
        model = requests
        fields = '__all__'

class S_requests_count(serializers.ModelSerializer):
    class Meta:
        model = requests
        fields = ['id']

class S_requestsoptions_post(serializers.ModelSerializer):
    class Meta:
        model = requestsoptions
        fields = '__all__'       

class S_missions_post(serializers.ModelSerializer):
    class Meta:
        model = missions
        fields = '__all__'              

class S_missionsoptions_post(serializers.ModelSerializer):
    class Meta:
        model = missionsoptions
        fields = '__all__'         

class S_requestsoptions_get(serializers.ModelSerializer):
    option=S_vehiclesalloptions_get(many=False)
    class Meta:
        model = requestsoptions
        fields = ['option'] 

class S_missionsoptions_get(serializers.ModelSerializer):
    option=S_missionsalloptions_get(many=False)
    class Meta:
        model = requestsoptions
        fields = ['option']     
        
class S_usersaddresses_get(serializers.ModelSerializer):
    class Meta:
        model = usersaddresses
        fields = '__all__'
 
class S_attributions_get_forM(serializers.ModelSerializer):
    user=S_users(many=False)
    vehicle=S_vehicle_with_cat(many=False)
    class Meta:
        model = attributions
        fields = '__all__'

class S_mission_files(serializers.ModelSerializer):
    class Meta:
        model = mission_files
        fields = '__all__'

class S_missions_get(serializers.ModelSerializer):
    mission_options = S_missionsoptions_get(many=True, read_only=True)
    merch_nature=S_merchnature_get(many=False, read_only=True)
    palette_type=S_palettype_get(many=False, read_only=True)
    dep_address=S_usersaddresses_get(many=False)
    arr_address=S_usersaddresses_get(many=False)
    attribution=S_attributions_get_forM(many=True)
    mission_tracker=S_missions_tracker_get(many=True)
    mission_files=S_mission_files(many=True)
    class Meta:
        model = missions
        fields = ['id','count','weight','width','length','height','ref','requester','vendor','PO','description','dep_address','arr_address','dep_address_start','dep_address_end','arr_address_start','arr_address_end','CRval','insuranceval','RPval','CR','insurance','RP','created_at','updated_at','merch_nature','palette_type','mission_options','attribution','state','request','mission_tracker','mission_files','charge_S','charge_E','trip_S','trip_E','discharge_S','discharge_E','CR_status','RP_status']        

class S_attributions_get_forR(serializers.ModelSerializer):
    user=S_users(many=False)
    vehicle=S_vehicle_with_cat(many=False)
    class Meta:
        model = attributions
        fields = '__all__'

class S_requestoffers_get(serializers.ModelSerializer):
    company=S_companies_get(many=False)
    class Meta:
        model = requestoffers
        fields = '__all__'

class S_company_detail(serializers.ModelSerializer):
    type=S_company_types_get(many=False)
    class Meta:
        model = companies
        fields = '__all__'

class S_request_C_invoices(serializers.ModelSerializer):
    class Meta:
        model = C_invoices
        fields = '__all__'

class S_requestcodes(serializers.ModelSerializer):
    class Meta:
        model = requestcodes
        fields = '__all__'

class S_user_requests_get(serializers.ModelSerializer):
    currency_code=S_currencies_get(many=False)
    category=S_vehiclecategories_get(many=False)
    payment_type=S_paymenttype_get(many=False)
    request_options = S_requestsoptions_get(many=True, read_only=True)
    request_missions = S_missions_get(many=True, read_only=True)
    user = S_users(many=False)
    request_offers=S_requestoffers_get(many=True)
    company=S_company_detail(many=False)
    attribution=S_attributions_get_forR(many=True)
    C_invoice=S_request_C_invoices(many=False)
    request_codes=S_requestcodes(many=True)
    class Meta:
        model = requests
        fields = ['id','Rref','company','count_type','count','budget_type','budget','charge_date','discharge_date','state','category','payment_type','user','created_at','updated_at','request_options','request_missions','request_offers','attribution','report','C_invoice','VAT','currency_code','request_codes']
  
class S_requestoffers_post(serializers.ModelSerializer):
    class Meta:
        model = requestoffers
        fields = '__all__'

class S_request_P_invoices(serializers.ModelSerializer):
    class Meta:
        model = P_invoices
        fields = '__all__'

class S_provider_requests_get(serializers.ModelSerializer):
    currency_code=S_currencies_get(many=False)
    category=S_vehiclecategories_get(many=False)
    payment_type=S_paymenttype_get(many=False)
    request_options = S_requestsoptions_get(many=True, read_only=True)
    request_missions = S_missions_get(many=True, read_only=True)
    user = S_users(many=False)
    request_offers=S_requestoffers_get(many=True)
    company=S_company_detail(many=False)
    attribution=S_attributions_get_forR(many=True)
    P_invoice=S_request_P_invoices(many=False)
    request_codes=S_requestcodes(many=True)
    class Meta:
        model = requests
        fields = ['id','Rref','company','count_type','count','budget_type','budget','charge_date','discharge_date','state','category','payment_type','user','created_at','updated_at','request_options','request_missions','request_offers','attribution','report','P_invoice','VAT','currency_code','request_codes']

class S_request_get(serializers.ModelSerializer):
    currency_code=S_currencies_get(many=False)
    request_missions = S_missions_get(many=True, read_only=True)
    request_codes=S_requestcodes(many=True)
    class Meta:
        model = requests
        fields = ['id','Rref','company','count_type','count','budget_type','budget','charge_date','discharge_date','state','category','payment_type','user','created_at','updated_at','request_missions','VAT','currency_code','request_codes']

class S_attributions_get(serializers.ModelSerializer):
    user=S_users(many=False)
    vehicle=S_vehicle_with_cat(many=False)
    request=S_request_get(many=False)
    mission=S_missions_get(many=False)
    class Meta:
        model = attributions
        fields = '__all__'

class S_last_attributions_get(serializers.ModelSerializer):
    company=S_companies_C(many=False)
    class Meta:
        model = attributions
        fields = ['company','company_rating','review','request']

class S_company_ratings_get(serializers.ModelSerializer):
    class Meta:
        model = attributions
        fields = ['company_rating','request','review']

class S_user_ratings_get(serializers.ModelSerializer):
    class Meta:
        model = attributions
        fields = ['user_rating','request']

class S_vehicle_ratings_get(serializers.ModelSerializer):
    class Meta:
        model = attributions
        fields = ['vehicle_rating','request']

class S_language_pack(serializers.ModelSerializer):
    class Meta:
        model = language_pack
        fields = '__all__'

class S_languages(serializers.ModelSerializer):
    class Meta:
        model = languages
        fields = '__all__'

class S_settings(serializers.ModelSerializer):
    class Meta:
        model = settings
        fields = '__all__'

class S_VAT(serializers.ModelSerializer):
    class Meta:
        model = VAT
        fields = '__all__'

class S_banner_get(serializers.ModelSerializer):
    class Meta:
        model = banner
        fields = '__all__'