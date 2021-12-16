from django.urls import path
from .views import ProductView, BarCodeView
from . import views
app_name = "products"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('products/<str:url>', views.ProductView.as_view()),
    path('barcode/<str:barcode>', views.BarCodeView.as_view())

]