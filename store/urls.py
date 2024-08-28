# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('user-items/', views.user_purchased_items, name='user_purchased_items'),
    path('purchase/', views.purchase_item, name='purchase_item'),  # New URL for purchasing an item
]
