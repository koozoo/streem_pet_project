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
                                         convert_to='mp4',
                                         origin_video_object=video)
            if render_object:
                result = render_object.start()
                print(result)
                if result:
                    for item in result:
                        add_item = VideoForStreem(
                            title=item.title,
                            type=item.type,
                            resolution=item.resolution,
                            duration_in_seconds=item.duration_in_seconds,
                            video=item.video
                        )
                        add_item.origin_video = item.origin_video
                        add_item.save()
    else:
        print('No render objects')


@app.task
def add_video_for_stream(origin_video_id: int,
                         type_: str,
                         title: str,
                         resolution: str,
                         duration: int,
                         video_path: str):

    new_video = VideoForStreem(title=title,
                               type=type_,
                               origin_video=origin_video_id,
                               resolution=resolution,
                               duration_in_seconds=duration,
                               video=video_path,
                               status='n')
    new_video.save()
