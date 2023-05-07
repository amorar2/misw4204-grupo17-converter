import os


ALLOWED_EXTENSIONS = {'zip', '7z', 'tar.gz', 'tar.bz2'}


def get_filename(file_name, time_stamp, format):
    return file_name + '_' + time_stamp + format


def generate_filename(task_id, file_name, new_format):
    return task_id + '_' + file_name + new_format


def delete_file_from_folder(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        print("Error: %s file not found" % path)


def allowed_files(file_format):
    return file_format in ALLOWED_EXTENSIONS
