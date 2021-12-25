#!/usr/bin/env python
import cv2
import numpy as np
import sys
import time
import imutils
waitTime = 33
def nothing(x):
    pass

def analyse(name, parameters):

	workingImage = cv2.imread(name)

	# traitement de l'image en nuance de gris
	# workingImage = cv2.cvtColor(workingImage1, cv2.COLOR_BGR2GRAY)
	# fait un flougaussien
	# workingImage = cv2.bilateralFilter(workingImage1, 18, 90,100)       # initialement à 6 , 157 , 157

	a,b,c,d,e,f,g,h=parameters
	print(f'A:{a} B:{b} C:{c} D:{d} E:{e} F:{f} G:{g} H:{h} ')
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = a          #  = 15   #  original 10
	params.maxThreshold = b          #  = 180  #  original 200
	params.filterByColor  = True
	params.blobColor  = c            # blobColor = 0 sombre / blobColor = 255 clair
	params.filterByArea = True
	params.minArea = d               #  23 mais avec une marge  50
	params.maxArea = e               # 120 mais avec marge     150
	params.filterByCircularity = True
	params.minCircularity = f        # params.minCircularity = 0.1
	params.filterByConvexity = True
	params.minConvexity = g          # params.minConvexity = 0.69
	params.filterByInertia = True
	params.minInertiaRatio = h       # params.minInertiaRatio = 0.52

	detector = cv2.SimpleBlobDetector_create(params)

	g = cv2.cvtColor(workingImage, cv2.COLOR_BGR2GRAY)

	keyPoints = detector.detect(g)

	im_with_keypoints = cv2.drawKeypoints(workingImage, keyPoints, np.array([]), (0, 0, 255),
									  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	nb_varroas=len(keyPoints)
	return nb_varroas,im_with_keypoints

# Create a window
cv2.namedWindow('image')
cv2.namedWindow('imageResult')

# create trackbars for color change
cv2.createTrackbar('minThreshold','image',150,200,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('maxThreshold','image',200,250,nothing)
cv2.createTrackbar('blobColor','image',0,255,nothing)
#cv2.setTrackbarPos('blobColor', 'image', 0) 
cv2.createTrackbar('minArea','image',135,137,nothing)
cv2.createTrackbar('maxArea','image',153,155,nothing)
cv2.createTrackbar('minCircularity_x100','image',0,100,nothing) #0.7,0.9 Circularity : un cercle a une circularité de 1, la circularité d'un carré est de 0,785,
cv2.createTrackbar('minConvexity_x100','image',0,100,nothing)   #0.1,0.2 Convexity : Aire du Blob / Aire de son enveloppe convexe  1.38/2 =0.69
cv2.createTrackbar('minInertiaRatio_x100','image',0,100,nothing)#0.1,0.2 Inertia : pour un cercle : 1, par une ellipse compris entre 0 et 1, pour une ligne : 0

img = cv2.imread(sys.argv[1])
output = img

while(1):

    # get current positions of all trackbars
    minThreshold = cv2.getTrackbarPos('minThreshold','image')
    maxThreshold = cv2.getTrackbarPos('maxThreshold','image')
    blobColor = cv2.getTrackbarPos('blobColor','image')
    minArea = cv2.getTrackbarPos('minArea','image')
    maxArea = cv2.getTrackbarPos('maxArea','image')
    minCircularity = 0.01*cv2.getTrackbarPos('minCircularity_x100','image')
    minConvexity = 0.01*cv2.getTrackbarPos('minConvexity_x100','image')
    minInertiaRatio = 0.01*cv2.getTrackbarPos('minInertiaRatio_x100','image')
	
    parameters=(minThreshold,maxThreshold,blobColor,minArea,maxArea,minConvexity,minConvexity,minInertiaRatio)

    _,im_with_keypoints=analyse(sys.argv[1],parameters) 
    cv2.imshow('image',img)
    cv2.imshow('imageResult',im_with_keypoints)
    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(waitTime) & 0xFF == ord('q'):
        break