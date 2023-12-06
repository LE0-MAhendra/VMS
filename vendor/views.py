from django.shortcuts import render
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import VendorSerializer, POSerializer, HPSerializer

# Create your views here.


@api_view(["POST", "GET"])
def vendors(request):
    if request.method == "GET":
        try:
            vendors = Vendor.objects.all()
        except Vendor.DoesNotExist:
            return Response(
                {"message": "no Vendor Exists please add a vendor"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Vendor added successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def vendor(request, pk):
    try:
        vendor = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        return Response(
            {"message": f"no Vendor Exists with this {pk} id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data
        serializer = VendorSerializer(vendor, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Vendor data for this {pk} id is updated"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        vendor.delete()
        return Response({"message": "Vendor is Deleted"}, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def purchase_orders(request):
    pass


@api_view(["GET", "PUT", "DELETE"])
def purchase_order(request, pk):
    pass


@api_view(["GET"])
def get_performance(request, pk):
    pass
