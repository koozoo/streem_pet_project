import dataclasses
import datetime
from subprocess import PIPE, run
import shlex

import ffmpeg
import uuid
import moviepy.editor as moviepy

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


@dataclasses.dataclass
class VideoStreemData:
    title: str
    type: str
    origin_video: int
    resolution: str
    duration_in_seconds: int
    video: str

class ConvertVideo:

    _resolution_format = {
        'HD': {
            'width': 720,
            'height': 1280
        },
        'FHD': {
            'width': 1080,
            'height': 1920
        },
        'SD': {
            'width': 480,
            'height': 720
        },
        '2K': {
            'width': 1440,
            'height': 2560
        },
        '4K': {
            'width': 2160,
            'height': 3840
        }
    }

    def __init__(self, video_path, convert_to: str, origin_video_object: VideoStreemData = None):
        self.origin_video_object = origin_video_object
        self.origin_video = Path(video_path.path)
        self.convert_to = convert_to

    def __subprocess(self, command):
        try:
            result = run(shlex.split(command), stdout=PIPE, stderr=PIPE, universal_newlines=True)
            return result.stdout
        except Exception as e:
            print(f'Unknown error. {e}')

    def _convert_to_mp4(self, input_format, output_file_name):

        try:
            if input_format in ['avi', 'webm']:
                # moviepy convert
                clip = moviepy.VideoFileClip(str(self.origin_video))
                clip.write_videofile(output_file_name+'.mp4')
            else:
                # ffmpeg convert
                streem = ffmpeg.input(self.origin_video)
                streem = ffmpeg.output(streem, f'{output_file_name}.mp4')
                ffmpeg.run(streem)

        except Exception as e:
            print(e)

    def _convert_to_avi(self, input_format, output_file_name):
        ...

    def _convert_to_webm(self, input_format, output_file_name):
        if input_format in ['mp4', 'avi']:
            # moviepy convert
            clip = moviepy.VideoFileClip(str(self.origin_video))
            clip.write_videofile(output_file_name + '.webm')

    def _convert_to_mkv(self, input_format, output_file_name):
        # ffmpeg convert
        streem = ffmpeg.input(self.origin_video)
        streem = ffmpeg.output(streem, f'{output_file_name}.mkv')
        ffmpeg.run(streem)

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

    def _object_update(self, type_: str):
        print(type_)

    def _create_object(self, type_: str):
        print(type_)

    def check_format(self):
        data = str(self.origin_video).split('.')

        return {'format': data[-1],
                'output_file_name': f'{".".join(data[:-1])}.{uuid.uuid4()}'
                }

    def check_resolution(self):
        return self.__subprocess(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of "
                                 f"default=nw=1:nk=1 {str(self.origin_video)}").split("\n")

    def convert_route(self, format_: str, output_file_name):
        if self.convert_to != format_:
            match self.convert_to:
                case 'mp4':
                    return self._convert_to_mp4(input_format=format_, output_file_name=output_file_name)

    def start(self) -> list[VideoStreemData]:
        _format_data = self.check_format()

        if self.convert_to != _format_data['format']:
            _duration = self._get_duration_video()
            original_resolution = self.check_resolution()

            # for i in original_resolution:
            #     print('line: ', i)
            for resolution_title, resolution in self._resolution_format.items():
                print(f'START RENDER OBJECT: <ID: {id(self.origin_video_object)}> --->  video title: {self.origin_video_object.title} key: {resolution_title} - value: {resolution} | duration: {_duration}')

            # print(self.convert_route(format_=_format_data['format'], output_file_name=_format_data['output_file_name']))
        else:
            return []
