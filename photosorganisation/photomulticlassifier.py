'''Imports'''
from tensorflow.keras import models
from photosorganisation.data import get_image_dict
import os
import cv2
import numpy as np
import shutil
import sys
from tensorflow.keras.applications.vgg16 import preprocess_input


def photomulticlassifier(folder_path):
    loca_path = os.path.dirname(__file__)
    model_path = os.path.join(loca_path, "trained_models",
                              "photo_multi_classifier.h5")
    #model_path = "photosorganisation/trained_models/meme_classifier.h5"
    pipeline = models.load_model(model_path)

    path = folder_path
    #path = os.path.join('.', 'raw_data', 'test_mantha')

    img_dict = get_image_dict(path, grayscale=False, size=(150, 150), vgg16=True)
    city_dump = os.path.join(path, 'city')
    nature_dump = os.path.join(path, 'nature')
    food_dump = os.path.join(path, 'food')
    animals_dump = os.path.join(path, 'animals')
    dumps = [city_dump,nature_dump,food_dump,animals_dump]
    for dump in dumps:
        if not os.path.exists(dump):
            os.mkdir(dump)

    class_names = ['city', 'nature', 'food', 'animals']
    for k in img_dict.keys():
       # img_preprocessed = preprocess_input(img_dict[k])
        pred = pipeline.predict(np.expand_dims(img_dict[k], axis=0))
        pred_new = [round(val) for val in pred[0]]
        if 1 in pred_new:
            i=pred_new.index(1)
            shutil.move((os.path.join(path, k)), (os.path.join(path, class_names[i], k)))

#photomulticlassifier('/home/aswathy/code/StorageHeroes/raw_data/test_multiclassifier')
