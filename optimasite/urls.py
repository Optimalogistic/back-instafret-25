from django.urls import path,include,re_path

from rest_framework.routers import DefaultRouter

from . import views

from .views import *
from .views import V_device_tokens

router = DefaultRouter()

# Your existing router registrations remain unchanged...
router.register('companies-get',V_companies_get,basename='companies-get')
router.register('companies-post',V_companies_post,basename='companies-post')
router.register('user-is-name',V_users_is_name,basename='user-is-name')
router.register('register',V_register,basename='users')
router.register('login',V_login,basename='login')
router.register('tokensP',V_tokens_post,basename='tokensP')
router.register('tokensG',V_tokens_get,basename='tokensG')
router.register('countries',V_countries_get,basename='countries')
router.register('cities',V_cities_get,basename='cities')
router.register('allservices',V_company_all_services_get,basename='allservices')
router.register('services',V_company_services_get,basename='services')
router.register('companytypes',V_company_types_get,basename='companytypes')
router.register('genders',V_genders_get,basename='genders')
router.register('permissions',V_permissions_get,basename='permissions')
router.register('statuses',V_statuses_get,basename='statuses')
router.register('managers',V_managers_get,basename='managers')
router.register('users-edit',V_users_edit,basename='users-edit')
router.register('drivers',V_drivers_get,basename='drivers')
router.register('drivers-noattri',V_drivers_no_attri_get,basename='drivers-noattri')
router.register('vehiclesallcategories',V_vehiclecategories_get,basename='vehiclesallcategories')
router.register('vehiclesalloptions',V_vehiclesalloptions_get,basename='vehiclesalloptions')
router.register('register-vehicle',V_register_vehicle,basename='register-vehicle')
router.register('vehicles',V_vehicles_get,basename='vehicles')
router.register('vehicles-noattri',V_vehicles_no_attri_get,basename='vehicles-noattri')
router.register('vehicles-edit',V_vehicles_edit,basename='vehicles-edit')
router.register('vehicles-option',V_vehicles_options_get,basename='vehicles-option')
router.register('attributions',V_attributions_get,basename='attributions')
router.register('attributions-register',V_attributions_post,basename='attributions-register')
router.register('driver-attributions',V_driver_attributions_get,basename='driver-attributions')
router.register('palettype',V_palettype_get,basename='palettype')
router.register('merchnature',V_merchnature_get,basename='merchnature')
router.register('paymenttype',V_paymenttype_get,basename='paymenttype')
router.register('missionsalloptions',V_missionsalloptions_get,basename='missionsalloptions')
router.register('request-post',V_requests_post,basename='request-post')
router.register('request-options-post',V_requestsoptions_post,basename='request-options-post')
router.register('mission-post',V_missions_post,basename='mission-post')
router.register('mission-options-post',V_missionsoptions_post,basename='mission-options-post')
router.register('user-requests',V_user_requests_get,basename='user-requests')
router.register('request-options',V_requestsoptions_get,basename='request-options')
router.register('all-users-addresses',V_allusersaddresses_get,basename='all-users-addresses')
router.register('users-addresses',V_usersaddresses_get,basename='users-addresses')
router.register('provider-new-requests',V_provider_new_requests_get,basename='provider-new-requests')
router.register('request-offers',V_requestoffers_post,basename='request-offers')
router.register('provider-requests',V_provider_requests_get,basename='provider-requests')
router.register('missions-tracker',V_missions_tracker_get,basename='missions-tracker')
router.register('mission-files',V_mission_files,basename='mission-files')
router.register('company-ratings',V_company_ratings_get,basename='company-ratings')
router.register('user-ratings',V_user_ratings_get,basename='user-ratings')
router.register('vehicle-ratings',V_vehicle_ratings_get,basename='vehicle-ratings')
router.register('languages',V_languages_get,basename='languages')
router.register('language-pack',V_language_pack_get,basename='language-pack')
router.register('user-count',V_users_count,basename='user-count')
router.register('vehicle-count',V_vehicles_count,basename='vehicle-count')
router.register('request-count',V_requests_count,basename='request-count')
router.register('last-vehicles',V_last_vehicles_get,basename='last-vehicles')
router.register('last-requests',V_last_requests_get,basename='last-requests')
router.register('last-attributions',V_last_attributions_get,basename='last-attributions')
router.register('search-requests',V_search_requests_get,basename='search-requests')
router.register('search-vehicles',V_search_vehicles_get,basename='search-vehicles')
router.register('request-P-invoices',V_request_P_invoices,basename='request-P-invoices')
router.register('request-C-invoices',V_request_C_invoices,basename='request-C-invoices')
router.register('settings',V_settings_get,basename='settings')
router.register('VAT',V_VAT_get,basename='VAT')
router.register('request-copy',V_request_copy_get,basename='request-copy')
router.register('request-code',V_requestcodes_post,basename='request-code')
router.register('currencies',V_currencies_get,basename='currencies')
router.register('banner',V_banner_get,basename='banner')

###################################################################################
# NEW SHIPMENT TRACKING ENDPOINTS (Following your naming convention)
###################################################################################
# NEW SHIPMENT TRACKING ENDPOINTS
router.register('carriers-get',V_carriers_get,basename='carriers-get')
router.register('carriers-post',V_carriers_post,basename='carriers-post')
router.register('shipment-tags-get',V_shipment_tags_get,basename='shipment-tags-get')
router.register('shipment-tags-post',V_shipment_tags_post,basename='shipment-tags-post')
router.register('shipments-get',V_shipments_get,basename='shipments-get')
router.register('shipments-post',V_shipments_post,basename='shipments-post')
router.register('shipments-count',V_shipments_count,basename='shipments-count')
router.register('shipments-track-public',V_shipments_track_public,basename='shipments-track-public')
router.register('shipment-status-get',V_shipment_status_updates_get,basename='shipment-status-get')
router.register('shipment-status-post',V_shipment_status_updates_post,basename='shipment-status-post')
router.register('shipment-followers-get',V_shipment_followers_get,basename='shipment-followers-get')
router.register('shipment-followers-post',V_shipment_followers_post,basename='shipment-followers-post')
router.register('broker-profiles-get',V_broker_profiles_get,basename='broker-profiles-get')
router.register('broker-profiles-post',V_broker_profiles_post,basename='broker-profiles-post')
router.register('notification-logs-get',V_notification_logs_get,basename='notification-logs-get')

# NEW WALLET ENDPOINTS
router.register('supported-currencies-get', V_supported_currencies_get, basename='supported-currencies-get')
router.register('user-wallets-get', V_user_wallets_get, basename='user-wallets-get')
router.register('wallet-transactions-get', V_wallet_transactions_get, basename='wallet-transactions-get')
router.register('admin-credit-wallet', V_admin_credit_wallet, basename='admin-credit-wallet')
router.register('wallet-summary', V_wallet_summary, basename='wallet-summary')

# notification firebase
router.register('device-tokens', V_device_tokens, basename='device-tokens')


# Device Tokens Management
router.register('device-tokens-get', V_device_tokens_get, basename='device-tokens-get')
router.register('device-tokens-post', V_device_tokens_post, basename='device-tokens-post')

# Notification Management  
router.register('notifications-get', V_notifications_get, basename='notifications-get')
router.register('notifications-post', V_notifications_post, basename='notifications-post')

# Admin Notification Controls
router.register('admin-notifications-send', V_admin_notifications_send, basename='admin-notifications-send')
router.register('admin-notifications-broadcast', V_admin_notifications_broadcast, basename='admin-notifications-broadcast')

# Notification Settings
router.register('notification-settings-get', V_notification_settings_get, basename='notification-settings-get')
router.register('notification-settings-post', V_notification_settings_post, basename='notification-settings-post')

# IMPORTANT: urlpatterns should come AFTER all router registrations

urlpatterns = [

path('',include(router.urls)),

re_path('send-email', EmailAPI.as_view()),

###################################################################################

# FIREBASE NOTIFICATIONS DIRECT ENDPOINTS

###################################################################################
path('api/device-tokens/', views.register_device_token, name='register_device_token'),
 
# Device Token Registration (for web admin)
path('device-tokens-register/', views.register_device_token, name='device-tokens-register'),

# Admin Notification Testing
path('admin/test-notifications/', views.test_notification, name='admin-test-notifications'),

# Notification Status Updates
path('notifications/mark-read/', views.mark_notification_read, name='mark-notification-read'),
path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-notifications-read'),

# Firebase Token Management
path('firebase/token-refresh/', views.refresh_firebase_token, name='firebase-token-refresh'),
path('firebase/token-validate/', views.validate_firebase_token, name='firebase-token-validate'),

# Notification Analytics
path('admin/notification-stats/', views.notification_statistics, name='notification-statistics'),
path('admin/notification-logs/', views.notification_logs_view, name='notification-logs'),

# User Notification Preferences
path('user/notification-preferences/', views.user_notification_preferences, name='user-notification-preferences'),

# Bulk Notification Operations
path('admin/bulk-notify-users/', views.bulk_notify_users, name='bulk-notify-users'),
path('admin/bulk-notify-companies/', views.bulk_notify_companies, name='bulk-notify-companies'),

]
