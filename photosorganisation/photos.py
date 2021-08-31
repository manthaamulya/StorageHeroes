import os
import matplotlib.pyplot as plt
from photosorganisation.get_total_size import get_size
import sys
from photosorganisation.duplicates import find_duplicates, move_duplicates
###
def get_photos(file_path):
    ListOfImages = []
    sub_dirs = []
    dirs = []
    for subdir, dirs, files in os.walk(file_path):
        sub_dirs.append(subdir)
        if "Duplicates" in dirs:
            dirs.remove("Duplicates")
        if "Blurry" in dirs:
            dirs.remove("Blurry")
        if "Similar" in dirs:
            dirs.remove("Similar")
        if "Memes" in dirs:
            dirs.remove("Memes")
        if "Screenshots" in dirs:
            dirs.remove("Screenshots")
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                ListOfImages.append(os.path.join(subdir, file))
    return ListOfImages,sub_dirs



if __name__ == "__main__":
    folder_path = sys.argv[1]

    total_size = get_size(folder_path)
    received_photos,folders = get_photos(folder_path)
    total_photos = len(received_photos)
    total_folders = len(folders)-1
    print(f"Found total {total_photos} photos from {total_folders} sub-folders. Total size: {total_size}")
    #print(received_photos)
    duplicates,hash_keys = find_duplicates(received_photos)
    print(f"Found {len(duplicates)} duplicates")
    move_duplicates(duplicates,folder_path)
   # total_duplicates_size =

#print((get_photos('/home/amulyamantha/code/jaseppala/photosorganisation/raw_data/')[1]))
