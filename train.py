
import os
import random
import pandas as pd
from PIL import Image
import cv2
from ultralytics import YOLO
from IPython.display import Video
from IPython.display import display
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set(style='darkgrid')
import pathlib
import glob
from tqdm.notebook import trange, tqdm
import warnings
warnings.filterwarnings('ignore')

image = cv2.imread("../datasets/underwater_plastics/train/images/1-1_jpg.rf.3c35c15f5361d33821647bfd181b0af7.jpg")
h, w, c = image.shape
print(f"The image has dimensions {w}x{h} and {c} channels.")

model = YOLO("yolov8n.pt") 

# Use the model to detect object
image = "../datasets/underwater_plastics/train/images/1-1_jpg.rf.3c35c15f5361d33821647bfd181b0af7.jpg"
result_predict = model.predict(source = image, imgsz=(640))

# Build from YAML and transfer weights
Final_model = YOLO('yolov8n.yaml').load('yolov8n.pt')  

# Training The Final Model
Result_Final_model = Final_model.train(data="../datasets/underwater_plastics/data.yaml",epochs=25, imgsz = 640, batch = 16 ,lr0=0.01, dropout= 0.15, device = 0)