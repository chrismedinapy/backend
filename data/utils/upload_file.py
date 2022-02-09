import os

def upload_file_to_local(file, directory):
    """
    Upload a file to local with given directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{file.name}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return (f"{directory}/{file.name}")