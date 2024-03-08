from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Video
import os
import ffmpeg
import time
import shutil
# Create your views here.
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')
        duration = request.POST.get('duration')
        video = Video.objects.create(
            title = title,
            video_file= video_file,
            duration = duration,
            size = video_file.size, 
            type =video_file.content_type
        )
        video.save()
        id = video.get_id()
        time.sleep(0.5)
        return JsonResponse({'id':id},safe=False)

@csrf_exempt
def convert_video(request, id):
    if request.method == 'POST':
        try:
            video = get_object_or_404(Video, id=id)
            input_file_path = os.path.join('media', str(video.video_file))
            input_stream = ffmpeg.input(input_file_path)
            resolutions = [
            {
                'resolution': '2560x1440',
                'videoBitrate': '8000k',
                'audioBitrate': '256k',
                'bandwidth': '8256000'
            },
            {
                'resolution': '1920x1080',
                'videoBitrate': '5000k',
                'audioBitrate': '256k',
                'bandwidth': '5256000'
            },
            {
                'resolution': '1280x720',
                'videoBitrate': '2500k',
                'audioBitrate': '192k',
                'bandwidth': '2692000'
            },
            {
                'resolution': '854x480',
                'videoBitrate': '1000k',
                'audioBitrate': '128k',
                'bandwidth': '1128000'
            }
            ]
            for i in resolutions:
                resolution = i['resolution']
                output_file_path = os.path.join('media', 'videos',str(video.id),'hls_output', f'{video.id}_{resolution}_output.m3u8')
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                output_stream = ffmpeg.output(input_stream, output_file_path,format='hls',vcodec='h264',video_bitrate=i['videoBitrate'],
                acodec='aac',
                audio_bitrate=i['audioBitrate'],
                vf=f'scale={resolution}',
                hls_time=10,
                hls_list_size=0
                )
                ffmpeg.run(output_stream)
                i['output'] = f'{video.id}_{resolution}_output.m3u8'
            master_m3u8_path = os.path.join('media', 'videos',str(video.id),'hls_output', f'{video.id}_master.m3u8')
            os.makedirs(os.path.dirname(master_m3u8_path), exist_ok=True)
            with open(master_m3u8_path, 'w') as master_m3u8_file:
                master_m3u8_file.write("#EXTM3U\n#EXT-X-VERSION:3\n")
                for i in resolutions:
                    master_m3u8_file.write(f"#EXT-X-STREAM-INF:BANDWIDTH={i['bandwidth']},RESOLUTION={i['resolution']}\n{i['output']}\n")
            video.hls_file = master_m3u8_path[6:]
            video.save()
        except:
            return HttpResponse(status=200)
        return HttpResponse(status=200)

@csrf_exempt
def get_all_video(request):
    if request.method == 'GET':
        result = Video.objects.filter(hls_file__isnull=False).order_by("-timestamp").all()
        video_details = [i.get_values() for i in result]
        time.sleep(0.5)
        return JsonResponse(video_details, safe=False)

@csrf_exempt
def delete_video(request, id):
    if request.method == 'DELETE':
        try:
            shutil.rmtree(os.path.join('media','videos',str(id)))
            videoInfo = Video.objects.get(id=id)
            videoInfo.delete()
        except Exception:
            pass
        time.sleep(0.5)
        return HttpResponse(status=204)