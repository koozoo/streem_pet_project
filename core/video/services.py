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
from video.models import Video, VideoForStreem


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
    _video = get_object_or_404(VideoForStreem, pk=video_id)

    path = Path(_video.video.path)
    file = path.open('rb')
    file_size = path.stat().st_size
    print("file size",file_size)
    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')
    print("content_range",content_range)

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        print('content_ranges',content_ranges)
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        print("start - end", range_start, range_end)
        range_start = max(0, int(range_start)) if range_start else 0
        print("start", range_start)
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        print("range_end",range_end)
        file = ranged(file, start=range_start, end=range_end)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'
        print("content_range end",content_range)

    return file, status_code, content_length, content_range


@dataclasses.dataclass
class VideoStreemData:
    title: str
    type: str
    origin_video: Video
    resolution: str
    duration_in_seconds: int
    video: str


class ConvertVideo:
    _resolution_format = {
        '720': {
            'width': 1280,
            'height': 720
        },
        '1080': {
            'width': 1920,
            'height': 1080,
        },
        '480': {
            'width': 720,
            'height': 480,
        },
        '1440': {
            'width': 2560,
            'height': 1440,
        },
        '2160': {
            'width': 3840,
            'height': 2160,
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

    def _convert_to_mp4(self, input_format, output_file_name, resolution: dict = None):

        try:
            if input_format in ['avi', 'webm', 'mpeg']:
                # moviepy convert
                clip = moviepy.VideoFileClip(str(self.origin_video))

                if resolution is not None:
                    new_file_path = output_file_name + f'_{resolution["width"]}x{resolution["height"]}' + '.mp4'
                    resize_clip = clip.resize(height=int(resolution['height']))
                    resize_clip.write_videofile(new_file_path)

                    return {'video_path': new_file_path,
                            'status': 'success'}
                else:
                    clip.write_videofile(output_file_name + '.mp4')

                    return {'video_path': output_file_name + '.mp4',
                            'status': 'success'}
            else:
                # ffmpeg convert
                streem = ffmpeg.input(self.origin_video)
                streem = ffmpeg.output(streem, f'{output_file_name}.mp4')
                ffmpeg.run(streem)
                return {'video_path': output_file_name + '.mp4',
                        'status': 'success'}

        except Exception as e:
            print(e)
            return {'video_path': '',
                    'status': 'error'}

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
        default_resolution = None
        current_resolution = self.__subprocess(
            f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of "
            f"default=nw=1:nk=1 {str(self.origin_video)}").split("\n")

        if current_resolution[1] in self._resolution_format:
            default_resolution = self._resolution_format[current_resolution[1]]
        else:
            for title, data in self._resolution_format.items():
                if int(data['width']) == int(current_resolution[0]):
                    default_resolution = self._resolution_format[title]

        return default_resolution

    def convert_route(self, format_: str, output_file_name, resolution: dict = None):
        if self.convert_to != format_:

            match self.convert_to:
                case 'mp4':
                    if resolution is not None:
                        return self._convert_to_mp4(input_format=format_,
                                                    output_file_name=output_file_name,
                                                    resolution=resolution)
                    else:
                        return self._convert_to_mp4(input_format=format_,
                                                    output_file_name=output_file_name)

    def start(self) -> list[VideoStreemData]:
        _format_data = self.check_format()
        result_list = []
        if self.convert_to != _format_data['format']:
            _duration = self._get_duration_video()
            start_resolution = self.check_resolution()

            for resolution_title, resolution in self._resolution_format.items():
                if int(start_resolution['height']) >= int(resolution_title):
                    result = self.convert_route(format_=_format_data['format'],
                                                output_file_name=_format_data['output_file_name'],
                                                resolution=self._resolution_format[resolution_title])

                    result_list.append(VideoStreemData(title=self.origin_video_object.title,
                                                       type=self.origin_video_object.type,
                                                       origin_video=self.origin_video_object,
                                                       resolution=resolution_title,
                                                       duration_in_seconds=_duration['seconds'],
                                                       video=result['video_path']))
            return result_list
        else:
            return []
