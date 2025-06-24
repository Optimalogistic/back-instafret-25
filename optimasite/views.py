from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.db.models import Q
from rest_framework.views import APIView
from django.conf import settings as A_settings
from django.core.mail import EmailMultiAlternatives, get_connection
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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
