from django.urls import path
from . import views

urlpatterns = [
    path('quote/', views.quote, name="quote"),
    path('wallet/', views.wallet, name="wallet"),
    path('', views.order_stock, name="order_stock"),
    path('sell/<stock_id>', views.sell, name="sell"),
    path('deposit/', views.deposit, name="deposit"),
    path('sellOrder/', views.sell_stock, name="sell_stock" ),
]