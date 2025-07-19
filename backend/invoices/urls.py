from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, VendorViewSet, InvoiceViewSet, DisputeViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'disputes', DisputeViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('', include(router.urls)),
]
