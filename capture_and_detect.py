import subprocess
import time
import datetime

def capture_image(timestamp):
    # Capture image using libcamera-still and save it with timestamp
    image_path = f"/home/admin/YOLOv5_Source/{timestamp}.jpg"
    libcamera_command = f"libcamera-still -o {image_path}"
    subprocess.run(libcamera_command, shell=True)
    return image_path

def detect_person(image_path, output_path):
    # Run YOLOv5 detect with the captured image, get the results, and save them to a file and check if a person is detected
    detect_command = f"python3 detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source {image_path} --save-txt --save-conf --exist-ok --project /home/admin/YOLOv5_Source --name {timestamp}"
    subprocess.run(detect_command, shell=True)
    with open(output_path, 'r') as f:
        detection_results = f.read()
    if "person" in detection_results:
        print("Person detected.")
        # Record video for 30 seconds
        video_path = record_video(timestamp)
        print("Video recorded.")
    else:
        print("No person detected.")
        
   

    

def record_video(timestamp):
    # Record video for 30 seconds
    video_path = f"/home/admin/YOLOv5_Source/{timestamp}.mp4"
    record_command = f"libcamera-vid -t 30000 -o {video_path}"
    subprocess.run(record_command, shell=True)
    return video_path

if __name__ == "__main__":
    while True:
        # Generate a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print(f"Capturing image at timestamp: {timestamp}")

        # Capture image using libcamera-still
        image_path = capture_image(timestamp)
        print("Image captured.")

        # Define the output path for the YOLOv5 detection results
        detection_output_path = f"/home/admin/YOLOv5_Source/{timestamp}_detection_results.txt"

        # Check if a person is detected
        detect_person(image_path, detection_output_path)
        
        # Read the detection results from the output file
        with open(detection_output_path, "r") as output_file:
            detection_results = output_file.read()
        
        if "Person" in detection_results:
            print("Person detected.")
            # Record video in the background
            video_path = record_video(timestamp)
            print("Video recording started.")

            # Wait for the video recording to complete (30 seconds)
            time.sleep(30)
            print("Video recording completed.")
        else:
            print("No person detected.")

        # Wait for 5 seconds before capturing the next image
        time.sleep(5)
