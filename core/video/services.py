import datetime
import subprocess
import ffmpeg

from pathlib import Path
from typing import IO, Generator

import cv2
from django.shortcuts import get_object_or_404

from movie.models import Movie
from tv_shows.models import Shows, ShowsItem
from video.models import Video


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8124
) -> Generator[bytes, None, None]:
    consumed = 0
    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size

        if data_length <= 0:
            break

        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, slug: str = None, type_video: str = 'movie', video_id: int = None):

    if type_video == "movie":
        objects = get_object_or_404(Movie, slug=slug)
        _video = get_object_or_404(Video, pk=objects.video.pk)
    else:
        objects = get_object_or_404(ShowsItem, pk=video_id)
        _video = get_object_or_404(Video, pk=objects.video.pk)

    path = Path(_video.video.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        file = ranged(file, start=range_start, end=range_end)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range


class ConvertVideo:

    def __init__(self, video_path, convert_to: str):
        self.origin_video = Path(video_path.path)
        self.convert_to = convert_to

    def _subprocess(self, ):
        ...

    def _convert_avi_to_mp4(self, input_format):

        try:
            streem = ffmpeg.input(self.origin_video)
            streem = ffmpeg.output(streem, f'')
        except Exception as e:
            print(e)


    def _convert_to_avi(self, input_format):
        ...

    def _convert_to_webm(self, input_format):
        ...

    def _convert_to_mkv(self, input_format):
        ...

    def _get_duration_video(self) -> dict:
        # create video capture object
        data = cv2.VideoCapture(f'{self.origin_video}')

        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)

        # calculate duration of the video
        seconds = round(frames / fps)
        video_time = datetime.timedelta(seconds=seconds)

        result = {
            'seconds': seconds,
            'string_format': video_time
        }

        return result

    def create_new_object(self):
        ...

    def check_format(self):
        return str(self.origin_video).split('.')[-1]

    def check_resolution(self):
        return ''

    def convert_route(self, format_: str):
        if self.convert_to != format_:
            if format_ == 'avi':
                match self.convert_to:
                    case 'mp4':
                        return self._convert_avi_to_mp4(input_format=format_)

    def start(self):
        _format = self.check_format()
        _resolution = self.check_resolution()
        _duration = self._get_duration_video()

        print(self.convert_route(format_=_format))



