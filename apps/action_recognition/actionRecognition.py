import torch
import cv2
import json
from torchvision.transforms import Compose, Lambda
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.data.encoded_video import EncodedVideo
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    ShortSideScale,
    UniformTemporalSubsample,
    UniformCropVideo
)


class factoryActionRecognition:
    def __init__(self):
        self.transform = None
        self.clip_duration = None
        self.FramesToProcess = 300
        self.inputs = None
        self.video_path = 'output.mp4'
        self.kinetics_id_to_classname = None
        self.model_name = 'slowfast_r101'
        self.model = torch.hub.load('facebookresearch/pytorchvideo', self.model_name, pretrained=True)
        # Set to GPU or CPU
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.eval()
        self.model = self.model.to(self.device)
    def setTime(self, time):
        self.FramesToProcess = 45 * time # setting it to 45 because the input video is set to 45 fps.
    def InitializeClassNames(self):
        json_filename = f"apps/action_recognition/working_classes.json"
        with open(json_filename, "r") as f:
            kinetics_classnames = json.load(f)

        # Create an id to label name mapping
        self.kinetics_id_to_classname = {}
        for k, v in kinetics_classnames.items():
            self.kinetics_id_to_classname[v] = str(k).replace('"', "")
    def setOutputVideoName(self, name):
        self.video_path = name
    def Processing(self):
        side_size = 256
        mean = [0.45, 0.45, 0.45]
        std = [0.225, 0.225, 0.225]
        crop_size = 256
        num_frames = 32
        sampling_rate = 2
        frames_per_second = 30
        slowfast_alpha = 4
        num_clips = 10
        num_crops = 3

        class PackPathway(torch.nn.Module):
            """
            Transform for converting video frames as a list of tensors.
            """

            def __init__(self):
                super().__init__()

            def forward(self, frames: torch.Tensor):
                fast_pathway = frames
                # Perform temporal sampling from the fast pathway.
                slow_pathway = torch.index_select(
                    frames,
                    1,
                    torch.linspace(
                        0, frames.shape[1] - 1, frames.shape[1] // slowfast_alpha
                    ).long(),
                )
                frame_list = [slow_pathway, fast_pathway]
                return frame_list

        self.transform = ApplyTransformToKey(
            key="video",
            transform=Compose(
                [
                    UniformTemporalSubsample(num_frames),
                    Lambda(lambda x: x / 255.0),
                    NormalizeVideo(mean, std),
                    ShortSideScale(
                        size=side_size
                    ),
                    CenterCropVideo(crop_size),
                    PackPathway()
                ]
            ),
        )

        # The duration of the input clip is also specific to the model.
        self.clip_duration = (num_frames * sampling_rate) / frames_per_second

    def recordVideo(self):
        # This will return video from the first webcam on your computer.
        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.video_path, fourcc, 45.0, (640, 480))
        numberOfFrames = 0
        #self.FramesToProcess = 300  # change this value for a higher length video input
        print("Recording video.")
        # loop runs if capturing has been initialized.
        while True:
            # reads frames from a camera
            # ret checks return at each frame
            ret, frame = cap.read()
            numberOfFrames = numberOfFrames + 1
            # Converts to HSV color space, OCV reads colors as BGR
            # frame is converted to hsv
            #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # output the frame
            out.write(frame)
            # Wait for 'a' key to stop the program
            if numberOfFrames >= self.FramesToProcess:
                numberOfFrames = 0  # flush to zero
                cap.release()

                # After we release our webcam, we also release the output
                out.release()

                # De-allocate any associated memory usage
                cv2.destroyAllWindows()
                break
        print("Finished recording video.")
        # Select the duration of the clip to load by specifying the start and end duration
        # The start_sec should correspond to where the action occurs in the video
        start_sec = 0
        end_sec = start_sec + self.clip_duration

        # Initialize an EncodedVideo helper class and load the video
        video = EncodedVideo.from_path(self.video_path)

        # Load the desired clip
        video_data = video.get_clip(start_sec=start_sec, end_sec=end_sec)

        # Apply a transform to normalize the video input
        video_data = self.transform(video_data)

        # Move the inputs to the desired device
        self.inputs = video_data["video"]
        self.inputs = [i.to(self.device)[None, ...] for i in self.inputs]

    def predictActions(self):
        print("Predicting actions.")
        # Pass the input clip through the model
        preds = self.model(self.inputs)

        # Get the predicted classes
        post_act = torch.nn.Softmax(dim=1)
        preds = post_act(preds)
        pred_classes = preds.topk(k=5).indices[0]

        # Map the predicted classes to the label names
        pred_class_names = [self.kinetics_id_to_classname[int(i)] for i in pred_classes]
        return pred_class_names

#from actionRecognition import factoryActionRecognition


#def main():
 #   actionRecognition = factoryActionRecognition()
 #   actionRecognition.InitializeClassNames()
 #   actionRecognition.Processing()
 #   actionRecognition.recordVideo()
 #   print(actionRecognition.predictActions())


#if __name__ == "__main__":
 #   main()
