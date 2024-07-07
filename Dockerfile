FROM python:3.9.19-bullseye

RUN pip install ultralytics onnxruntime-gpu numpy opencv-python pillow
RUN apt-get update
RUN apt-get install -y libgl1

ADD resources /resources
ADD input /input
RUN mkdir /output

WORKDIR /resources

RUN chmod +x /resources/analyze.py

CMD ["python", "./analyze.py"]