#!/bin/bash

# Infinite loop to capture images and run YOLOv5 detection
while true; do
    # Generate a timestamp
    TIMESTAMP=$(date +"%Y%m%d%H%M%S")

    # Capture image using libcamera-still and save it with timestamp
    libcamera-still -o /home/admin/YOLOv5_Source/$TIMESTAMP.jpg

    # Run YOLOv5 detect with the captured image
    DETECTION=$(yolov5 detect --source /home/admin/YOLOv5_Source/$TIMESTAMP.jpg)

    # If person is detected, record video for 30 seconds
    if echo $DETECTION | grep -q "person"; then
        # Call the Python script to record video in the background
        python3 record_video.py &

        # Wait for the Python script to finish recording video
        wait

        # Sleep for 10 seconds after video is recorded
        sleep 10
    else
        # If no person detected, wait for 5 seconds before capturing the next image
        sleep 5
    fi
done
