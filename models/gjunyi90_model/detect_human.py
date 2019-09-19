from imageai.Detection import ObjectDetection
import os
from PIL import Image
from pathlib import Path
import pickle

# Download model with the link
# 'https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/resnet50_coco_best_v2.0.1.h5'


def get_human_ratio(image, detector):
    human_ratios = []

    im = Image.open(image)
    image_size = im.size[0] * im.size[1]

    detections = detector.detectObjectsFromImage(input_image=image)
    for detection in detections:
        for i, attribute in enumerate(detection.values()):
            if attribute == 'person':
                human_box = list(detection.values())[2]

                # Box Points - [x1,y1,x2,y2]
                human_size = (human_box[2] - human_box[0]) * (human_box[3] - human_box[1])
                human_ratios.append(human_size / image_size)
    return human_ratios


execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

data_path = 'data/train'
data_path_full = (Path().resolve().parents[1] / f'{data_path}').resolve()
folders = data_path_full.glob("*/*")
detection_list = []

for folder in folders:
    folder = folder.resolve().glob("*.*")
    for files in list(folder):
        ratio = sum(get_human_ratio(folder, detector))
        detection_list.append([str(folder), ratio])

with open("detection_list.pkl", "wb") as f:
    pickle.dump(detection_list, f)
