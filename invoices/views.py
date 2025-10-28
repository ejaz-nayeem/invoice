from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Invoice, Item
from .serializers import (
    InvoiceListSerializer,
    InvoiceDetailSerializer,
    InvoicePaymentSerializer
)
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

# --- General Invoice Management Views ---

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def invoice_list_create_view(request):
    """
    Lists all invoices (GET) or creates a new invoice (POST).
    - GET: Returns simplified invoice data, ordered by creation date.
    - POST: Requires full details (customer, items).
    """
    if request.method == 'GET':
        invoices = Invoice.objects.prefetch_related(
            Prefetch('items', queryset=Item.objects.only('product_name'))
        ).order_by('-created_at')
        serializer = InvoiceListSerializer(invoices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InvoiceDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def invoice_retrieve_update_destroy_view(request, pk):
    """
    Retrieves, updates, or deletes a single invoice by its primary key (ID).
    - GET: Returns full details, including nested items.
    - PUT: Updates the invoice (requires full data).
    - DELETE: Deletes the invoice.
    """
    try:
        invoice = Invoice.objects.prefetch_related('items').get(pk=pk)
    except Invoice.DoesNotExist:
        raise Http404("Invoice not found")

    if request.method == 'GET':
        serializer = InvoiceDetailSerializer(invoice)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InvoiceDetailSerializer(invoice, data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                instance.full_clean(exclude=['id'])
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- "Transaction" Function (Listing all invoices) ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list_view(request):
    """
    Lists all invoices as 'transactions', ordered by creation date.
    Returns simplified invoice data.
    """
    invoices = Invoice.objects.prefetch_related(
        Prefetch('items', queryset=Item.objects.only('product_name'))
    ).order_by('-created_at')
    serializer = InvoiceListSerializer(invoices, many=True)
    return Response(serializer.data)

# --- "Payment" Function (Listing and viewing Paid Invoices) ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paid_invoice_list_view(request):
    """
    Lists all invoices that have been marked as 'Paid', ordered by creation date.
    Returns simplified invoice data.
    """
    invoices = Invoice.objects.filter(is_paid=True).prefetch_related(
        Prefetch('items', queryset=Item.objects.only('product_name'))
    ).order_by('-created_at')
    serializer = InvoiceListSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paid_invoice_detail_view(request, pk):
    """
    Retrieves full details of a single invoice, only if it is marked as 'Paid'.
    """
    try:
        invoice = Invoice.objects.prefetch_related('items').get(pk=pk, is_paid=True)
    except Invoice.DoesNotExist:
        raise Http404("Paid invoice not found")
    serializer = InvoiceDetailSerializer(invoice)
    return Response(serializer.data)

# --- Invoice Payment View ---

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def invoice_mark_paid_view(request, pk):
    """
    Marks an existing invoice as 'Paid'.
    Requires sending {"is_paid": true}. Cannot unmark as paid through this endpoint.
    """
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        raise Http404("Invoice not found")

    serializer = InvoicePaymentSerializer(invoice, data=request.data, partial=True)
    if serializer.is_valid():
        if serializer.validated_data.get('is_paid', False):
            serializer.save()
            return Response(serializer.data)
        return Response({"detail": "Cannot unmark an invoice as unpaid."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)