from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Role: allow frontend to pick on signup, or omit this field for just 'user'
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'role')
        extra_kwargs = {'role': {'default': 'user'}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user

from rest_framework import serializers
from .models import Invoice, Dispute, Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_info']

class InvoiceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        source='vendor',
        write_only=True
    )
    created_by = serializers.StringRelatedField(read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'vendor', 'vendor_id', 'amount', 'currency',
            'issue_date', 'due_date', 'paid_date', 'payment_method', 'status',
            'remarks', 'created_by', 'approved_by', 'tags', 'created_at',
            'updated_at', 'attachment'
        ]
        read_only_fields = ['created_by', 'approved_by', 'created_at', 'updated_at']

class DisputeSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    invoice_id = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.objects.all(),
        source='invoice',
        write_only=True
    )
    raised_by = serializers.StringRelatedField(read_only=True)
    resolved_by = serializers.StringRelatedField(read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Dispute
        fields = [
            'id', 'invoice', 'invoice_id', 'raised_by', 'description', 'category',
            'status', 'resolution_comments', 'resolved_by', 'raised_at',
            'resolved_at', 'updated_at','attachment'
        ]
        read_only_fields = ['raised_by', 'resolved_by', 'raised_at', 'resolved_at', 'updated_at']
