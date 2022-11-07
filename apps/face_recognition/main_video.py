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
            return False


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
