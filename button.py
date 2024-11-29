import RPi.GPIO as GPIO
import subprocess
import time
from lib import image_sender
from PIL import Image
from lib import LCD_2inch4

GPIO.setmode(GPIO.BCM)
button_pin = 26
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_state = 1
image_path = "/home/kubac/ugabuga/pics/button_made.jpg"
command = ["libcamera-jpeg", "--width", "240", "--height", "320", "--output", image_path, "--nopreview", "--timeout", "1", "--immediate"]

# video_path = "/home/kubac/ugabuga/pics/video.mjpeg"
# command = ["libcamera-vid", "--codec", "mjpeg", "--width", "240", "--height", "320", "--output", video_path, "--timeout", "5000", "--nopreview"]

display = LCD_2inch4.LCD_2inch4()
display.Init()
display.clear()
display.bl_DutyCycle(50)

image = Image.new("RGB", (display.width, display.height), "WHITE")

# photo_sender = image_sender.ImageSender(video_path, display, image)
photo_sender = image_sender.ImageSender(image_path, display, image)

# subprocess.Popen(["libcamera-vid", "--codec", "mjpeg", "-o", "/home/kubac/ugabuga/stream.jpg", "--width", "240", "--height", "320", "-t", "99999999999999999999999999min", "-n"])


# preview_sender = image_sender.ImageSender("/home/kubac/ugabuga/stream.jpg")

while True:
    # preview_sender.call()
    # preview_sender.close()
    time.sleep(0.1)
    current_state = GPIO.input(button_pin)

    if previous_state == 1 and current_state == 0:
        subprocess.run(command)
        time.sleep(0.1)
        photo_sender.call()
        previous_state = 0

    if current_state != previous_state:
        previous_state = current_state
