import time

from libcamera import Transform
from picamera2 import Picamera2, Preview

with Picamera2() as picam2:
    picam2.start_preview(Preview.QTGL, transform=Transform(hflip=1))
    picam2.start()
    time.sleep(10)
