from django.utils import timezone
import os
from django.db import models
from appdetails_app.models import App
from django.contrib.auth.models import User

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"task__screenshot_{instance.id}_{instance.app.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('media/screenshots', filename)

# Create your models here.
class TaskDetails(models.Model):
    screenshot = models.ImageField(upload_to=upload_to)
    app = models.ForeignKey(App, related_name='app', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='tasks_created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def delete(self, *args, **kwargs):
        if self.screenshot:
            self.screenshot.delete()
        super().delete(*args, **kwargs)