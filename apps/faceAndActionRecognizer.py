from action_recognition.actionRecognition import factoryActionRecognition 
from  faces_recognition.better_face_recognition import faceRecognition 

def main():
    ActionRecognition = factoryActionRecognition()
    ActionRecognition.setTime(5)

    ActionRecognition.InitializeClassNames()
    ActionRecognition.Processing()
    ActionRecognition.recordVideo()
    ActionsPerformed = ActionRecognition.predictActions()
     
    FaceRecognition = faceRecognition()
   # FaceRecognition.overrideInputVideo("SirWajahat.mp4") # Set this when you want a custom video to load for Face Detection.
    FaceRecognition.FaceRecognitionTolerance = 0.42 # Higher tolerance means face will be recognized more easily, though at the risk of being inaccurate
    FaceRecognition.setTime(5)
    FaceRecognition.loadKnownFaces()
    PeopleInVideo = FaceRecognition.processVideo()
    print(f"The following people may be involved in the activities: {ActionsPerformed}")
    for id, name in PeopleInVideo.items():
        print(f"ID: {id}")
   

if __name__ == "__main__":
    main()
