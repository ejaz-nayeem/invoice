from django.urls import path
from .views import (
    invoice_list_create_view,
    invoice_retrieve_update_destroy_view,
    transaction_list_view,
    paid_invoice_list_view,
    paid_invoice_detail_view,
    invoice_mark_paid_view
)

urlpatterns = [
    path('invoices/', invoice_list_create_view, name='invoice-list-create'),
    path('invoices/<int:pk>/', invoice_retrieve_update_destroy_view, name='invoice-detail'),
    path('transactions/', transaction_list_view, name='transaction-list'),
    path('paid-invoices/', paid_invoice_list_view, name='paid-invoice-list'),
    path('paid-invoices/<int:pk>/', paid_invoice_detail_view, name='paid-invoice-detail'),
    path('invoices/<int:pk>/pay/', invoice_mark_paid_view, name='invoice-mark-paid'),
]