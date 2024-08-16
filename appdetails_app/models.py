from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.name}_{instance.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('media/icons', filename)

# Create your models here.
class AppCategory(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='categories_created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class AppSubCategory(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(AppCategory, related_name='category', on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, related_name='sub_categories_created_by', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} ({self.category.name})"

class App(models.Model):
    name = models.CharField(max_length=255)
    download_link = models.URLField(max_length=255)
    icon = models.ImageField(upload_to=upload_to)
    category = models.ForeignKey(AppCategory, related_name='app_category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(AppCategory, related_name='app_sub_category', on_delete=models.CASCADE)
    points = models.IntegerField()
    created_by = models.ForeignKey(User, related_name='apps_created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='apps_updated_by', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.icon:
            self.icon.delete()
        super().delete(*args, **kwargs)
