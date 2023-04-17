import zipfile
import tarfile


# Convert from TAR.GZ to ZIP
def convert_targz_to_zip(input_file, output_file):
    print('converting from ..tar.gz to .zip')
    with tarfile.open(input_file, 'r:gz') as tar_ref:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for member in tar_ref.getmembers():
                try:
                    zip_ref.write(member.name, arcname=member.name)
                except:
                    print('¯\_(ツ)_/¯')

# Convert from TAR.BZ2 to ZIP
def convert_tarbz2_to_zip(input_file, output_file):
    print('converting from .tar.bz2 to .zip')
    with tarfile.open(input_file, 'r:bz2') as tar_ref:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for member in tar_ref.getmembers():
                zip_ref.writestr(
                    member.name, tar_ref.extractfile(member).read())
