from rest_framework import serializers
from .models import Invoice, Item
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['product_name']

class ItemDetailSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'product_name', 'quantity', 'amount', 'total_amount']
        read_only_fields = ['id', 'total_amount']

class InvoiceListSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'status', 'sub_total', 'created_at', 'items']
        read_only_fields = ['id', 'created_at', 'sub_total']

    def get_status(self, obj):
        return "Paid" if obj.is_paid else "Pending"

class InvoiceDetailSerializer(serializers.ModelSerializer):
    items = ItemDetailSerializer(many=True)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'customer_phone', 'created_at', 'is_paid', 'status', 'sub_total', 'items']
        read_only_fields = ['id', 'created_at', 'sub_total']

    def get_status(self, obj):
        return "Paid" if obj.is_paid else "Pending"

    def validate_customer_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def create(self, validated_data):
        logger.info("Validated data: %s", validated_data)
        items_data = validated_data.pop('items', [])
        logger.info("Items data: %s", items_data)
        if not items_data:
            raise serializers.ValidationError({"items": "An invoice must have at least one item."})
        with transaction.atomic():
            invoice = Invoice.objects.create(**validated_data)
            for item_data in items_data:
                logger.info("Creating item: %s", item_data)
                Item.objects.create(invoice=invoice, **item_data)
            return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_phone = validated_data.get('customer_phone', instance.customer_phone)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()

        if items_data is not None:
            if not items_data and not instance.items.exists():
                raise serializers.ValidationError({"items": "An invoice cannot have all its items removed."})
            elif not items_data and instance.items.exists():
                raise serializers.ValidationError({"items": "Cannot remove all items from an existing invoice."})

            existing_items_map = {item.id: item for item in instance.items.all()}
            updated_item_ids = []

            for item_data in items_data:
                item_id = item_data.get('id')
                if item_id in existing_items_map:
                    item = existing_items_map.pop(item_id)
                    for attr, value in item_data.items():
                        setattr(item, attr, value)
                    item.save()
                    updated_item_ids.append(item_id)
                else:
                    Item.objects.create(invoice=instance, **item_data)

            items_to_delete = existing_items_map.values()
            if items_to_delete:
                for item in items_to_delete:
                    item.delete()

        return instance

class InvoicePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['is_paid']

    def update(self, instance, validated_data):
        if validated_data.get('is_paid') is False:
            raise serializers.ValidationError({"is_paid": "Cannot unmark an invoice as paid via this endpoint."})
        instance.is_paid = True
        instance.save()
        return instance