import uuid

from celery import shared_task
from .services import ConvertVideo
from celery_app import app
from video.models import Video, VideoForStreem


@app.task
def start_render_video():
    all_video_to_render = Video.objects.filter(status='n')

    if all_video_to_render:
        Video.objects.filter(status='n').update(status='p')

        for video in all_video_to_render:
            render_object = ConvertVideo(video_path=video.video,
                                         convert_to='m3u8',
                                         origin_video_object=video)
            if render_object:
                result = render_object.start()
                print(f"result: {result}")

                if result:
                    for item in result:
                        add_item = item
                        add_item.save()
    else:
        print('No render objects')

