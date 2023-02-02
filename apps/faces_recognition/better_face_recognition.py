import face_recognition
import os
import cv2
import pickle
import time
 

class faceRecognition:
    def __init__(self):
        self.KNOWN_FACES_DIR = "D:/Final Year Project/Employee_Monitoring_Testbed/apps/media/images/Users/"
        self.FaceRecognitionTolerance = 0.5
        self.FRAME_THICKNESS = 3
        self.FONT_THICKNESS = 2
        self.false_positive_tolerance = 2
        self.FramesToProcess = 300
        self.faceRecognitionModel = "hog"
        self.fileName = "output.mp4"
        self.video = cv2.VideoCapture(self.fileName)
        self.newFaceName = "defaultName"
        self.known_faces = []
        self.known_ids = []
        self.known_names = []
        self.names_found = []
        self.ids_found = []
        self.dictionaryOutput = {}
        self.result = None
        self.next_id = 0

    def setTime(self, time):
        self.FramesToProcess = 30 * time
    def loadKnownFaces(self):
        for name in os.listdir(self.KNOWN_FACES_DIR):
            for filename in os.listdir(f"{self.KNOWN_FACES_DIR}/{name}"):
                encoding = pickle.load(open(f"{self.KNOWN_FACES_DIR}/{name}/{filename}", "rb"))
                self.known_faces.append(encoding)
                temp_id = filename.split('-')[0] # first half of the string
                self.known_ids.append(int(temp_id))
                temp_name = filename.split('-')[1].split('--')[0] # get the name of the individual from the file
                self.known_names.append(temp_name)
             #   self.result = cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'), 60, (640, 480))
        if len(self.known_ids) > 0:
            self.next_id = max(self.known_ids) + 1
        else:
            self.next_id = 0
    
    def overrideInputVideo(self, videoName):
        self.video = cv2.VideoCapture(videoName)

    def processVideo(self):
        numberOfFrames = 0
        print(f"Processing video: {self.fileName}")
        ret, image = self.video.read()
        while(ret):
            if numberOfFrames >= self.FramesToProcess-2:
                    numberOfFrames = 0  # flush to zero
                    self.video.release()
                    # De-allocate any associated memory usage
                    cv2.destroyAllWindows()
                    break
            numberOfFrames = numberOfFrames + 1
            ret, image = self.video.read()
            locations = face_recognition.face_locations(image, model=self.faceRecognitionModel)
            encodings = face_recognition.face_encodings(image, locations)

            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.FaceRecognitionTolerance)
                match = ""
                matchName = ""
                if results.count(True) >= self.false_positive_tolerance:
                    match = self.known_ids[results.index(True)]
                    matchName = self.known_names[results.index(True)]
                    self.ids_found.append(match)
                    self.names_found.append(matchName)
                #else:
                #    print("Match not found. Iterating to next frame")
                #    match = str(self.next_id)
                #    self.next_id += 1
                #    self.known_ids.append(match)
                #    self.known_faces.append(face_encoding)
                #    os.mkdir(f"{self.KNOWN_FACES_DIR}/{match}-{self.newFaceName}")
                #    pickle.dump(face_encoding, open(f"{self.KNOWN_FACES_DIR}/{match}-{self.newFaceName}/{match}-{self.newFaceName}--{int(time.time())}.pkl", "wb"))
                else:
                    print("...")
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, top_left, bottom_right, color, self.FRAME_THICKNESS)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[3], face_location[2]+22)
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, str(match)+ ":"+matchName, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200))
            self.dictionaryOutput = dict(zip(self.ids_found, self.names_found))
        return self.dictionaryOutput

"""
from better_face_recognition import faceRecognition

def main():
    FaceRecognition = faceRecognition()
    FaceRecognition.loadKnownFaces()
    localDictionary = FaceRecognition.processVideo()
    for id, name in localDictionary.items():
        print(f"ID: {id} | Name: {name}")
if __name__ == "__main__":
    main()
"""