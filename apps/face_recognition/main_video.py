import cv2
from simple_facerec import SimpleFacerec
import tkinter as tk
from tkinter import simpledialog


class FactoryFaceRecognition:
    def __init__(self):
        self.cap = None
        self.sfr = SimpleFacerec()
        self.imagesPath = "images"
        self.sfr.load_encoding_images(self.imagesPath)
        self.userName = ""
        self.frameDelay = None

    def loadCamera(self):
        self.cap = cv2.VideoCapture(2)

    def checkForFace(self):
        ret, frame = self.cap.read()
        # Detect Faces
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.imshow("Frame", frame)
            if name == "Unknown":
                self.addNewUser(frame)
            else:
                print("Face matched: " + name)
                self.userName = name
                self.cap.release()
                cv2.destroyAllWindows()
                return name

    def checkPersonName(self):
        return self.userName

    def AddFrameDelay(self, delay):
        self.frameDelay = delay

    def addNewUser(self, frame):
        self.userName = ""
        ROOT = tk.Tk()
        ROOT.withdraw()
        # the input dialog
        self.userName = simpledialog.askstring(title="Identification",
                                               prompt="What's your Name?:")
        if self.userName is None:
            self.addNewUser(frame)
            self.cap.release()
            cv2.destroyAllWindows()
            return True
        else:
            cv2.imwrite("images/" + self.userName + ".png", frame)
            self.sfr.load_encoding_images(self.imagesPath)
            self.cap.release()
            cv2.destroyAllWindows()
            return False


"""
from main_video import FactoryFaceRecognition


def main():
    faceRecognition = FactoryFaceRecognition()
    faceRecognition.loadCamera()
    print("Looking for people!")
    while faceRecognition.checkPersonName() == "":
        faceRecognition.checkForFace()
# ToDO: Add an option to checkForFace after X number of frames that can be manually assigned for ease of use for the
#       developer.

if __name__ == "__main__":
    main()
"""

import face_recognition as fr
import cv2
import numpy as np
import os
class FactoryMultipleFacesRecognition:
    def __init__(self):
        self.cap = None
        self.images_folder = 'images/'
        self.load_image = None
        self.target_image = None
        self.target_encoding = None
        self.face_recognition_tolerance = 0.6
        self.faces_found = None

    def loadCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # set Width
        self.cap.set(4, 480)  # set Height
        ret, frame = self.cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        self.target_image = fr.face_locations(rgb_small_frame)
        self.target_encoding = fr.face_encodings(rgb_small_frame,self.target_image)
        print(self.target_image)
        print(self.target_encoding)

    def encode_faces(self, folder):
        list_people_encoding = []
        for filename in os.listdir(folder):
            known_image = fr.load_image_file(f'{folder}{filename}')
            known_encoding = fr.face_encodings(known_image)[0]
            list_people_encoding.append((known_encoding, filename))
            print(list_people_encoding)
        return list_people_encoding

    def find_target_face(self):
        # face_location = fr.face_locations(target_image)
        faces_found = []
        for person in self.encode_faces(self.images_folder):
            encoded_face = person[0]
            filename = person[1]
            is_target_face = False
            is_target_face = fr.compare_faces(encoded_face, self.target_encoding,
                                              tolerance=self.face_recognition_tolerance)
            for face in is_target_face:
                if face:
                    print("face found")
                    index = filename.rfind(".")
                    faces_found.append(filename[0:index])
        return faces_found


from main_video import FactoryMultipleFacesRecognition as multiFaceRecognition


def main():
    mf = multiFaceRecognition()
    mf.loadCamera()
    print(f"Faces found: {mf.find_target_face()}")
    # render_image()


if __name__ == "__main__":
    main()
