from django.urls import path, include
from .views import products_view, products_detail_view, category_list

app_name = 'shop'

urlpatterns = [

    path('', products_view, name='products'),
    path('search/<slug:slug>/', category_list, name='category_list'),
    path('<slug:slug>/', products_detail_view, name='product_detail'),



]
