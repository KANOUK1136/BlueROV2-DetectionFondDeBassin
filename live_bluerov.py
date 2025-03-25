#import cv2
import argparse
import numpy as np
from ultralytics import YOLO
import supervision as sv
from supervision.draw.color import Color
from gi.repository import Gst
from bluerov_video import Video  # Import BlueROV video class

# Define your custom class labels
CUSTOM_CLASSES = [
    "Mask", "Can", "Cellphone", "electronics", "Gbottle", "Glove", 
    "Metal", "Misc", "Net", "Pbag", "Pbottle", "Plastic", 
    "Rod", "Sunglasses", "Tire"
]

ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live with BlueROV stream")
    parser.add_argument("--webcam-resolution", default=[1280, 720], nargs=2, type=int)
    parser.add_argument("--port", type=int, default=5600, help="UDP Port for BlueROV stream")
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    # BlueRov video stream     
    video = Video(port=args.port)

    print('Initializing BlueROV stream...')
    waited = 0
    while not video.frame_available():
        waited += 1
        print(f'\r  Frame not available (x{waited})', end='')
        cv2.waitKey(30)
    
    print('\nSuccess! Starting streaming - press "q" to quit.')

    model = YOLO("runs/detect/train4/weights/best.pt")  

    box_annotator = sv.BoxAnnotator(thickness=2)
    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon)
    
    color = Color(r=0, g=0, b=255)
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=color, thickness=2)

    while True:
        if video.frame_available():
            frame = video.frame()
        else:
            continue  

        results = model(frame, agnostic_nms=True)[0]

        detections = sv.Detections(
            xyxy=results.boxes.xyxy.cpu().numpy(),
            confidence=results.boxes.conf.cpu().numpy(),
            class_id=results.boxes.cls.cpu().numpy().astype(int)
        )

        frame = box_annotator.annotate(scene=frame, detections=detections)

        for xyxy, confidence, class_id in zip(detections.xyxy, detections.confidence, detections.class_id):
            class_label = CUSTOM_CLASSES[class_id] if class_id < len(CUSTOM_CLASSES) else "Unknown"
            label = f"{class_label} {confidence:0.2f}"
            x1, y1, x2, y2 = map(int, xyxy)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)

        cv2.imshow("YOLOv8 Live Detection - BlueROV", frame)

        # Exit on with "q"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
