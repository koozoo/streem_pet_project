import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


# app = Celery('core') for docker
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'render': {
        'task': 'video.tasks.start_render_video',
        'schedule': 5.0
    },
}

# app.conf.timezone = 'UTC'

# t = uuid.uuid4()
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, start_render_video.s(title=f'{t}'), expires=10)

