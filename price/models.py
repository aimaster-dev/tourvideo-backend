from django.db import models
from django.utils import timezone
from tourplace.models import TourPlace

# Create your models here.
class Price(models.Model):
    level = models.IntegerField()
    price = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    record_time = models.IntegerField(default=0)
    record_limit = models.IntegerField(default=0)
    tourplace = models.ForeignKey(TourPlace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pricing_tbl'