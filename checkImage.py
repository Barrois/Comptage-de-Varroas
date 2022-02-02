#!/usr/bin/env python3
# encoding: utf-8


import sys,os,json,requests
import time
from time import sleep
import cv2
import collections
import imutils
import math
import numpy as np
from pathlib import Path

def resizeMilleCinqCentTrente(image):
    win_name = "visualization"  #  1. use var to specify window name everywhere
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  #  2. use 'normal' flag

    destinationwidth = 1530
    destinationheight = 2106
    windowH = 1053
    windowW = 765

    dim = (destinationwidth, destinationheight)

    height  = image.shape[0]
    width = image.shape[1]
    smallest = width


    if (height < width):
        smallest = height
        dim = (destinationheight, destinationwidth)
        windowH = 765
        windowW = 1053

    print("smallest: ", smallest)
    if (smallest > 1530):
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        cv2.resizeWindow(win_name, windowW, windowH)  #  use variables defined/computed BEFOREHAND
        cv2.imshow(win_name, resized)
        cv2.waitKey(0)

try:

    # need script path to find crops images
    dirpath = Path(__file__).parent.absolute()
    dirpath = str(dirpath)
    print("Directory Path:", dirpath)
    filename = sys.argv[1]

    name, ext = os.path.splitext(sys.argv[1])

    workingImage = cv2.imread(filename)
    output = name + '_final' + ext
    data = {'filename': filename, 'output': output, 'count': 0, 'image_height':workingImage.shape[0], 'image_width': workingImage.shape[1]}
    print("fichier:", filename)
    print("final:", output)
    print(json.dumps(data))
    resizeMilleCinqCentTrente(workingImage)
except IndexError:
    print("missing filename")
    sys.exit()