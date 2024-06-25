from django.db import models
from django.conf import settings

# Create your models here.
class Camera(models.Model):
    camera_name = models.CharField(max_length=255, blank=True, default='')
    isp = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera_ip = models.CharField(max_length=255)
    camera_port = models.CharField(max_length=255)
    camera_user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'camera_tbl'
        constraints = [
            models.UniqueConstraint(fields=['camera_ip', 'camera_port'], name='unique_camera_ip_port')
        ]