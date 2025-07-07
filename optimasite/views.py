from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response

from rest_framework import filters
from django.db.models import Q
from rest_framework.views import APIView
from django.conf import settings as A_settings
from django.core.mail import EmailMultiAlternatives, get_connection
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import device_tokens
from .serializers import (
    S_device_tokens_post,   # le serializer POST
    S_device_tokens_get     # le serializer GET
)
# Ajoutez ces imports en haut de votre fichier views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

def get_custom_user(request):
    """
    Retourne une instance du modèle users correspondant à l'utilisateur connecté.
    Si l'utilisateur n'existe pas dans users, il le crée automatiquement.
    """
    if not request.user.is_authenticated:
        return None
    email = getattr(request.user, 'email', None)
    if email:
        try:
            return users.objects.get(email=email)
        except users.DoesNotExist:
            return users.objects.create(
                username=getattr(request.user, 'username', ""),
                email=email,
                firstname=getattr(request.user, 'first_name', ""),
                lastname=getattr(request.user, 'last_name', ""),
                account_status=True,
                permissions_id=3,  # à adapter
                usertype_id=1,     # à adapter
                lang_id=1,         # à adapter
            )
    username = getattr(request.user, 'username', None)
    if username:
        try:
            return users.objects.get(username=username)
        except users.DoesNotExist:
            return users.objects.create(
                username=username,
                email="",
                firstname=getattr(request.user, 'first_name', ""),
                lastname=getattr(request.user, 'last_name', ""),
                account_status=True,
                permissions_id=3,
                usertype_id=1,
                lang_id=1,
            )
    return None


# Your existing views remain unchanged...

class V_companies_get(viewsets.ModelViewSet):
    serializer_class = S_companies_get
    queryset= companies.objects.all()
    http_method_names = ['get']

class V_companies_post(viewsets.ModelViewSet):
    serializer_class = S_companies_post
    queryset= companies.objects.all()
    http_method_names = ['post', 'put']

class V_users_is_name(viewsets.ModelViewSet):
    serializer_class = S_users_is_name
    queryset= users.objects.filter(account_status=1)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username']
    http_method_names = ['get']

class V_register(viewsets.ModelViewSet):
    serializer_class = S_users_flat
    queryset= users.objects.all()
    http_method_names = ['post']

class V_login(viewsets.ModelViewSet):
    serializer_class = S_users_flat
    queryset= users.objects.filter(account_status=1)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username','=phone','=password']
    http_method_names = ['get']

class V_tokens_post(viewsets.ModelViewSet):
    serializer_class = S_tokens_post
    queryset= tokens.objects.all()
    http_method_names = ['post']

class V_tokens_get(viewsets.ModelViewSet):
    serializer_class = S_tokens_get
    queryset= tokens.objects.filter(user__account_status=1)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=token']
    http_method_names = ['get']

class V_countries_get(viewsets.ModelViewSet):
    serializer_class = S_countries_get
    queryset= countries.objects.filter(active=1)
    http_method_names = ['get']

class V_cities_get(viewsets.ModelViewSet):
    serializer_class = S_cities_get
    queryset= cities.objects.filter(active=1)
    filter_backends = [filters.SearchFilter]
    search_fields = ['country__id']
    http_method_names = ['get']

class V_company_all_services_get(viewsets.ModelViewSet):
    serializer_class = S_company_all_services_get
    queryset= companyallservices.objects.filter(active=1)
    http_method_names = ['get']

class V_company_services_get(viewsets.ModelViewSet):
    serializer_class = S_company_services_get
    queryset= companyservices.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['company__id']
    http_method_names = ['get','post','delete']

class V_company_types_get(viewsets.ModelViewSet):
    serializer_class = S_company_types_get
    queryset= companytypes.objects.filter(active=1)
    http_method_names = ['get']

class V_genders_get(viewsets.ModelViewSet):
    serializer_class = S_genders_get
    queryset= genders.objects.filter(active=1)
    http_method_names = ['get']

class V_permissions_get(viewsets.ModelViewSet):
    serializer_class = S_permissions_get
    queryset= permissions.objects.filter(active=1)
    http_method_names = ['get']

class V_statuses_get(viewsets.ModelViewSet):
    serializer_class = S_statuses_get
    queryset= statuses.objects.filter(active=1)
    http_method_names = ['get']

class V_managers_get(viewsets.ModelViewSet):
    serializer_class = S_managers_get
    queryset= users.objects.filter(permissions__gt=1,account_status=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_users_edit(viewsets.ModelViewSet):
    serializer_class = S_users_flat
    queryset= users.objects.all()
    http_method_names = ['put']

class V_users_count(viewsets.ModelViewSet):
    serializer_class = S_users_count
    queryset= users.objects.all()
    http_method_names = ['get']

class V_drivers_get(viewsets.ModelViewSet):
    serializer_class = S_drivers_get
    queryset= users.objects.filter(permissions=1,account_status=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_drivers_no_attri_get(viewsets.ModelViewSet):
    serializer_class = S_drivers_get
    queryset= users.objects.filter(~Q(attribution__state=1),(~Q(attribution__request__state=3)|(Q(attribution__request__state=3)&Q(attribution__mission__state=6))),permissions=1,account_status=1).order_by('-updated_at').distinct()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_vehiclecategories_get(viewsets.ModelViewSet):
    serializer_class = S_vehiclecategories_get
    queryset= vehiclecategories.objects.filter(active=1)
    http_method_names = ['get']

class V_vehiclesalloptions_get(viewsets.ModelViewSet):
    serializer_class = S_vehiclesalloptions_get
    queryset= vehiclesalloptions.objects.filter(active=1)
    http_method_names = ['get']

class V_register_vehicle(viewsets.ModelViewSet):
    serializer_class = S_vehicles
    queryset= vehicles.objects.all()
    http_method_names = ['post']

class V_vehicles_get(viewsets.ModelViewSet):
    serializer_class = S_vehicles_get
    queryset= vehicles.objects.filter(vehicle_status=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_last_vehicles_get(viewsets.ModelViewSet):
    serializer_class = S_last_vehicles_get
    queryset= vehicles.objects.filter(vehicle_status=1).order_by('-attribution__request__updated_at')
    http_method_names = ['get']

class V_vehicles_count(viewsets.ModelViewSet):
    serializer_class = S_vehicles_count
    queryset= vehicles.objects.all()
    http_method_names = ['get']

class V_vehicles_no_attri_get(viewsets.ModelViewSet):
    serializer_class = S_vehicles_get_A
    queryset= vehicles.objects.filter(~Q(attribution__state=1),(~Q(attribution__request__state=3)|(Q(attribution__request__state=3)&Q(attribution__mission__state=6))),vehicle_status=1).order_by('-updated_at').distinct()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_vehicles_edit(viewsets.ModelViewSet):
    serializer_class = S_vehicles
    queryset= vehicles.objects.all()
    http_method_names = ['put']

class V_vehicles_options_get(viewsets.ModelViewSet):
    serializer_class = S_vehiclesoptions_get
    queryset= vehiclesoptions.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['vehicle__id']
    http_method_names = ['get','post','delete']

class V_attributions_get(viewsets.ModelViewSet):
    serializer_class = S_attributions_get
    queryset= attributions.objects.all().order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get', 'delete']

class V_last_attributions_get(viewsets.ModelViewSet):
    serializer_class = S_last_attributions_get
    queryset= attributions.objects.filter(state=2).order_by('-updated_at')
    http_method_names = ['get']

class V_driver_attributions_get(viewsets.ModelViewSet):
    serializer_class = S_attributions_get
    queryset= attributions.objects.all().order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_attributions_post(viewsets.ModelViewSet):
    serializer_class = S_attributions_post
    queryset= attributions.objects.all()
    filter_backends = [filters.SearchFilter]
    http_method_names = ['post', 'put']

class V_palettype_get(viewsets.ModelViewSet):
    serializer_class = S_palettype_get
    queryset= palettype.objects.filter(active=1)
    http_method_names = ['get']

class V_merchnature_get(viewsets.ModelViewSet):
    serializer_class = S_merchnature_get
    queryset= merchnature.objects.filter(active=1)
    http_method_names = ['get']

class V_paymenttype_get(viewsets.ModelViewSet):
    serializer_class = S_paymenttype_get
    queryset= paymenttype.objects.filter(active=1)
    http_method_names = ['get']

class V_missionsalloptions_get(viewsets.ModelViewSet):
    serializer_class = S_missionsalloptions_get
    queryset= missionsalloptions.objects.all()
    http_method_names = ['get']

class V_requests_post(viewsets.ModelViewSet):
    serializer_class = S_requests_post
    queryset= requests.objects.all()
    http_method_names = ['post','put']

class V_requests_count(viewsets.ModelViewSet):
    serializer_class = S_requests_count
    queryset= requests.objects.filter(state__gte=5)
    http_method_names = ['get']

class V_requestsoptions_post(viewsets.ModelViewSet):
    serializer_class = S_requestsoptions_post
    queryset= requestsoptions.objects.all()
    http_method_names = ['post']

class V_missions_post(viewsets.ModelViewSet):
    serializer_class = S_missions_post
    queryset= missions.objects.all()
    http_method_names = ['post','put']

class V_missionsoptions_post(viewsets.ModelViewSet):
    serializer_class = S_missionsoptions_post
    queryset= missionsoptions.objects.all()
    http_method_names = ['post']

class V_user_requests_get(viewsets.ModelViewSet):
    serializer_class = S_user_requests_get
    queryset= requests.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_last_requests_get(viewsets.ModelViewSet):
    serializer_class = S_user_requests_get
    queryset= requests.objects.filter(state=1).order_by('-updated_at')
    http_method_names = ['get']

class V_search_requests_get(viewsets.ModelViewSet):
    serializer_class = S_user_requests_get
    queryset= requests.objects.filter(state=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['Rref','=category__id','=category__upper__id','=category__upper__upper__id','=payment_type__id']
    http_method_names = ['get']

class V_search_vehicles_get(viewsets.ModelViewSet):
    serializer_class = S_vehicles_search_get
    queryset= vehicles.objects.filter(vehicle_status=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=category__id','=category__upper__id','=category__upper__upper__id']
    http_method_names = ['get']

class V_requestsoptions_get(viewsets.ModelViewSet):
    serializer_class = S_requestsoptions_get
    queryset= requestsoptions.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=request__id']
    http_method_names = ['get']

class V_allusersaddresses_get(viewsets.ModelViewSet):
    serializer_class = S_usersaddresses_get
    queryset= usersaddresses.objects.all()

class V_usersaddresses_get(viewsets.ModelViewSet):
    serializer_class = S_usersaddresses_get
    queryset= usersaddresses.objects.filter(active__gte=1).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get','delete','put','post']

class V_provider_new_requests_get(viewsets.ModelViewSet):
    serializer_class = S_provider_requests_get
    queryset= requests.objects.filter(state=1)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=category__id']
    http_method_names = ['get']

class V_requestoffers_post(viewsets.ModelViewSet):
    serializer_class = S_requestoffers_post
    queryset= requestoffers.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']
    http_method_names = ['get','delete','put','post']

class V_provider_requests_get(viewsets.ModelViewSet):
    serializer_class = S_provider_requests_get
    queryset= requests.objects.filter(state__gte=2)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_request_P_invoices(viewsets.ModelViewSet):
    serializer_class = S_request_P_invoices
    queryset= P_invoices.objects.all()
    http_method_names = ['get','post']

class V_request_C_invoices(viewsets.ModelViewSet):
    serializer_class = S_request_C_invoices
    queryset= C_invoices.objects.all()
    http_method_names = ['get','post']

class V_missions_tracker_get(viewsets.ModelViewSet):
    serializer_class = S_missions_tracker_get
    queryset= missions_tracker.objects.all()
    http_method_names = ['post','put']

class V_mission_files(viewsets.ModelViewSet):
    serializer_class = S_mission_files
    queryset= mission_files.objects.all()
    http_method_names = ['post']

class V_company_ratings_get(viewsets.ModelViewSet):
    serializer_class = S_company_ratings_get
    queryset= attributions.objects.filter(request__state__gte=5).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=company__id']
    http_method_names = ['get']

class V_user_ratings_get(viewsets.ModelViewSet):
    serializer_class = S_user_ratings_get
    queryset= attributions.objects.filter(request__state__gte=5).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_vehicle_ratings_get(viewsets.ModelViewSet):
    serializer_class = S_vehicle_ratings_get
    queryset= attributions.objects.filter(request__state__gte=5).order_by('-updated_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=vehicle__id']
    http_method_names = ['get']

class V_language_pack_get(viewsets.ModelViewSet):
    serializer_class = S_language_pack
    queryset= language_pack.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=code__id']
    http_method_names = ['get']

class V_languages_get(viewsets.ModelViewSet):
    serializer_class = S_languages
    queryset= languages.objects.filter(active=1)
    http_method_names = ['get']

class V_settings_get(viewsets.ModelViewSet):
    serializer_class = S_settings
    queryset= settings.objects.all()
    http_method_names = ['get']

class V_VAT_get(viewsets.ModelViewSet):
    serializer_class = S_VAT
    queryset= VAT.objects.filter(active=1)
    http_method_names = ['get']

class V_request_copy_get(viewsets.ModelViewSet):
    serializer_class = S_user_requests_get
    queryset= requests.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=user__id']
    http_method_names = ['get']

class V_requestcodes_post(viewsets.ModelViewSet):
    serializer_class = S_requestcodes
    queryset= requestcodes.objects.all()
    http_method_names = ['post']

class V_currencies_get(viewsets.ModelViewSet):
    serializer_class = S_currencies_get
    queryset= currencies.objects.filter(active=1)
    http_method_names = ['get']

class V_banner_get(viewsets.ModelViewSet):
    serializer_class = S_banner_get
    queryset= banner.objects.filter(active=1)
    http_method_names = ['get']

###################################################################################
# NEW SHIPMENT TRACKING VIEWS (Following your naming convention)
###################################################################################

class V_carriers_get(viewsets.ModelViewSet):
    serializer_class = S_carriers_get
    queryset = carriers.objects.filter(is_active=1)
    http_method_names = ['get']

class V_carriers_post(viewsets.ModelViewSet):
    serializer_class = S_carriers_post
    queryset = carriers.objects.all()
    http_method_names = ['post', 'put']

class V_shipment_tags_get(viewsets.ModelViewSet):
    serializer_class = S_shipment_tags_get
    queryset = shipment_tags.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=broker_user__id']
    http_method_names = ['get']

class V_shipment_tags_post(viewsets.ModelViewSet):
    serializer_class = S_shipment_tags_post
    queryset = shipment_tags.objects.all()
    http_method_names = ['post', 'put', 'delete']
    
    def perform_create(self, serializer):
        # Get the broker_user from the request context
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            serializer.save(broker_user=self.request.user)

class V_shipments_get(viewsets.ModelViewSet):
    serializer_class = S_shipments_get
    queryset = shipments.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=broker_user__id', '=current_status', '=tracking_type', '=carrier__id', 'mbl_booking_number', 'container_number', 'vehicle_number', 'internal_reference']
    http_method_names = ['get']

class V_shipments_post(viewsets.ModelViewSet):
    serializer_class = S_shipments_post
    queryset = shipments.objects.all()
    http_method_names = ['post', 'put']

class V_shipments_count(viewsets.ModelViewSet):
    serializer_class = S_shipments_count
    queryset = shipments.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=broker_user__id']
    http_method_names = ['get']

class V_shipments_track_public(viewsets.ModelViewSet):
    serializer_class = S_shipments_track_public
    queryset = shipments.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=carrier__code', 'mbl_booking_number', 'container_number', 'vehicle_number']
    http_method_names = ['get']

class V_shipment_status_updates_get(viewsets.ModelViewSet):
    serializer_class = S_shipment_status_updates_get
    queryset = shipment_status_updates.objects.all().order_by('-timestamp')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=shipment__id']
    http_method_names = ['get']

class V_shipment_status_updates_post(viewsets.ModelViewSet):
    serializer_class = S_shipment_status_updates_post
    queryset = shipment_status_updates.objects.all()
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        # Get shipment_id from request data
        shipment_id = request.data.get('shipment_id')
        if not shipment_id:
            return Response({'error': 'shipment_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            shipment = shipments.objects.get(id=shipment_id)
        except shipments.DoesNotExist:
            return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the status update
            status_update = serializer.save(
                shipment=shipment,
                created_by=request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'SYSTEM'
            )
            
            # Update shipment current status
            shipment.current_status = status_update.status
            shipment.save()
            
            # TODO: Send notifications to followers (implement later)
            
            return Response({
                'message': 'Status updated successfully',
                'status': status_update.status,
                'shipment_id': shipment.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class V_shipment_followers_get(viewsets.ModelViewSet):
    serializer_class = S_shipment_followers_get
    queryset = shipment_followers.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=shipment__id']
    http_method_names = ['get']

class V_shipment_followers_post(viewsets.ModelViewSet):
    serializer_class = S_shipment_followers_post
    queryset = shipment_followers.objects.all()
    http_method_names = ['post', 'put', 'delete']

class V_broker_profiles_get(viewsets.ModelViewSet):
    serializer_class = S_broker_profiles_get
    queryset = broker_profiles.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_broker_profiles_post(viewsets.ModelViewSet):
    serializer_class = S_broker_profiles_post
    queryset = broker_profiles.objects.all()
    http_method_names = ['post', 'put']
    
    def perform_create(self, serializer):
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

class V_notification_logs_get(viewsets.ModelViewSet):
    serializer_class = S_notification_logs_get
    queryset = notification_logs.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['=shipment__id', '=shipment__broker_user__id']
    http_method_names = ['get']

class EmailAPI(APIView):
    def post(self, request, *args, **kwargs):
        with get_connection(
            host=A_settings.EMAIL_HOST,
            port=A_settings.EMAIL_PORT,
            username=A_settings.EMAIL_HOST_USER,
            password=A_settings.EMAIL_HOST_PASSWORD,
            use_tls=A_settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = A_settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message=""
            html_message = request.POST.get("html_message")
            Email=EmailMultiAlternatives(subject, message,email_from, recipient_list, connection=connection)
            Email.attach_alternative(html_message, "text/html")
            Email.send()
        return HttpResponse('')
# Add these enhanced wallet views

class V_admin_credit_wallet(viewsets.ModelViewSet):
    """Admin endpoint to credit user wallets"""
    serializer_class = S_admin_wallet_action
    queryset = user_wallets.objects.all()
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        from .services.wallet_service import EnhancedWalletService
        
        # Check if user is admin/staff
        if not request.user.is_staff:
            return Response({
                'success': False,
                'error': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wallet_service = EnhancedWalletService()
            
            try:
                target_user = users.objects.get(id=serializer.validated_data['user_id'])
            except users.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            result = wallet_service.admin_credit_wallet(
                user=target_user,
                amount=serializer.validated_data['amount'],
                currency_code=serializer.validated_data['currency_code'],
                admin_user=request.user,
                description=serializer.validated_data.get('description', '')
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'message': f"Credited {serializer.validated_data['amount']} {serializer.validated_data['currency_code']} to {target_user.username}",
                    'new_balance': result['new_balance']
                })
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class V_apply_coupon(viewsets.ModelViewSet):
    """Apply coupon to wallet"""
    serializer_class = S_apply_coupon
    queryset = wallet_coupons.objects.all()
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        from .services.wallet_service import EnhancedWalletService
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wallet_service = EnhancedWalletService()
            result = wallet_service.apply_coupon(
                user=request.user,
                coupon_code=serializer.validated_data['coupon_code'],
                purchase_amount=serializer.validated_data['purchase_amount'],
                currency_code=serializer.validated_data['currency_code']
            )
            
            if result['success']:
                return Response(result)
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class V_wallet_summary(viewsets.ModelViewSet):
    """Get complete wallet summary"""
    serializer_class = S_user_wallets_get
    queryset = user_wallets.objects.all()
    http_method_names = ['get']
    
    def list(self, request, *args, **kwargs):
        from .services.wallet_service import EnhancedWalletService
        
        wallet_service = EnhancedWalletService()
        result = wallet_service.get_wallet_summary(request.user)
        
        if result['success']:
            return Response(result)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)

# Add these wallet views to your existing views.py

class V_supported_currencies_get(viewsets.ModelViewSet):
    serializer_class = S_supported_currencies_get
    queryset = supported_currencies.objects.filter(is_active=True)
    http_method_names = ['get']

class V_user_wallets_get(viewsets.ModelViewSet):
    serializer_class = S_user_wallets_get
    queryset = user_wallets.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_wallet_transactions_get(viewsets.ModelViewSet):
    serializer_class = S_wallet_transactions_get
    queryset = wallet_transactions.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=wallet__user__id', '=wallet__id']
    http_method_names = ['get']

class V_admin_credit_wallet(viewsets.ModelViewSet):
    """Admin endpoint to credit user wallets"""
    serializer_class = S_admin_wallet_action
    queryset = user_wallets.objects.all()
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        from .services.wallet_service import EnhancedWalletService
        
        # Check if user is admin/staff
        if not request.user.is_staff:
            return Response({
                'success': False,
                'error': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wallet_service = EnhancedWalletService()
            
            try:
                target_user = users.objects.get(id=serializer.validated_data['user_id'])
            except users.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            result = wallet_service.admin_credit_wallet(
                user=target_user,
                amount=serializer.validated_data['amount'],
                currency_code=serializer.validated_data['currency_code'],
                admin_user=request.user,
                description=serializer.validated_data.get('description', '')
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'message': f"Credited {serializer.validated_data['amount']} {serializer.validated_data['currency_code']} to {target_user.username}",
                    'new_balance': result['new_balance']
                })
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class V_wallet_summary(viewsets.ModelViewSet):
    """Get complete wallet summary"""
    serializer_class = S_user_wallets_get
    queryset = user_wallets.objects.all()
    http_method_names = ['get']
    
    def list(self, request, *args, **kwargs):
        from .services.wallet_service import EnhancedWalletService
        
        wallet_service = EnhancedWalletService()
        result = wallet_service.get_wallet_summary(request.user)
        
        if result['success']:
            return Response(result)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
            


class V_payment_methods_get(viewsets.ModelViewSet):
    serializer_class = S_payment_methods_get
    queryset = payment_methods.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__id']
    http_method_names = ['get']

class V_wallet_top_ups_get(viewsets.ModelViewSet):
    serializer_class = S_wallet_top_ups_get
    queryset = wallet_top_ups.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=wallet__user__id']
    http_method_names = ['get']


# -------------------------------------------------------------------

class V_device_tokens(viewsets.ModelViewSet):
    """
    • GET    /api/device-tokens/           → liste des tokens de l’utilisateur
    • POST   /api/device-tokens/           → enregistre ou met à jour un token
    • POST   /api/device-tokens/delete_token/
                                            body: {"token": "<token>"}
    """
    permission_classes = [IsAuthenticated]
    serializer_class   = S_device_tokens_get
    queryset           = device_tokens.objects.all()

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if not custom_user:
            return device_tokens.objects.none()
        return self.queryset.filter(user=custom_user)

    def create(self, request, *args, **kwargs):
        serializer = S_device_tokens_post(data=request.data)
        serializer.is_valid(raise_exception=True)
        custom_user = get_custom_user(request)
        if not custom_user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)
        device_tokens.objects.update_or_create(
            token=serializer.validated_data["token"],
            defaults={
                "user": custom_user,
                "user_agent": serializer.validated_data.get("user_agent", ""),
                "is_active": True
            }
        )
        return Response({"saved": True}, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def delete_token(self, request):
        tok = request.data.get("token")
        if not tok:
            return Response({"error": "token required"}, status=400)
        custom_user = get_custom_user(request)
        if not custom_user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)
        deleted, _ = device_tokens.objects.filter(user=custom_user, token=tok).delete()
        return Response({"deleted": bool(deleted)})
    
# # Ajoutez ces vues à la fin de votre fichier views.py

# @staff_member_required
# @csrf_exempt
# def register_device_token(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             token = data.get('token')
#             user_agent = data.get('user_agent', '')
#             user_id = data.get('user_id') or request.user.id
            
#             device, created = device_tokens.objects.get_or_create(
#                 token=token,
#                 defaults={
#                     'user_id': user_id,
#                     'user_agent': user_agent,
#                     'is_active': True
#                 }
#             )
            
#             if not created:
#                 device.is_active = True
#                 device.save()
            
#             return JsonResponse({'success': True, 'created': created})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
    
#     return JsonResponse({'success': False, 'error': 'Method not allowed'})

# @staff_member_required
# def test_notification(request):
#     """Vue pour tester les notifications admin"""
#     from .services.fcm_service import test_admin_notification
    
#     result = test_admin_notification()
#     return JsonResponse(result)

# Ajoutez aussi cette vue pour les device tokens
class V_device_tokens_post(viewsets.ModelViewSet):
    serializer_class = S_device_tokens_post
    queryset = device_tokens.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        custom_user = get_custom_user(self.request)
        if not custom_user:
            raise Exception("Utilisateur non authentifié ou non trouvé")
        # Désactiver les anciens tokens de cet utilisateur
        device_tokens.objects.filter(user=custom_user).update(is_active=False)
        # Créer le nouveau token
        serializer.save(user=custom_user, is_active=True)

class V_device_tokens_get(viewsets.ModelViewSet):
    serializer_class = S_device_tokens_get
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if not custom_user:
            return device_tokens.objects.none()
        return device_tokens.objects.filter(user=custom_user)
    
class V_notifications_get(viewsets.ModelViewSet):
    serializer_class = S_notifications_get
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if not custom_user:
            return notification_logs.objects.none()
        return notification_logs.objects.filter(user=custom_user).order_by('-created_at')[:50]

class V_notifications_post(viewsets.ModelViewSet):
    serializer_class = S_notifications_post
    queryset = notification_logs.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        custom_user = get_custom_user(self.request)
        if not custom_user:
            raise Exception("Utilisateur non authentifié ou non trouvé")
        serializer.save(user=custom_user)
        

# Vues Admin pour Notifications (avec les bons imports)
class V_admin_notifications_send(viewsets.ModelViewSet):
    serializer_class = S_admin_notifications_send
    permission_classes = [IsAuthenticated, IsAdminUser]  # Maintenant IsAdminUser est importé
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        from .services.fcm_service import fcm_service
        
        title = request.data.get('title')
        body = request.data.get('body')
        user_ids = request.data.get('user_ids', [])
        notification_type = request.data.get('type', 'admin')
        
        if not title or not body:
            return Response({'error': 'Title and body are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les utilisateurs
        target_users = users.objects.filter(id__in=user_ids)
        
        if not target_users.exists():
            return Response({'error': 'No valid users found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Envoyer les notifications
        result = fcm_service.send_notification_with_sound(
            tokens=fcm_service.get_user_tokens(target_users),
            title=title,
            body=body,
            data={
                'type': notification_type,
                'admin_sent': 'true'
            }
        )
        
        return Response(result)

class V_admin_notifications_broadcast(viewsets.ModelViewSet):
    serializer_class = S_admin_notifications_broadcast
    permission_classes = [IsAuthenticated, IsAdminUser]  # Maintenant IsAdminUser est importé
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        from .services.fcm_service import fcm_service
        
        title = request.data.get('title')
        body = request.data.get('body')
        target_type = request.data.get('target_type', 'all')
        
        if not title or not body:
            return Response({'error': 'Title and body are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Déterminer les utilisateurs cibles
        if target_type == 'companies':
            target_users = users.objects.filter(user_type__name='Company')
        elif target_type == 'users':
            target_users = users.objects.filter(user_type__name='Client')
        else:
            target_users = users.objects.filter(is_active=True)
        
        # Envoyer par chunks pour éviter les limites
        result = fcm_service.send_chunked_notifications(
            tokens=fcm_service.get_user_tokens(target_users),
            title=title,
            body=body,
            data={
                'type': 'broadcast',
                'target_type': target_type
            }
        )
        
        return Response(result)


class V_notification_settings_get(viewsets.ModelViewSet):
    serializer_class = S_notification_settings_get
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        # Retourner les paramètres de notification de l'utilisateur
        user_settings = {
            'new_requests': True,
            'status_updates': True,
            'new_offers': True,
            'marketing': False,
            'sound_enabled': True,
            'email_notifications': True
        }
        
        # Vous pouvez créer un modèle pour stocker ces préférences
        return Response(user_settings)

class V_notification_settings_post(viewsets.ModelViewSet):
    serializer_class = S_notification_settings_post
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        # Sauvegarder les paramètres de notification
        settings_data = request.data
        
        # Ici vous pouvez sauvegarder dans un modèle UserNotificationSettings
        return Response({'success': True, 'message': 'Settings updated'})

#####  SYSTEM NOUVEU NOTIF ADMIn ######

@csrf_exempt
def register_device_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            user_agent = data.get('user_agent', '')
            custom_user = get_custom_user(request)
            if not custom_user:
                return JsonResponse({'success': False, 'error': 'User not authenticated'})
            device_tokens.objects.filter(user=custom_user).update(is_active=False)
            device, created = device_tokens.objects.get_or_create(
                token=token,
                defaults={
                    'user': custom_user,
                    'user_agent': user_agent,
                    'is_active': True
                }
            )
            if not created:
                device.user = custom_user
                device.is_active = True
                device.user_agent = user_agent
                device.save()
            return JsonResponse({'success': True, 'created': created})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@staff_member_required
def test_notification(request):
    """Vue pour tester les notifications admin"""
    from .services.fcm_service import test_admin_notification
    
    result = test_admin_notification()
    return JsonResponse(result)

@login_required
@csrf_exempt
def mark_notification_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notification_id')
            
            # Marquer comme lu (si vous avez un modèle pour ça)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        # Marquer toutes les notifications comme lues
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def refresh_firebase_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_token = data.get('old_token')
            new_token = data.get('new_token')
            
            if old_token and new_token:
                # Mettre à jour le token
                device_tokens.objects.filter(token=old_token).update(token=new_token)
                return JsonResponse({'success': True})
            
            return JsonResponse({'success': False, 'error': 'Tokens required'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def validate_firebase_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if token:
                exists = device_tokens.objects.filter(token=token, is_active=True).exists()
                return JsonResponse({'valid': exists})
            
            return JsonResponse({'valid': False})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)})
    
    return JsonResponse({'valid': False, 'error': 'Method not allowed'})

@staff_member_required
def notification_statistics(request):
    """Statistiques des notifications pour l'admin"""
    stats = {
        'total_tokens': device_tokens.objects.filter(is_active=True).count(),
        'total_users_with_tokens': device_tokens.objects.filter(is_active=True).values('user').distinct().count(),
        'notifications_sent_today': 0,  # Vous pouvez calculer ça si vous avez un modèle de logs
        'success_rate': 95.5  # Exemple
    }
    
    return JsonResponse(stats)

@staff_member_required
def notification_logs_view(request):
    """Logs des notifications pour l'admin"""
    # Retourner les logs de notifications
    return JsonResponse({'logs': []})

@login_required
def user_notification_preferences(request):
    """Préférences de notification de l'utilisateur"""
    if request.method == 'GET':
        preferences = {
            'new_requests': True,
            'status_updates': True,
            'new_offers': True,
            'sound_enabled': True
        }
        return JsonResponse(preferences)
    
    elif request.method == 'POST':
        # Sauvegarder les préférences
        return JsonResponse({'success': True})

@staff_member_required
@csrf_exempt
def bulk_notify_users(request):
    """Notification en masse aux utilisateurs"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            body = data.get('body')
            
            from .services.fcm_service import fcm_service
            
            # Récupérer tous les utilisateurs clients
            target_users = users.objects.filter(user_type__name='Client', is_active=True)
            
            result = fcm_service.send_chunked_notifications(
                tokens=fcm_service.get_user_tokens(target_users),
                title=title,
                body=body,
                data={'type': 'bulk_user_notification'}
            )
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@staff_member_required
@csrf_exempt
def bulk_notify_companies(request):
    """Notification en masse aux entreprises"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            body = data.get('body')
            
            from .services.fcm_service import fcm_service
            
            # Récupérer toutes les entreprises
            target_users = users.objects.filter(user_type__name='Company', is_active=True)
            
            result = fcm_service.send_chunked_notifications(
                tokens=fcm_service.get_user_tokens(target_users),
                title=title,
                body=body,
                data={'type': 'bulk_company_notification'}
            )
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
