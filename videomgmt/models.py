from django.db import models
from django.core.files.base import ContentFile
from user.models import User
from tourplace.models import TourPlace
from moviepy.editor import VideoFileClip
import io
from PIL import Image

# Create your models here.
class Header(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='headers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='headers/thumbnail/', null=True, blank= True)
    tourplace = models.ForeignKey(TourPlace, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.generate_thumbnail()
    
    def generate_thumbnail(self):
        clip = VideoFileClip(self.video_path.path)
        temp_thumb = io.BytesIO()
        frame = clip.get_frame(t = 1)
        image = Image.fromarray(frame)
        image.save(temp_thumb, format='JPEG')
        temp_thumb.seek(0)
        self.thumbnail.save(f"{self.pk}_thumbnail.jpg", ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        clip.close()
        self.save()

    class Meta:
        db_table = 'header_tbl'

class Footer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='footers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='footers/thumbnail/', null=True, blank= True)
    tourplace = models.ForeignKey(TourPlace, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.generate_thumbnail()
    
    def generate_thumbnail(self):
        clip = VideoFileClip(self.video_path.path)
        temp_thumb = io.BytesIO()
        frame = clip.get_frame(t = 1)
        image = Image.fromarray(frame)
        image.save(temp_thumb, format='JPEG')
        temp_thumb.seek(0)
        self.thumbnail.save(f"{self.pk}_thumbnail.jpg", ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        clip.close()
        self.save()

    class Meta:
        db_table = 'footer_tbl'

class Video(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    tourplace = models.ForeignKey(TourPlace, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='videos/')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='videos/thumbnail/', null=True, blank= True)

    class Meta:
        db_table = 'video_tbl'