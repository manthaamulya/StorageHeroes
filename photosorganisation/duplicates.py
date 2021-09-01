# imports
import hashlib
import PIL
from imageio import imread
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import numpy as np
from hashlib import md5
import os
import shutil
from termcolor import colored
from photosorganisation.get_total_size import get_size


def find_duplicates(filepath):
    duplicates = []
    hash_keys = dict()
    print(colored("Looking for Duplicates..", "cyan", attrs=['bold']))
    for index, filename in enumerate(filepath):
        #print(filename)
        if os.path.isfile(filename):
            with open(filename,'rb') as  f:
                #print(filename)
                filehash = hashlib.md5(f.read()).hexdigest()
                #print(filehash)
            if filehash not in hash_keys:
                hash_keys[filehash] = index
            else:
                #print("Duplicate found")
                duplicates.append((filename,index,hash_keys[filehash]))
    return duplicates, hash_keys
#
def move_duplicates(duplicatesList,folder_path):
    if len(duplicatesList) > 0:
        duplicates_folder = os.path.join(folder_path, 'Duplicates')
        #print(duplicates_folder)
        if not os.path.exists(duplicates_folder):
            os.mkdir(duplicates_folder)
        for file in duplicatesList:
            #print(file)
            shutil.move(file[0], duplicates_folder)
        total_duplicates_size = get_size(os.path.join(folder_path, 'Duplicates'))
        print(colored(f"Moved Duplicates to folder, size: {total_duplicates_size}","green"))
