import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')  
app = Celery('your_project_name')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
