import datetime
import os
from celery import Celery
from ..utils import convert_targz_to_zip, convert_tarbz2_to_zip2
from ..utils import generate_filename, get_filename
from ..models import db, Task, EnumStatusType


redis_uri = os.environ.get('REDIS_URL')
if not redis_uri:
    redis_uri = 'redis://redis:6379/0'

celery_app = Celery(__name__, broker=redis_uri)

BUCKET_NAME = 'converter-storage/'
TEMP_FOLDER = 'files/'


@celery_app.task
def register_convert_task(task_id, file_name, time_stamp, format, new_format):
    try:
        print('taskId=' + task_id + ' - Task register_convert_task starts')
        print('taskId=' + task_id + ' - Request to convert file: ' + file_name +
              ' from ' + format + ' to ' + new_format)
        old_file = BUCKET_NAME + get_filename(file_name, time_stamp, format)
        new_file = generate_filename(task_id, file_name, new_format)

        print('taskId=' + task_id + ' - Convert starts')
        if (format == '.tar.gz' and new_format == '.zip'):
            convert_targz_to_zip(task_id, old_file, new_file)
        if (format == '.tar.bz2' and new_format == '.zip'):
            convert_tarbz2_to_zip2(task_id, old_file, new_file)
        print('taskId=' + task_id + ' - Convert finish')
        print('taskId=' + task_id + ' - Updating task id: ' + task_id)

        # TODO: update task status
        # task = Task.query.get_or_404(int(task_id))
        # task.status = EnumStatusType.PROCESSED
        # task.updated_at = datetime.datetime.utcnow
        # db.session.commit()

        print('taskId=' + task_id + ' - Updated to: ' +
              str(EnumStatusType.PROCESSED))
        print('taskId=' + task_id + ' - Task register_convert_task completed')
        return True
    except:
        return False
