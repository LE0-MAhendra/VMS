from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timesince import timesince
from django.utils import timezone


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
    ]
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f"Purchase Order {self.po_number}"

    def save(self, *args, **kwargs):
        # Save changes to the PurchaseOrder
        super().save(*args, **kwargs)
        pos_completed = PurchaseOrder.objects.filter(
            vendor=self.vendor, status=PurchaseOrder.COMPLETED
        )
        pos_completed_count = pos_completed.count()
        # Calculating the On-Time Delivery Rate upon completion
        if self.status == PurchaseOrder.COMPLETED:
            pos_on_time_delivered = pos_completed.filter(
                # __lte refers to less than or equal to
                delivery_date__lte=self.delivery_date
            ).count()
            if pos_completed_count > 0:
                self.vendor.on_time_delivery_rate = (
                    pos_on_time_delivered / pos_completed_count
                ) * 100
            else:
                self.vendor.on_time_delivery_rate = 0
        # Updating the  Quality Rating Average upon completion
        if self.quality_rating is not None and pos_completed is not None:
            if pos_completed_count > 0:
                self.vendor.quality_rating_avg = (
                    sum(pos_completed.values_list("quality_rating", flat=True))
                    / pos_completed_count
                )
            else:
                self.vendor.quality_rating_avg = 0
        # Calculating the  Average Response Time upon acknowledgment
        if self.acknowledgment_date is not None:
            pos_all_acknowledged = PurchaseOrder.objects.filter(
                vendor=self.vendor, acknowledgment_date__isnull=False
            )
            pos_all_acknowledged_count = pos_all_acknowledged.count()
            # Calculate the sum of time differences
            acknowledgment_dates = pos_all_acknowledged.values_list(
                "acknowledgment_date", flat=True
            )
            issue_dates = pos_all_acknowledged.values_list("issue_date", flat=True)
            time_differences = [
                (ack_date - issue_date).total_seconds()
                for ack_date, issue_date in zip(acknowledgment_dates, issue_dates)
            ]
            # Calculate the average response time
            self.vendor.average_response_time = (
                sum(time_differences) / pos_all_acknowledged_count
                if pos_all_acknowledged_count > 0
                else 0
            )

        # Calculating the  Fulfilment Rate upon any change in PO status
        all_pos = PurchaseOrder.objects.filter(vendor=self.vendor)
        fulfilled_pos = all_pos.filter(
            status=PurchaseOrder.COMPLETED, quality_rating__isnull=False
        )
        self.vendor.fulfillment_rate = (
            (fulfilled_pos.count() / all_pos.count()) * 100
            if all_pos.count() > 0
            else 0
        )
        # save the changes into vendor
        self.vendor.save()
        update_historical_performance(self)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        time_since = timesince(self.date, timezone.now())
        return f"{self.vendor.name} - {time_since} ago"


def update_historical_performance(instance):
    if instance.status == PurchaseOrder.COMPLETED:
        instance.vendor.refresh_from_db()
        HistoricalPerformance.objects.create(
            vendor=instance.vendor,
            on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
            quality_rating_avg=instance.vendor.quality_rating_avg,
            average_response_time=instance.vendor.average_response_time,
            fulfillment_rate=instance.vendor.fulfillment_rate,
        )
