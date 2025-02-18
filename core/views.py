# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice, Buyer, Seller
from .serializers import InvoiceSerializer, InvoiceListSerializer, BuyerSerializer, SellerSerializer

@api_view(['POST'])
@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()
            return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@csrf_exempt
def delete_invoice(request,inv):
    if request.method == 'DELETE':
        invoice = Invoice.objects.get(invoice_number=inv)
        if invoice:
            invoice.delete()
        return Response({"message": "Deleted successfully"},tatus=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

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
def invoicesdetail(request,inv):
    if request.method == 'GET':
        invoice_list = Invoice.objects.get(invoice_number=inv)
        serializer = InvoiceSerializer(invoice_list, many=False)
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