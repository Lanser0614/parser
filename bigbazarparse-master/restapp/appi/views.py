from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from pars import barcode as get_barcode
from .serializers import ModelSerializer


class ProductView(APIView):
    def get(self, request, url):
        products = Products.objects.filter(olcha_url=url)
        serializer = ModelSerializer(products, many=True)
        return Response(serializer.data)

class BarCodeView(APIView):
    def get(self,request, barcode):
        return Response(get_barcode(barcode,con=None))
