import datetime
import os
from celery import Celery
from ..utils import convert_tarbz2_to_zip, convert_targz_to_zip
from ..utils import generate_filename, get_filename
from ..models import db, Task, EnumStatusType


redis_uri = os.environ.get('REDIS_URL')
if not redis_uri:
    redis_uri = 'redis://redis:6379/0'

celery_app = Celery(__name__, broker=redis_uri)

FILES_FOLDER = 'files/'

@celery_app.task
def register_convert_task(task_id, file_name, time_stamp, format, new_format):
    try:
        print('task register_convert_task starts')
        print('request to convert file: ' + file_name +
            ' from ' + format + ' to ' + new_format)
        old_file = FILES_FOLDER + get_filename(file_name, time_stamp, format)
        new_file = FILES_FOLDER + generate_filename(task_id, file_name, new_format)

        print('convert starts')
        if (format == '.tar.gz' and new_format == '.zip'):
            convert_targz_to_zip(old_file, new_file)
        if (format == '.tar.bz2' and new_format == '.zip'):
            convert_tarbz2_to_zip(old_file, new_file)
        print('convert finish')
        print('updating task id: ' + task_id)

        # TODO: update task status
        # task = Task.query.get_or_404(int(task_id))
        # task.status = EnumStatusType.PROCESSED
        # task.updated_at = datetime.datetime.utcnow
        # db.session.commit()

        print('task id: ' + task_id + ' updated to: ' + str(EnumStatusType.PROCESSED))
        print('task register_convert_task finish')
        return True
    except:
        return False
