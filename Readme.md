# Video Object Identifier With Markup
## Description
Modifies videos, adding boundary boxes and notes what is identified within frames of the input videos.

## Pre-requisites
1. docker
2. docker compose

## Prep Before Running
1. Grab a yolov8 object detection model and place in `./resources`. Using `yolov8s.pt` is recommended since it's small and fast. If using an alternate model, update the `analyze.env` file to note the new model name. Model source location: https://github.com/ultralytics/assets/releases/

## Usage
1. Clone this repo locally.
2. Navigate to the repo within your system shell. Ensure the `Prep Before Running` steps are completed.
3. Edit the value for SINGLEFRAME in .env to `"True"` or `"False"` depending on desired behavior (see "SINGLEFRAME Usage" below).
4. Place the video files which you would like to have processed within the `./input` subdirectory. Each video here in `.mov` or `.mp4` format will be processed, annotated, and exported to `./output/`.
5. Execute `docker compose up`. This will create the container, begin video analysis and show progress in your terminal. Alternatively, run with `docker compose up -d` to run in detached mode, and follow up with `docker compose logs --follow` to see log output.

## SINGLEFRAME Usage
Since analyzing videos often takes a considerable amount of time, the ENV VAR `SINGLEFRAME` can be set to only have the program create a single picture of the first identified object. Set this to `"True"` to create just a single image instead of analyzing the whole video and creating a new video, or keep as `"False"` for default behavior. The video will be analyzed up to the point where it identifies an object. 

## Visual Options
The `analyze.env` file has many options for altering the visuals associated with the presentation of object detection on the outputted files. 

| Variable                     | Description                                                         | Default Value |
|------------------------------|---------------------------------------------------------------------|---------------|
| FONTSIZE                     | Set the size of the font                                            | 76            |
| RECTBACKGROUNDWIDTHMULTIPLIER| Used in the calculation of the width of the box behind text         | 6             |
| TEXTBACKDROPRECTVERTOFFSET   | Used in the calculation of the vert placement of the box behind text| 95            |
| FONTCOLORR                   | Determine the text's Red value (R, in RGB)                          | 255           |
| FONTCOLORG                   | Determine the text's Green value (G, in RGB)                        | 255           |
| FONTCOLORB                   | Determine the text's Blue value (B, in RGB)                         | 255           |
| TEXTBACKDROPRECTHEIGHT       | Used in the calculation of the height of the box behind text        | 80            |
| RECTBACKGROUNDCOLORR         | Determine the Red value (R, in RGB) of the box placed behind text   | 0             |
| RECTBACKGROUNDCOLORG         | Determine the Green value (G, in RGB) of the box placed behind text | 0             |
| RECTBACKGROUNDCOLORB         | Determine the Blue value (B, in RGB) of the box placed behind text  | 0             |

## TO DO
I only really tested this with 1080x1920 (Vertical video for Instagram upload), so the weight/color of the boundary boxes and size/color of font/font backgrounds are as I wanted them. Your use case likely leverages different sized video, so my choices may be way out of whack. Play with these values in the `analyze.env` file to tweak these settings.