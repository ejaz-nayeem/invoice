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



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def invoice_list_create_view(request):
    
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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_list_view(request):
    
    invoices = Invoice.objects.prefetch_related(
        Prefetch('items', queryset=Item.objects.only('product_name'))
    ).order_by('-created_at')
    serializer = InvoiceListSerializer(invoices, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paid_invoice_list_view(request):
    
    invoices = Invoice.objects.filter(is_paid=True).prefetch_related(
        Prefetch('items', queryset=Item.objects.only('product_name'))
    ).order_by('-created_at')
    serializer = InvoiceListSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paid_invoice_detail_view(request, pk):
   
    try:
        invoice = Invoice.objects.prefetch_related('items').get(pk=pk, is_paid=True)
    except Invoice.DoesNotExist:
        raise Http404("Paid invoice not found")
    serializer = InvoiceDetailSerializer(invoice)
    return Response(serializer.data)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def invoice_mark_paid_view(request, pk):
   
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