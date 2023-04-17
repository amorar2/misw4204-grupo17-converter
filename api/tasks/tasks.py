import zipfile
import tarfile
from celery import Celery
from ..utils import convert_targz_to_zip, convert_tarbz2_to_zip

celery_app = Celery(__name__, broker='redis://redis:6379/0')

FILE_FOLDER = 'files'


def get_filename(file_name, time_stamp, format):
    return file_name + '_' + time_stamp + format


def generate_filename(task_id, file_name, new_format):
    return task_id + '_' + file_name + new_format


@celery_app.task
def register_convert_task(task_id, file_name, time_stamp, format, new_format):
    print(file_name, time_stamp, format, new_format)
    print('Converting file from ' + format + ' to ' + new_format)
    print(file_name, time_stamp, format, new_format)
    print(format == '.tar.bz2')
    old_file = FILE_FOLDER + get_filename(file_name, time_stamp, format)
    new_file = FILE_FOLDER + generate_filename(task_id, file_name, new_format)
    if (format == '.tar.gz' and new_format == '.zip'):
        print('converting from ..tar.gz to .zip')
        convert_targz_to_zip(old_file, new_file)
    if (format == '.tar.bz2' and new_format == '.zip'):
        print('converting from .tar.bz2 to .zip')
        convert_tarbz2_to_zip(old_file, new_file)
    print('finish')
    return True
