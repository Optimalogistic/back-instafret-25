# optimasite/views_notifications.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import device_tokens
from .serializers import DeviceTokenSerializer   # simple serializer

class V_device_tokens(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = DeviceTokenSerializer
    queryset           = device_tokens.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["post"], detail=False)
    def delete_token(self, request):
        token = request.data.get("token")
        if token:
            device_tokens.objects.filter(token=token, user=request.user).delete()
            return Response({"deleted": True})
        return Response({"error": "token required"}, status=400)
