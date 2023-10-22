# import module 
import cv2 
import datetime 


def get_duration_video(video_path: str) -> str:
    # create video capture object
    data = cv2.VideoCapture(f'{video_path}')

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)

    return str(video_time)
