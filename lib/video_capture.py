import subprocess
import threading
import time
import logging
import datetime
import io
from PIL import Image

class VideoCapture:
    def __init__(self, lcd_display):
        self.lcd = lcd_display
        self._running = False
        self._capture_thread = None
        
    def _capture_video(self):
        while self._running:
            try:
                cmd = [
                    "libcamera-vid",
                    "--codec", "mjpeg",
                    "--width", "240",
                    "--height", "320",
                    "--output", "-",
                    "--nopreview",
                    "--framerate", "24",  # Increased framerate
                    "--inline",           # Optimize for streaming
                    # "--tune", "zerolatency",  # Optimize for low latency
                    "--segment", "1",     # Split output into 1ms segments
                    "--flush", "1"        # Flush buffers quickly
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    bufsize=0  # No buffering
                )
                
                frame_buffer = b''
                frame_counter = 0
                
                while self._running:
                    chunk = process.stdout.read(4096)
                    if not chunk:
                        break
                        
                    frame_buffer += chunk
                    
                    # Find JPEG markers in buffer
                    start = frame_buffer.find(b'\xff\xd8')
                    end = frame_buffer.find(b'\xff\xd9')
                    
                    if start != -1 and end != -1:
                        jpeg = frame_buffer[start:end + 2]
                        frame_buffer = frame_buffer[end + 2:]
                        
                        frame_counter += 1
                        if frame_counter % 2 == 0:  # Process every second frame
                            try:
                                image = Image.open(io.BytesIO(jpeg))
                                self.lcd.ShowImage(image)
                            except Exception as e:
                                logging.error("Error displaying frame: %s", str(e))
                
                process.terminate()
                    
            except Exception as e:
                logging.error("Error in capture thread: %s", str(e))
                time.sleep(0.1)

    def start(self):
        """Start video capture and display"""
        logging.info("Starting video capture at %s", datetime.datetime.now())
        self._running = True
        self._capture_thread = threading.Thread(target=self._capture_video)
        self._capture_thread.daemon = True  # Make thread daemon for better cleanup
        self._capture_thread.start()

    def stop(self):
        """Stop video capture"""
        logging.info("Stopping video capture at %s", datetime.datetime.now())
        self._running = False
        if self._capture_thread:
            self._capture_thread.join(timeout=1.0)  # Add timeout to avoid hanging
        self.lcd.clear()

