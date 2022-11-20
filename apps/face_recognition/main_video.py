import random

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
        self.userName = []
        self.frameDelay = None
        self.tolerance = 0.55
        self.numberOfPeopleInFrame = 0

    def loadCamera(self):
        self.cap = cv2.VideoCapture(0)

    def checkForFace(self):
        ret, frame = self.cap.read()
        # Detect Faces
        self.userName = []
        face_locations, face_names = self.sfr.detect_known_faces(frame=frame, face_tolerance=self.tolerance)
        self.numberOfPeopleInFrame = len(face_names)

        for face_loc, name in zip(face_locations, face_names):
            if name is "Unknown" or name is "unknown":
                name = "Unknown Individual"
                cv2.imwrite("images/" + name + ".png", frame)
                self.sfr.load_encoding_images(self.imagesPath)
            # y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            # cv2.imshow("Frame", frame)
            self.userName.append(name)
            # self.removeCamera()
        return self.userName

    def checkPeopleInFrame(self):
        return self.userName

    def removeCamera(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def getTolerance(self):
        return self.tolerance

    def setTolerance(self, newTolerance):
        self.tolerance = newTolerance

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
            self.removeCamera()
            return True
        else:
            cv2.imwrite("images/" + self.userName + ".png", frame)
            self.sfr.load_encoding_images(self.imagesPath)
            self.removeCamera()
            return False


from main_video import FactoryFaceRecognition
import msvcrt as m

def main():
    found_face = []

    faceRecognition = FactoryFaceRecognition()
    faceRecognition.loadCamera()
    print("Looking for people!")
    #    while faceRecognition.checkPersonName() == "":
    #        found_face.append(faceRecognition.checkForFace())
    userInput = 'X'
    while userInput is not 'Q' or userInput is not 'q':
        faceRecognition.checkForFace()
        if faceRecognition.numberOfPeopleInFrame > 0:
            print(faceRecognition.checkPeopleInFrame())
            #userInput = input("Press any key to continue...")
            print("Press any key to continue")
            userInput = m.getch()
# ToDO: Add an option to checkForFace after X number of frames that can be manually assigned for ease of use for the
#       developer.

if __name__ == "__main__":
    main()
