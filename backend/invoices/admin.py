from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Invoice, Dispute, Vendor

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'vendor', 'amount', 'status', 'due_date', 'created_by', 'approved_by')
    list_filter = ('status', 'vendor', 'due_date', 'tags')
    search_fields = ('invoice_number', 'vendor__name', 'tags')
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'approved_by'
    )
    raw_id_fields = ('vendor',)
    actions = ['approve_invoices']

    def save_model(self, request, obj, form, change):
        if not obj.pk:         # If creating a new invoice
            obj.created_by = request.user
        obj.save()

    def approve_invoices(self, request, queryset):
        for invoice in queryset:
            if invoice.status not in ['Approved', 'Paid']:
                invoice.status = 'Approved'
                invoice.approved_by = request.user
                invoice.save()
        self.message_user(request, "Selected invoices have been marked as approved and current user assigned as approver.")
    approve_invoices.short_description = "Approve selected invoices (set status, set approving user)"

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'category', 'status', 'raised_by', 'raised_at', 'resolved_by', 'resolved_at')
    list_filter = ('status', 'category', 'raised_by', 'resolved_by')
    search_fields = ('invoice__invoice_number', 'description')
    readonly_fields = ('raised_at', 'updated_at', 'resolved_at')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)
