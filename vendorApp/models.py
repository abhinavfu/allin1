from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from .serializers import *
from datetime import datetime
from django.db.models import Avg, Count, F, Q


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Creates an authentication token for the User.
    """
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField(default="")
    address = models.TextField(default="")
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        unique_together = ('vendor_code',)

    def __str__(self):
        return self.name

# status = ('pending', 'completed', 'canceled')
class Purchase_Order(models.Model):
    po_number = models.CharField(max_length=100,unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(default="pending",max_length=100)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('po_number',)

    def __str__(self):
        return self.po_number


class  Historical_Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


@receiver(post_save, sender=Purchase_Order)
def calculate_vendor_performance(sender, instance, **kwargs):
    """
    It calculate the vendor's performance metrics such as 

        - on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
        - quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
        - average_response_time: FloatField - Average time taken to acknowledge purchase orders.
        - fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

    It also create and update Historical Performance of Vendor.

    Parmeters:
        - sender : object for the Purchase Order Model
        - instance : represents the instance of the class Purchase Order.
        - kwargs (dict): Additional keyword arguments.

    """
    print("Purchase Order triggered.")
    try:
        # single Purchase Order which is updated or been acknowledged
        selected_PO = Purchase_Order.objects.get(id=instance.id)
        # Selecting vendor for the same Purchase order's vendor
        vendor = Vendor.objects.get(id=selected_PO.vendor.id)
        # list of Purchase order with selected vendor
        obj_PO = Purchase_Order.objects.filter(vendor=vendor)
        try:
            on_time_delivery_rate = []
            quality_rating_avg = []
            average_response_time = []
            fulfillment_rate = []
                
            for i in obj_PO:
                if i.status == "completed":
                    # on_time_delivery_rate
                    if i.delivery_date > i.acknowledgment_date:
                        # True = 1
                        on_time_delivery_rate.append(1)
                    else:
                        # False = 0
                        on_time_delivery_rate.append(0)

                    # quality_rating
                    if i.quality_rating != None:
                        quality_rating_avg.append(i.quality_rating)

                    # average_response_time
                    avg_time = i.acknowledgment_date - i.issue_date 
                    # avg_time returns in days (eg- 02 days 00:00)
                    average_response_time.append(avg_time.days)
                    
                    # fulfillment_rate
                    fulfillment_rate.append(1) # true
                elif i.status == "cancelled" or i.status == "pending":
                    fulfillment_rate.append(0) # false

            # checking if the value is not null or zero, if found zero or null then it raises ZERO DIVISION ERROR
            try:
                on_time_delivery_rate = round(sum(on_time_delivery_rate)/len(on_time_delivery_rate)*100,2)
            except ZeroDivisionError:
                on_time_delivery_rate = 0
            try:
                quality_rating_avg = round(sum(quality_rating_avg)/len(quality_rating_avg),2)
            except ZeroDivisionError:
                quality_rating_avg = 0
            try:
                average_response_time = round(sum(average_response_time)/len(average_response_time),2)
            except ZeroDivisionError:
                average_response_time = 0
            try:
                fulfillment_rate = round(sum(fulfillment_rate)/len(fulfillment_rate)*100,2)
            except ZeroDivisionError:
                fulfillment_rate = 0

            # --------------------------------------------------------------------------------------
            # Additional (Checking Time)
            # --------------------------------------------------------------------------------------
            # # Method 1 for fast Time complexity
            # def time_cal():
            #     start = datetime.now() # start time

            #     on_time_delivery_rate = []
            #     quality_rating_avg = []
            #     average_response_time = []
            #     fulfillment_rate = []
                    
            #     for i in obj_PO:
            #         if i.status == "completed":
            #             # on_time_delivery_rate
            #             if i.delivery_date > i.acknowledgment_date:
            #                 # True = 1
            #                 on_time_delivery_rate.append(1)
            #             else:
            #                 # False = 0
            #                 on_time_delivery_rate.append(0)

            #             # quality_rating
            #             if i.quality_rating != None:
            #                 quality_rating_avg.append(i.quality_rating)

            #             # average_response_time
            #             avg_time = i.acknowledgment_date - i.issue_date 
            #             # avg_time returns in days (eg- 02 days 00:00)
            #             average_response_time.append(avg_time.days)
                        
            #             # fulfillment_rate
            #             fulfillment_rate.append(1) # true
            #         elif i.status == "cancelled" or i.status == "pending":
            #             fulfillment_rate.append(0) # false

            #     # checking if the value is not null or zero, if found zero or null then it raises ZERO DIVISION ERROR
            #     try:
            #         on_time_delivery_rate = round(sum(on_time_delivery_rate)/len(on_time_delivery_rate)*100,2)
            #     except ZeroDivisionError:
            #         on_time_delivery_rate = 0
            #     try:
            #         quality_rating_avg = round(sum(quality_rating_avg)/len(quality_rating_avg),2)
            #     except ZeroDivisionError:
            #         quality_rating_avg = 0
            #     try:
            #         average_response_time = round(sum(average_response_time)/len(average_response_time),2)
            #     except ZeroDivisionError:
            #         average_response_time = 0
            #     try:
            #         fulfillment_rate = round(sum(fulfillment_rate)/len(fulfillment_rate)*100,2)
            #     except ZeroDivisionError:
            #         fulfillment_rate = 0
            #     end = datetime.now() # end time
            #     total_time = end - start
            #     x= {
            #         'on_time_delivery_rate' : on_time_delivery_rate,
            #         'quality_rating_avg' : quality_rating_avg,
            #         'average_response_time' : average_response_time,
            #         'fulfillment_rate' : fulfillment_rate,
            #         'total_time' : total_time
            #     }
            #     return x

            # print("Time check :",time_cal())
            # print("------------------------------------------------------------------")
            # # Method 2 for fast Time complexity
            # def time_cal2():
            #     start = datetime.now() # start time

            #     obj_PO_completed = obj_PO.filter(status='completed')
            #     obj_PO_completed_count = obj_PO_completed.count()
            #     #  on-time delivery rate
            #     on_time_pos = obj_PO_completed.filter(delivery_date__lte=F('acknowledgment_date'))
            #     on_time_delivery_rate = (on_time_pos.count() / obj_PO_completed_count) * 100 if obj_PO_completed_count > 0 else 0
        
            #     #  quality rating average
            #     completed_orders = obj_PO.filter(status='completed', quality_rating__isnull=False)
            #     completed_orders_count = completed_orders.count()
            #     # 1) slow
            #     # quality_rating_sum = sum(order.quality_rating for order in completed_orders)
            #     # quality_rating_avg = quality_rating_sum / completed_orders_count if completed_orders_count > 0 else 0
            #     # 2) fast
            #     quality_rating_avg = completed_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] if completed_orders_count > 0 else 0

            #     #  average response time
            #     # 1) slow
            #     # total_time = sum((p.acknowledgment_date - p.issue_date).total_seconds() for p in obj_PO_completed)
            #     # average_response_time = total_time / obj_PO_completed_count if obj_PO_completed_count > 0 else 0   
            #     # 2) fast
            #     if obj_PO_completed_count > 0:
            #         response_times = obj_PO_completed.annotate(response_time=F('acknowledgment_date') - F('issue_date'))
            #         average_response_time = response_times.aggregate(average_response_time=Avg('response_time'))['average_response_time']
            #         average_response_time = average_response_time.days
            #     else:
            #         average_response_time = 0

            #     #  fulfilment rate
            #     # fulfilled_pos = obj_PO.exclude(status='completed', issue_date__isnull=False)
            #     fulfilled_pos = obj_PO.filter(status='completed', issue_date__isnull=False)
            #     fulfillment_rate = (fulfilled_pos.count() / obj_PO.count()) * 100 if obj_PO.count() > 0 else 0
                
            #     end = datetime.now() # end time
            #     total_time = end - start
            #     x= {
            #         'on_time_delivery_rate' : on_time_delivery_rate,
            #         'quality_rating_avg' : quality_rating_avg,
            #         'average_response_time' : average_response_time,
            #         'fulfillment_rate' : fulfillment_rate,
            #         'total_time' : total_time
            #     }
            #     return x
            
            # print("Time check :",time_cal2()) 
            # print("------------------------------------------------------------------")
            # 1st time
            # method 1 'total_time': datetime.timedelta(microseconds=1992)
            # method 2 'total_time': datetime.timedelta(microseconds=12064)

            # 2nd time
            # method 1 'total_time': datetime.timedelta(microseconds=2819)
            # method 2 'total_time': datetime.timedelta(microseconds=17884)
            
            # Result (8 records only) : method 2 is 6x slower than the method 1 
            # --------------------------------------------------------------------------------------
            # (End Checking Time)
            # --------------------------------------------------------------------------------------

            # If calculations is good, then update the Vendor model or else throw error.
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.quality_rating_avg = quality_rating_avg
            vendor.average_response_time = average_response_time
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()
            
            try:
                # If vendor matched with the Historical Performance model, then update the selected model
                hist_perf = Historical_Performance.objects.get(vendor=vendor.id)
                hist_perf.vendor = Vendor.objects.get(id=vendor.id) 
                hist_perf.on_time_delivery_rate = on_time_delivery_rate
                hist_perf.quality_rating_avg = quality_rating_avg
                hist_perf.average_response_time = average_response_time
                hist_perf.fulfillment_rate = fulfillment_rate
                hist_perf.save()
   
            except Exception as e:
                print("ERROR :",str(e))
                # if not, then create a new one
                hist_perf = Historical_Performance(
                    vendor = vendor,
                    on_time_delivery_rate = 0,
                    quality_rating_avg = 0,
                    average_response_time = 0,
                    fulfillment_rate = 0
                )
                hist_perf.save()
        except Exception as e:
            # If something gones wrong, it will throw an error.
            print("ERROR :",str(e))
    except Exception as e:
        # If something gones wrong, it will throw an error.
        print("ERROR :",str(e))
