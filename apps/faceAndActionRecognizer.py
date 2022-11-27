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
    FaceRecognition.setTime(5)
    FaceRecognition.loadKnownFaces()
    PeopleInVideo = FaceRecognition.processVideo()
    print(f"The following people may be involved in the activities: {ActionsPerformed}")
    for id, name in PeopleInVideo.items():
        print(f"ID: {id} | Name: {name}")
   

if __name__ == "__main__":
    main()
