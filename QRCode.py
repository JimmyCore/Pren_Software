
from time import sleep

import cv2
import numpy as np
from pyzbar.pyzbar import decode
from urllib.parse import unquote

from imutils.video.pivideostream import PiVideoStream

camera = PiVideoStream(resolution=(1024, 752), framerate=60, iso=500).start()
sleep(2)

while True:
    img = camera.read()
    # detect and decode
    for barcode in decode(img):
        tempmyData = barcode.data.decode('utf-8')
        # Add Rectangle around QR - Code
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        cv2.imwrite("TEST.jpg", img)
        print("ERKANNT")
