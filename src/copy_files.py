import os
import shutil

def copy(source, destination):
    if os.path.exists(destination):
        print(f"Deleting destination directory: {destination}")
        shutil.rmtree(destination)
    print(f"Creating directory: {destination}")
    os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy(source_path, destination_path)