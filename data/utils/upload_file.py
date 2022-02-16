import os


def upload_file_to_local(file, directory, new_name):
    """
    Upload a file to local with given directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{file.name}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    os.rename(f"{directory}/{file.name}", f"{directory}/{new_name}")
    return (f"{directory}/{new_name}")
