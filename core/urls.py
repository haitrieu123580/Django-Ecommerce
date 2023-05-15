from django.urls import path
# from .views import (
#     products,
#     home,
#     checkout)
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('checkout', views.checkout, name='checkout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart')
]
