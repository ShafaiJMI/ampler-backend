# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice, Buyer, Seller
from .serializers import InvoiceSerializer, InvoiceListSerializer, BuyerSerializer, SellerSerializer
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()
            return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def invoices(request):
    if request.method == 'GET':
        invoice_list = Invoice.objects.all()
        serializer = InvoiceListSerializer(invoice_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def Buyers(request):
    if request.method == 'GET':
        buyer_list = Buyer.objects.all()
        serializer = BuyerSerializer(buyer_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def Sellers(request):
    if request.method == 'GET':
        sellers_list = Seller.objects.all()
        serializer = SellerSerializer(sellers_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)