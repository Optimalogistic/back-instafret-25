from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    carriers, shipment_tags, shipments, shipment_status_updates, 
    broker_profiles, shipment_followers
)
from .serializers import (
    S_carriers_get, S_carriers_post, S_shipment_tags_get, S_shipment_tags_post,
    S_shipments_get, S_shipments_post, S_shipment_status_updates_post,
    S_broker_profiles_get, S_broker_profiles_post, S_shipments_track_public
)

class V_carriers(viewsets.ReadOnlyModelViewSet):
    """ViewSet for carriers - read only"""
    queryset = carriers.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return S_carriers_get

class V_shipment_tags(viewsets.ModelViewSet):
    """ViewSet for shipment tags"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return shipment_tags.objects.filter(broker_user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return S_shipment_tags_post
        return S_shipment_tags_get
    
    def perform_create(self, serializer):
        serializer.save(broker_user=self.request.user)

class V_shipments(viewsets.ModelViewSet):
    """ViewSet for shipments management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['current_status', 'tracking_type', 'carrier']
    search_fields = ['mbl_booking_number', 'container_number', 'vehicle_number', 'internal_reference']
    ordering_fields = ['created_at', 'updated_at', 'etd', 'eta']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = shipments.objects.filter(broker_user=self.request.user)
        
        # Filter by tags
        tag_names = self.request.query_params.getlist('tags')
        if tag_names:
            queryset = queryset.filter(tags__name__in=tag_names).distinct()
        
        return queryset.prefetch_related('tags', 'followers', 'status_updates')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return S_shipments_post
        return S_shipments_get
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update shipment status"""
        shipment = self.get_object()
        serializer = S_shipment_status_updates_post(data=request.data)
        
        if serializer.is_valid():
            status_update = serializer.save(
                shipment=shipment,
                created_by=request.user.username
            )
            
            # Update shipment current status
            shipment.current_status = status_update.status
            shipment.save()
            
            # TODO: Send notifications (we'll implement this next
