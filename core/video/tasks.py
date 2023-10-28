from celery import shared_task
from .services import ConvertVideo
from celery_app import app
from video.models import Video


@shared_task
def task_convert_to_mp4(input_file):
    converter = ConvertVideo(video_path=input_file, convert_to='mp4')
    result = converter.start()
    print(result)


@app.task
def start_render_video():
    print('start')
    # VideoForStreem
    # all_video_to_render = Video.objects.filter(status='n')
    # print(all_video_to_render)
    # new_video = Video(title=title,
    #                   type='m',
    #                   video='video/origin/2023/10/28/One.Piece.S01E03.rus.LostFilm.TV.avi',
    #                   status='n')
    # new_video.save()
    return 'test'
