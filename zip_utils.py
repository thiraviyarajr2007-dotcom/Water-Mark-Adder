import os
import zipfile

def zip_images(folder, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in os.listdir(folder):
            zipf.write(os.path.join(folder, file), file)