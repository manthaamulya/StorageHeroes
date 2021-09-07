"""Imports"""
from photosorganisation.photos import get_photos
from hashlib import md5
import PIL
from imageio import imread
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import numpy as np
import cv2
import os
import scipy
import itertools
from  scipy.spatial.distance import hamming
from photosorganisation.get_total_size import get_size
import sys
from photosorganisation.duplicates import find_duplicates, move_duplicates
import shutil
from termcolor import colored
import emoji

#
def img_gray(image):
    image = imread(image)
    return np.average(image,axis=2,weights=[0.2999,0.587,0.114])
#
#resize image and flatten
def resize(image, height=30, width=30):
    row_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten()
    col_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten('F')
    return row_res, col_res
#
#gradient direction based on intensity

def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()
#
def file_hash(array):
    return md5(array).hexdigest()
#


def difference_score(image, height=30, width=30):
    gray = img_gray(image)
    row_res, col_res = resize(gray, height, width)
    difference = intensity_diff(row_res, col_res)

    return difference
#
def hamming_distance(image, image2):
    score =scipy.spatial.distance.hamming(image, image2)
    return score
#
def difference_score_dict_hem(image_list):
    ds_dict = {}
    duplicates = []
    for image in image_list:
        ds = difference_score(image)

        if image not in ds_dict:
            ds_dict[image] = ds
        else:
            duplicates.append((image, ds_dict[image]))

    return duplicates, ds_dict
##
def move_similar(similarList,folder_path):
    similar_folder = os.path.join(folder_path, 'Similar')
    if not os.path.exists(similar_folder):
        os.mkdir(similar_folder)
    if len(similarList) > 0:
        for file in similarList:
            #print(file)
            shutil.move(file, similar_folder)
            total_Similar_size = get_size(os.path.join(folder_path, 'Similar'))
        print(emoji.emojize(colored(f"Found near duplicates. Delete unnecessary!! Save Space!! :hourglass_not_done:", "red")))
        print(emoji.emojize(colored(f"Found and moved {len(similarList)} Photos which are similar, Folder size:{total_Similar_size} :man_dancing:","green",attrs=['bold'])))

####
def sort_similar(received_photos):
    similar_lists = []
    similar, ds_dict_hem =difference_score_dict_hem(received_photos)
    for k1,k2 in itertools.combinations(ds_dict_hem, 2):
        if hamming_distance(ds_dict_hem[k1], ds_dict_hem[k2])< .31:
            similar_lists.append(k1)#
            similar_lists.append(k2)
    return set(similar_lists)

if __name__ == "__main__":
    folder_path = sys.argv[1]
    received_photos, folders = get_photos(folder_path)
    similar = sort_similar(received_photos)
    move_similar(similar, folder_path)

    print(colored(f"Found and moved {len(similar)} Photos similar to one another", "green",attrs=['bold']))
