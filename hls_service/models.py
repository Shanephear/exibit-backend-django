from django.db import models
import os
import uuid


def video_file_upload_path(instance, filename):
    return os.path.join('videos', str(instance.id), filename)

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(null=True)
    video_file = models.FileField(upload_to=video_file_upload_path)
    hls_file = models.TextField(null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    type = models.CharField(max_length=255,null=True)
    size = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def get_values(self):
        return {
            'id': self.id,
            'title' : self.title,
            'hls_file': self.hls_file,
            'duration': self.duration,
            'type': self.type,
            'size': self.size,
            'timestamp': self.timestamp
        }
    def get_id(self):
        return self.id

