import os
from os.path import isdir
import cv2
import numpy as np
from google.cloud import storage
from zipfile import ZipFile

from tensorflow.keras.applications.vgg16 import preprocess_input

def get_data_gcp(GCP_FILE_NAME):
    """downloads a zip file into the current working directory and extracts its contents into the raw data folder

    Args:
        GCP_FILE_NAME ([string]): [Name of the zip file]
    """
    client = storage.Client(project = 'le-wagon-ds-bootcamp-318909')
    bucket = client.get_bucket('lewagon-photo-classifier')
    blob = bucket.get_blob(GCP_FILE_NAME)
    blob.download_to_filename(os.path.join(os.getcwd(), GCP_FILE_NAME))

    with ZipFile(os.path.join(os.getcwd(), GCP_FILE_NAME), 'r') as zipObj:

        zipObj.extractall('../raw_data')

def load_data(path, how = 'one', grayscale = True, size = (100,100), asarray = True, n_img = 'all'):
    """loads all images into an array

    path: path to the folder in which the images or folders full of images are
    how: 'one' to load files from one folder, 'many' if images are in subfolders (default 'one')
    grayscale: pictures are stored in grayscale if True, in RGB if False (default 'True')
    asarray: return a np.array. Returns a list if False (default 'True')
    n_img: number of images to be loaded from the path (all by default)

    Returns:
        np.array of n_img pictures
        or list of n_img pictures if asarray = False
    """
    X = []

    if type(n_img) == int:
        i = 0

    if how == 'one':
        for file in os.listdir(path):                              # get every file in the folder
            img = cv2.imread(os.path.join(path, file))                  # load the image
            if grayscale:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                res = cv2.resize(gray, dsize=size)             # make it RGB (cv2 uses BGR)
                X.append(res)
            else:
                clr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                X.append(clr)
            if type(n_img) == int:
                i += 1
                if i == n_img:
                    if asarray:
                        return np.array(X)
                    else:
                        return X

    if how == 'many':
        for folder in os.listdir(path):
            if isdir(os.path.join(path, folder)):
                for file in os.listdir(os.path.join(path, folder)):                              # get every file in the folder
                    img = cv2.imread(os.path.join(path, folder, file))                  # load the image
                    if grayscale:
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)             # make it RGB (cv2 uses BGR)
                        res = cv2.resize(gray, dsize=size)
                        X.append(res)
                    else:
                        clr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        X.append(img)

                    if type(n_img) == int:
                        i += 1
                        if i == n_img:
                            if asarray:
                                return np.array(X)
                            else:
                                return X

    if asarray:
        return np.array(X)
    else:
        return X

picture_file_types = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.heic')

def get_image_dict(path, grayscale = True, size = (100, 100), vgg16 = False):
    """loads all images into a dictionary with file names as keys

    Args:
        path (string): the system path from which to load the images
        grayscale (bool, optional): load images as grayscale (True) or in colour (False). Defaults to True.
        size (tuple, optional): Resize images to the size expected by the model. Defaults to (100, 100).

    Returns:
        A dictionary of images as np.arrays with the file names as keys
    """
    #instantiating a dictionary with picture file names as keys
    img_dict = {file:0 for file in os.listdir(path) if file.lower().endswith(picture_file_types)}

    for file in os.listdir(path):
        if file.lower().endswith(picture_file_types):                              #get every image file in folder
            img = cv2.imread(os.path.join(path, file))                  # load the image
            if grayscale:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            #grayscale
                res = cv2.resize(gray, dsize=size)                    #resize
                img_dict[file] = res
            else:
                if vgg16:
                    clr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    res = cv2.resize(clr, dsize=size)
                    preproc = preprocess_input(res)
                    img_dict[file] = preproc
                else:
                    clr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    res = cv2.resize(gray, dsize=size)
                    img_dict[file] = clr

    return img_dict
