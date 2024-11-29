'''
import RPi.GPIO as GPIO
import subprocess
import time
from lib import image_sender

GPIO.setmode(GPIO.BCM)
button_pin = 26
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_state = 1
image_path = "/home/kubac/ugabuga/pics/button_made.jpg"
command = ["libcamera-jpeg", "--width", "240", "--height", "320", "--output", image_path, "--nopreview"]
photo_sender = image_sender.ImageSender(image_path)

# subprocess.Popen(["libcamera-vid", "--codec", "mjpeg", "-o", "/home/kubac/ugabuga/stream.jpg", "--width", "240", "--height", "320", "-t", "99999999999999999999999999min", "-n"])


# preview_sender = image_sender.ImageSender("/home/kubac/ugabuga/stream.jpg")

while True:
    # preview_sender.call()
    # preview_sender.close()
    time.sleep(0.1)
    current_state = GPIO.input(button_pin)

    if previous_state == 1 and current_state == 0:
        subprocess.run(command)
        time.sleep(1)
        photo_sender.call()
        previous_state = 0

    if current_state != previous_state:
        previous_state = current_state
'''

import RPi.GPIO as GPIO
import subprocess
import time
from lib import image_sender

GPIO.setmode(GPIO.BCM)
button_pin = 26
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_state = 1
image_path = "/home/kubac/ugabuga/pics/button_made.jpg"
preview_path = "/home/kubac/ugabuga/pics/preview.jpg"
capture_command = ["libcamera-jpeg", "--width", "240", "--height", "320", "--output", image_path, "--nopreview"]
preview_command = ["libcamera-jpeg", "--width", "240", "--height", "320", "--output", preview_path, "--nopreview"]

photo_sender = image_sender.ImageSender(image_path)
preview_sender = image_sender.ImageSender(preview_path)

while True:
    # Take and display preview
    subprocess.run(preview_command)
    preview_sender.call()
    
    current_state = GPIO.input(button_pin)
    
    if previous_state == 1 and current_state == 0:
        # Take actual photo when button pressed
        subprocess.run(capture_command)
        time.sleep(1)
        photo_sender.call()
        previous_state = 0
    
    if current_state != previous_state:
        previous_state = current_state
    
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
