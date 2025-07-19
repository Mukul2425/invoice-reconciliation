from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from rest_framework import status as drf_status
from rest_framework.response import Response


from rest_framework import permissions

class IsAdminOrFinance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ['admin', 'finance'] or request.user.is_superuser
        )

class IsOwnerOrAdminOrFinance(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For safe methods or if user is owner/admin/finance
        return (
            request.method in permissions.SAFE_METHODS
            or obj.created_by == request.user
            or getattr(request.user, 'role', None) in ['admin', 'finance']
            or request.user.is_superuser
        )

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    # Anyone can register, so no permission_classes => open endpoint



from rest_framework import viewsets, permissions, filters
from .models import Invoice, Dispute, Vendor
from .serializers import InvoiceSerializer, DisputeSerializer, VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsOwnerOrAdminOrFinance]
    filterset_fields = ['status', 'vendor__name', 'due_date']
    search_fields = ['invoice_number', 'tags']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        status_before = instance.status
        response = super().partial_update(request, *args, **kwargs)
        instance.refresh_from_db()
        # Key fix: Only set approved_by if status went to Approved, and it's not already set!
        if instance.status == "Approved" and (instance.approved_by is None or instance.approved_by != request.user):
            instance.approved_by = request.user
            instance.save(update_fields=['approved_by'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    permission_classes = [IsOwnerOrAdminOrFinance]
    filterset_fields = ['status', 'category', 'invoice__invoice_number']
    search_fields = ['description']

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)



