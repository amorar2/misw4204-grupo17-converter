def get_filename(file_name, time_stamp, format):
    return file_name + '_' + time_stamp + format


def generate_filename(task_id, file_name, new_format):
    return task_id + '_' + file_name + new_format