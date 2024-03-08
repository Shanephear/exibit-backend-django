from django.urls import path
from .views import upload_video,convert_video,get_all_video,delete_video
urlpatterns = [

    path('upload', upload_video, name='upload_video'),
    path('convert/<uuid:id>',convert_video , name='convert_video'),
    path('getall', get_all_video, name='get_all'),
    path('delete/<uuid:id>',delete_video , name='delete_video')
]
