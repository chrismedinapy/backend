from celery import shared_task


import hashlib


@shared_task()
def hash_file(csv_file):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    # with open(file_path, 'rb') as afile:
    buf = csv_file.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = csv_file.read(BLOCKSIZE)
    hashed_file = hasher.hexdigest()
    return hashed_file
