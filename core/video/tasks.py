from .services import ConvertVideo
from celery_app import app
from video.models import Video, VideoForStreem
from tv_shows.models import ShowsItem

from django.db.utils import DataError


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
                    _success = False
                    for item in result:
                        try:
                            item.save()
                            _success = True
                        except DataError:
                            print(type(item))
                            print(item.__dict__)
                            print(f"add item error -> ITEM: {item} | ERROR: {DataError}")
                        except Exception as e:
                            print(f"Unknown error: {e}")

                    if _success:
                        ShowsItem.objects.filter(video_id=video.pk).update(status='p')
                        Video.objects.filter(pk=video.pk, status='p').update(status='c')

    else:
        print('No render objects')

