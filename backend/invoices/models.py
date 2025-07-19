# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('finance', 'Finance'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


from django.db import models
from django.conf import settings

class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Disputed', 'Disputed'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Unreviewed', 'Unreviewed')
    ]
    invoice_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_invoices', null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='approved_invoices', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.vendor.name}"

class Dispute(models.Model):
    CATEGORY_CHOICES = [
        ('Incorrect Amount', 'Incorrect Amount'),
        ('Duplicate', 'Duplicate'),
        ('Late Delivery', 'Late Delivery'),
        ('Goods/Services Issue', 'Goods/Services Issue'),
        ('Other', 'Other')
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Under Review', 'Under Review'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected')
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='raised_disputes')
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    resolution_comments = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='resolved_disputes', null=True, blank=True)
    raised_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='disputes/', null=True, blank=True)
    
    def __str__(self):
        return f"Dispute for {self.invoice.invoice_number} by {self.raised_by.username}"
