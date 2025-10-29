from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invoices.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('create_invoice/', TemplateView.as_view(template_name='create_invoice.html'), name='create'),
    path('invoice_list/', TemplateView.as_view(template_name='invoices.html'), name='invoices'),
    #path('paid_invoices/', TemplateView.as_view(template_name='paid_invoices.html'), name='paid_invoices'),
    path('paid-invoices-list/', TemplateView.as_view(template_name='paid_invoices.html'), name='paid_invoices_html'),
]


