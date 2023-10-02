from django.db import models

# Create your models here.
class Parkings(models.Model):
    plate_number = models.CharField(max_length=10)
    vehicle_type = models.IntegerField() # 1 indicating 2-wheeler and 2 indicating 4-wheeler
    parking_spot = models.IntegerField()
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True)