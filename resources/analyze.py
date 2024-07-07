import os
import sys
import cv2
import argparse
from PIL import ImageFont, ImageDraw, Image
from ultralytics import YOLO
import numpy as np

# Set environment variable for headless mode
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# List of acceptable video formats for input
VIDEO_FORMATS = (".mov", ".mp4")

# Font used for image overlay
font_path = os.path.join('/resources', os.environ.get('FONT', "OCRA.ttf"))

stop_after_first_detect_frame = False

# Text attributes
font_size = int(os.environ.get('FONTSIZE', 76))
font_thinkness = int(os.environ.get('RECTBACKGROUNDWIDTHMULTIPLIER', 6))
font_vertical_offset = int(os.environ.get('TEXTBACKDROPRECTVERTOFFSET', 95))
text_color_r = int(os.environ.get('FONTCOLORR', 255))
text_color_g = int(os.environ.get('FONTCOLORG', 255))
text_color_b = int(os.environ.get('FONTCOLORB', 255))
text_color = (text_color_r,text_color_g,text_color_b) 
print(("Text Color RGB: {}{}{}").format(text_color_r, text_color_g, text_color_b))

# Colored box behind the text attributes
text_backdrop_rect_height_offset = int(os.environ.get('TEXTBACKDROPRECTHEIGHT', 80))
rect_background_color_r = int(os.environ.get('RECTBACKGROUNDCOLORR', 0))
rect_background_color_g = int(os.environ.get('RECTBACKGROUNDCOLORG', 0))
rect_background_color_b = int(os.environ.get('RECTBACKGROUNDCOLORB', 0))
rect_background_color = (rect_background_color_r,rect_background_color_g,rect_background_color_b)

def process_video(input_path, output_path):
    # Load YOLOv8 model pre-trained on COCO dataset
    model_dir = os.path.join('/resources', os.environ.get('MODEL', "yolov8s.pt"))
    model = YOLO(model_dir)

    # Open the input video file
    print(("Opening video file at {}").format(input_path))
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Open the output video file
    if not stop_after_first_detect_frame:
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    first_image = True

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        name_map = results[0].names

        # Draw bounding boxes for detected cars
        for result in results:
            for obj in result.boxes:
                name_id = int(obj.cls[0])
                confidence = round(float(obj.conf[0]) * 100)
                print("Found object {} with {} confidence".format(name_map[name_id], confidence))
                # if obj.cls == 'car':  # Check if detected object is a car
                x1, y1, x2, y2 = map(int, obj.xyxy[0])
                print("Box added at ({}, {}) to ({}, {})".format(x1, y1, x2, y2))
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)

                confidence_pct = "{}%".format(confidence)
                label = "{} {}".format(name_map[name_id], confidence_pct)
                # font_size = 6
                # font_vertical_offset = 95
                # text_backdrop_rect_height_offset = 80
                # rect_background_color = (0,0,0)
                # text_color = (255,255,255)    
                font = ImageFont.truetype(font_path, font_size)
                # For the text background
                # Finds space required by the text so that we can put a background with that amount of width.
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, font_thinkness, 1)
                # Add text backdrop color
                frame = cv2.rectangle(frame, (x1, y1 - text_backdrop_rect_height_offset), (x1 + w, y1), rect_background_color, -1)
                # Add text
                # frame = cv2.putText(frame, label, (x1, y1), font, font_size, text_color, 1)
                
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                frame = draw.text((x1, y1 - font_vertical_offset), label, font = font, fill = (255,255,255,100))
                img = np.array(img_pil)
                frame = img

            if result.boxes and first_image == True:
                image_output_file = ("{}.jpg").format(output_path)
                print(("Saving single frame of first identified object(s) to: {}").format(image_output_file))
                cv2.imwrite(image_output_file, img)
                first_image = False
                if stop_after_first_detect_frame:
                    print(("Stopping detection run for {} since the single frame option is {}.").format(input_path, stop_after_first_detect_frame))
                    return
        
        # Write the frame with annotations to the output video
        if not stop_after_first_detect_frame:
            out.write(frame)

    # Release resources
    cap.release()
    if not stop_after_first_detect_frame:
        out.release()
    print("Processing complete. Output saved to", output_path)

if __name__ == "__main__":
    # Get list of videos in input folder
    input_path = "/input"
    output_path = "/output"
    input_file_list = os.listdir(input_path)
    video_queue = []
    print(("Files and directories in {} : {}").format(input_path, input_file_list))

    # If we want *only* the first obj detect frame sent to file for checking
    if 'SINGLEFRAME' in os.environ:
        if os.environ.get('SINGLEFRAME', "False") == "True":
            stop_after_first_detect_frame = True
            print("ENV VAR SINGLEFRAME is True, will only generate image of first obj detect.")

    for file in input_file_list:
        if file.endswith(VIDEO_FORMATS):
            input_output = [os.path.join(input_path, file), os.path.join(output_path, file)]
            video_queue.append(input_output)
            print(("Found video file at {}").format(os.path.join(input_path, file)))

    for video in video_queue:
        # print(("{} calling {} to {}").format(video, video[0], video[1]))
        process_video(video[0], video[1])
