from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class HPSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"


class PESerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        )


class AcknowledgeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["acknowledgment_date"]
