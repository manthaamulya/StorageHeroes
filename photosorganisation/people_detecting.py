from matplotlib import pyplot
from PIL import Image
from numpy import asarray
import cv2
from mtcnn.mtcnn import MTCNN
import sys
import os
import shutil
#detect faces
def define_detector():
    detector = MTCNN()
    return detector

def detect_faces(filename,detector):
    img = pyplot.imread(filename)
    #create detector using default weights

    #detect all faces in image
    results = detector.detect_faces(img)
    return results


def extract_faces(filename, required_size=(224, 224)):
    #load image from file
    img = pyplot.imread(filename)
    #load detected faces from detector
    results = detect_faces(filename)
    faces_in_image = []
    # extract the bounding box from the faces
    for i in range(len(results)):
        x1, y1, width, height = results[i]['box']
        x2, y2 = x1 + width, y1 + height
        face = img[y1:y2, x1:x2]
        #draw erectangle
        cv2.rectangle(img, (x1, y2), (x2, y1), (0, 0, 255), 3)
        #resize the face pixels
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        faces_in_image.append(face_array)
    return faces_in_image, img
#function to decide if there are ppl or not
def people(filename,folder_path,detector):
    people = detect_faces(filename,detector)
    if len(people) > 0:
        people_dump = os.path.join(folder_path, 'People')
        if not os.path.exists(people_dump):
            os.mkdir(people_dump)
        #print(people_dump)
        shutil.move(filename, people_dump)

    else:
        pass
####
if __name__ == '__main__':
    number_of_folders = len(sys.argv)
    dirs_to_scan = sys.argv[1:]
    photos_with_people = 0
    # TO-DO make dict with file names
    for dir in dirs_to_scan:
        # get path, get files
        for file in dir:
            if people(filename):
                photos_with_people + 1
