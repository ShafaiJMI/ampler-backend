from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import AnalyticsSerializer
from .models import InvoiceAnalytics

@api_view(['GET'])
@csrf_exempt
def Analytics(request):
    if request.method == 'GET':
        stats = InvoiceAnalytics.objects.all()
        total_profit = sum(stat.profit for stat in stats)
        total_investment = sum(stat.landed_cost for stat in stats)
        total_sale = sum(stat.sale for stat in stats)
        total_trips = InvoiceAnalytics.objects.count()
        data = {
            'total_profit':total_profit,
            'total_investment':total_investment,
            'total_sale':total_sale,
            'total_trips':total_trips,
            'stats':stats
        }
        serializer = AnalyticsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
