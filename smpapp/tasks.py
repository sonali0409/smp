from celery import shared_task
import time
from PIL import Image
import os
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings

@shared_task
def compress_recipe_image(image_path):
    full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    
    try:
        original_file_size = os.path.getsize(full_path)  # in bytes
        original_file_size_kb = original_file_size / 1024
        original_file_size_mb = original_file_size_kb / 1024
        img = Image.open(full_path)
        width, height = img.size
        print(f"Before Original image size: {width}x{height}px")
        print(f"Before Original file size: {original_file_size_kb:.2f} KB ({original_file_size_mb:.2f} MB)")
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.thumbnail((1024, 1024))
        img.save(full_path, format='JPEG', quality=70)
        width, height = img.size
        print(f"After Original image size: {width}x{height}px")
        print(f"After Original file size: {original_file_size_kb:.2f} KB ({original_file_size_mb:.2f} MB)")

        return f"{image_path} compressed successfully."
    
    except Exception as e:
        return f"Error compressing {image_path}: {str(e)}"
    
@shared_task
def send_daily_email():
    today = datetime.today().weekday()  

    if today in [5, 6]:  
        return "Skipped weekend."

    send_mail(
        subject='Daily Recipe Reminder',
        message='Good morning! Check out today’s recipes!',
        from_email='sv026068@gmail.com',
        recipient_list=['rakesh.rocky.3108@gmail.com'],
        fail_silently=False,
    )
    return "Email sent successfully!"
    
@shared_task
def sample_task():
    print("sone se pahle")
    time.sleep(5)
    print("sone ke baad")
    return "Task completed!"
