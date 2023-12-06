from django.shortcuts import render
from .models import Vendor, PurchaseOrder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PESerializer, VendorSerializer, POSerializer, HPSerializer

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
    if request.method == "GET":
        try:
            pos = PurchaseOrder.objects.all()
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"message": "no POS Exists please add a Purchase order"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = POSerializer(pos, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        vendor_id = data.get("vendor")

        # Check if the vendor ID is valid
        try:
            checker = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response(
                {"message": f"Vendor with ID {vendor_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if checker:
            serializer = POSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Purchase Order added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def purchase_order(request, pk):
    try:
        pos = PurchaseOrder.objects.get(id=pk)
    except PurchaseOrder.DoesNotExist:
        return Response(
            {"message": "no POS Exists please add a Purchase order"},
            status=status.HTTP_404_NOT_FOUND,
        )
    # if checker and pos:
    if request.method == "GET":
        serializer = POSerializer(pos)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = request.data
        vendor_id = data.get("vendor")

        # Check if the vendor ID is valid
        try:
            checker = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response(
                {"message": f"no Vendor Exists with this {vendor_id} id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        serializer = POSerializer(pos, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Purchse order data for this {pk} id is updated"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        pos.delete()
        return Response(
            {"message": "Purchase order is Deleted"}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def get_performance(request, pk):
    try:
        vendor = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        return Response(
            {"message": f"no Vendor Exists with this {pk} id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = PESerializer(vendor)
        return Response(serializer.data)
