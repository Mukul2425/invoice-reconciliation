from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegistrationSerializer

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
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'vendor__name', 'due_date']
    search_fields = ['invoice_number', 'tags']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'category', 'invoice__invoice_number']
    search_fields = ['description']

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)
