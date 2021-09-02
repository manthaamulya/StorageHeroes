'''Imports'''
from tensorflow.keras import models
from photosorganisation.data import get_image_dict
import os
import cv2
import numpy as np
import shutil
import sys
from termcolor import colored
import emoji
def memes_classifier(folder_path):
    print(emoji.emojize(colored("	:cat_with_tears_of_joy: Looking for Memes..", "cyan", attrs=['bold'])))
    loca_path = os.path.dirname(__file__)
    model_path =  os.path.join(loca_path, "trained_models","meme_classifier.h5")
    #model_path = "photosorganisation/trained_models/meme_classifier.h5"
    pipeline = models.load_model(model_path)

    path = folder_path
    #path = os.path.join('.', 'raw_data', 'test_mantha')

    img_dict = get_image_dict(path, size = (100,100))
    memes_dump = os.path.join(path,'Memes')


    if not os.path.exists(memes_dump):
        os.mkdir(memes_dump)



    for k in img_dict.keys():
        pred = pipeline.predict(np.expand_dims(img_dict[k], axis = 0))
        if pred > 0.5:
            shutil.move((os.path.join(path, k)), (os.path.join(path, 'Memes', k)))
