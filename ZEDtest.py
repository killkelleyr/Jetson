import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum



# Create a ZED camera object
zed = sl.Camera()

# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD1080
init_params.camera_fps = 30

# Enable recording with the filename specified in argument
path_output = sys.argv[0]
err = zed.enable_recording(path_output, sl.SVO_COMPRESSION_MODE.SVO_COMPRESSION_MODE_LOSSLESS)

def main():
    print("Running...")
    init = sl.InitParameters()
    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

# Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(-1)

    while exit_app :
        if zed.grab() == sl.ERROR_CODE.SUCCESS :
            # Each new frame is added to the SVO file
            zed.record()

# Disable recording
zed.disable_recording()

if __name__ == "__main__":
    main()
