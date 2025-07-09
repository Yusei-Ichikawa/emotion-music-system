import ultralytics
ultralytics.checks()

from ultralytics import YOLO
from IPython.display import Image


# Load a model
model = YOLO("yolo11x.yaml")  # build a new model from YAML
model = YOLO("yolo11x.pt")  # load a pretrained model (recommended for training)
#model = YOLO("yolo11x.yaml").load("runs/detect/train/weights/best.pt")  # build from YAML and transfer weights
model = YOLO("yolo11x.yaml").load("yolo11x.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="./YOLO_format/data.yaml", epochs=150, imgsz=96, cos_lr=True, device=[-1, -1])
