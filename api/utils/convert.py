import zipfile
import tarfile
import gcsfs
import os
from google.cloud import storage
from api.utils.files import delete_file_from_folder

TEMP_FOLDER = 'files/'


def convert_targz_to_zip(task_id, input_file, output_file):
    # Convert from TAR.GZ to ZIP
    try:
        print('taskId=' + task_id + ' - Setting up connections')

        fs = gcsfs.GCSFileSystem(project='miso-mobile-2023')
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('converter-storage')
        output_path = TEMP_FOLDER + output_file

        print('taskId=' + task_id + ' - Converting2 from .tar.bz2 to .zip')
        print('taskId=' + task_id + ' - File ' +
              input_file + ' to: ' + output_file)

        with fs.open(input_file) as f:
            print('taskId=' + task_id + ' - Getting input file')

            with tarfile.open(fileobj=f, mode='r:gz') as tar_ref:
                print('taskId=' + task_id + ' - Creating output temp file')

                with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    print('taskId=' + task_id +
                          ' - output file = ' + output_path)
                    print('taskId=' + task_id + ' - Input file content:')

                    for member in tar_ref.getmembers():
                        try:
                            print('file name = ' + str(member.name))
                            zip_ref.write(member.name, arcname=member.name)
                        except:
                            print('¯\_(ツ)_/¯')
                    print('taskId=' + task_id + ' - Output temp file created')
                    print('taskId=' + task_id + ' - Uploading output file')

        blob = bucket.blob(output_file)
        blob.upload_from_filename(output_path)

        print('taskId=' + task_id + ' - Upload complete')

        if blob.exists():
            delete_file_from_folder(output_path)
            print('taskId=' + task_id + ' - Upload successful!')
        else:
            print('taskId=' + task_id + ' - Upload failed.')

    except Exception as error:
        print('taskId=' + task_id + ' - An exception occurred: {}'.format(error))


def convert_tarbz2_to_zip2(task_id, input_file, output_file):
    # Convert from TAR.BZ2 to ZIP
    try:
        print('taskId=' + task_id + ' - Setting up connections')

        fs = gcsfs.GCSFileSystem(project='miso-mobile-2023')
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('converter-storage')
        output_path = TEMP_FOLDER + output_file

        print('taskId=' + task_id + ' - Converting2 from .tar.bz2 to .zip')
        print('taskId=' + task_id + ' - File ' +
              input_file + ' to: ' + output_file)

        with fs.open(input_file) as f:
            print('taskId=' + task_id + ' - Getting input file')

            with tarfile.open(fileobj=f, mode='r:bz2') as tar_ref:
                print('taskId=' + task_id + ' - Creating output temp file')

                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    print('taskId=' + task_id +
                          ' - output file = ' + output_path)
                    print('taskId=' + task_id + ' - Input file content:')

                    for member in tar_ref.getmembers():
                        print('file name = ' + str(member.name))

                        zip_ref.writestr(
                            member.name, tar_ref.extractfile(member).read())

                    print('taskId=' + task_id + ' - Output temp file created')
                    print('taskId=' + task_id + ' - Uploading output file')

        blob = bucket.blob(output_file)
        blob.upload_from_filename(output_path)
        print('taskId=' + task_id + ' - Upload complete')

        if blob.exists():
            delete_file_from_folder(output_path)
            print('taskId=' + task_id + ' - Upload successful!')

        else:
            print('taskId=' + task_id + ' - Upload failed.')

    except Exception as error:
        print('taskId=' + task_id + ' - An exception occurred: {}'.format(error))
