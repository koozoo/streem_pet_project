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

    def _create_new_folder(self):
        ...

    def _create_hls(self):

        command = f"""
            ffmpeg -i {self.origin_video} \
            -filter_complex \
            "[0:v]fps=fps=30,split=3[v1][v2][v3]; \
            [v1]scale=width=-2:height=1080[1080p]; [v2]scale=width=-2:height=720[720p]; [v3]scale=width=-2:height=360[360p]" \
            -codec:v libx264 -crf:v 23 -profile:v high -pix_fmt:v yuv420p -rc-lookahead:v 60 -force_key_frames:v expr:'gte(t,n_forced*2.000)' -preset:v "medium" -b-pyramid:v "strict" \
            -map [1080p] -minrate:v:0 1600000 -maxrate:v:0 2000000 -bufsize:v:0 2*2000000 \
            -map [720p] -minrate:v:1 900000 -maxrate:v:1 1200000 -bufsize:v:1 2*1000000 \
            -map [360p] -minrate:v:2 500000 -maxrate:v:2 700000 -bufsize:v:2 2*500000 \
            -codec:a aac -ac:a 2 \
            -map 0:a:0 -b:a:0 192000 \
            -map 0:a:0 -b:a:1 128000 \
            -map 0:a:0 -b:a:2 96000 \
            -a53cc:0 1 -a53cc:1 1 \
            -f hls \
            -strftime 1 \
            -hls_flags second_level_segment_index \
            -hls_time 6 \
            -hls_playlist_type vod \
            -hls_segment_type mpegts \
            -hls_segment_filename 'test_data_%Y%m%d_%v_%%05d.ts' \
            -master_pl_name master.m3u8 \
            -var_stream_map "v:0,a:0,name:1080p v:1,a:1,name:720p v:2,a:2,name:360p" test_manifest_%v.m3u8
        """

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
