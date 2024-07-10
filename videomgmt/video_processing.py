import os
import sys
import subprocess
import hashlib
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
from django.core.wsgi import get_wsgi_application
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
application = get_wsgi_application()

import django
django.setup()
from django.conf import settings
from videomgmt.models import Video, Header, Footer
from user.models import User

def generate_unique_filename(original_filename, username):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hash_input = f"{original_filename}{username}{current_datetime}".encode('utf-8')
    hash_object = hashlib.sha256(hash_input)
    hash_hex = hash_object.hexdigest()[:16]  # Get the first 16 characters of the hash
    name, _ = os.path.splitext(original_filename)
    return f"{name}_{hash_hex}.mp4"

def convert_webm_to_mp4(webm_path, mp4_path):
    command = [
        'ffmpeg', '-i', webm_path, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', '-movflags', 'faststart', mp4_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ValueError(f"Error converting webm to mp4: {result.stderr.decode('utf-8')}")

def send_notification_email(user, video_url):
    subject = 'Your Video Has Been Processed'
    message = render_to_string('video_success_email.html', {
        'user': user,
        'video_url': video_url,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()

def process_video(video_id, user_id, original_filename):
    video = Video.objects.get(pk=video_id)
    user = User.objects.get(pk=user_id)

    header = Header.objects.filter(user=user).order_by('?').first()
    footer = Footer.objects.filter(user=user).order_by('?').first()

    if not header or not footer:
        video.status = False
        video.save()
        return

    temp_video_path = os.path.join(settings.MEDIA_ROOT, f'temp_uploaded_video_{user.username}.webm')
    converted_video_path = os.path.join(settings.MEDIA_ROOT, f'converted_video_{user.username}.mp4')

    convert_webm_to_mp4(temp_video_path, converted_video_path)

    try:
        header_clip = VideoFileClip(header.video_path.path)
        uploaded_clip = VideoFileClip(converted_video_path)
        footer_clip = VideoFileClip(footer.video_path.path)
        final_clip = concatenate_videoclips([header_clip, uploaded_clip, footer_clip], method="compose")
        final_video_name = generate_unique_filename(original_filename, user.username)
        final_video_relative_path = os.path.join('videos', final_video_name)
        final_video_absolute_path = os.path.join(settings.MEDIA_ROOT, final_video_relative_path)
        os.makedirs(os.path.dirname(final_video_absolute_path), exist_ok=True)
        final_clip.write_videofile(final_video_absolute_path, codec='libx264')

        video.video_path = final_video_relative_path
        video.status = True
        video.save()
        video_url = "http://localhost:8000/media/" + final_video_relative_path
        send_notification_email(user, video_url)
        
    finally:
        header_clip.reader.close()
        footer_clip.reader.close()
        uploaded_clip.reader.close()
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(converted_video_path):
            os.remove(converted_video_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python video_processing.py <video_id> <user_id> <original_filename>")
        sys.exit(1)
    
    video_id = int(sys.argv[1])
    user_id = int(sys.argv[2])
    original_filename = sys.argv[3]

    process_video(video_id, user_id, original_filename)
