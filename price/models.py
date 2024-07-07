from django.db import models
from django.utils import timezone

# Create your models here.
class Price(models.Model):
    level = models.IntegerField()
    title = models.CharField(max_length=255)
    record_time = models.IntegerField(default=0)
    record_limit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pricing_tbl'