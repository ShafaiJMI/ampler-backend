from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Token obtain (login)
    TokenRefreshView,     # Token refresh
)
from . import views

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-invoice/', views.create_invoice, name='create_invoice'),
    path('invoices/', views.invoices, name='invoices'),
    path('view-invoice/<inv>/', views.invoicesdetail, name='view-invoice'),
    path('analytics/', views.Analytics, name='analytics'),
    path('buyers/', views.Buyers, name='buyers'),
    path('sellers/', views.Sellers, name='sellers'),
    
]
"""
    path('invoices/', InvoiceViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('invoices/<int:pk>/', InvoiceViewSet.as_view({'get': 'retrieve'})),
"""