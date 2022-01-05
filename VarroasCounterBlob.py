#!/usr/bin/env python3
# encoding: utf-8

import sys,os,json,requests
import time
from time import sleep
import cv2
import imutils
import numpy as np


try:
    filename = sys.argv[1]
    name, ext = os.path.splitext(sys.argv[1])
    output = name + '_final' + ext
    data = {'filename': filename, 'output': output, 'count': 0}
    print("fichier:", filename)
    print("final:", output)
    print(json.dumps(data))
except IndexError:
    print("missing filename")
    sys.exit()

# Ancienne méthode
def comptage() :
	# lire l'image
	image = cv2.imread(filename)
	# ecricre ses dimensions
	print('Dimensions de l image de départ              :', image.shape)
	# transforme e nuance de gris
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# fait un flougaussien
	flougaussien = cv2.bilateralFilter(gray, 6, 157,157)
	#determine les contours
	edge = imutils.auto_canny(flougaussien)
	# calcul le perimetre des contours trouves (non fermes)
	(cnts,_) = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	compteur = 0
	for i in cnts:
		if (10000>cv2.contourArea(i)>40):
			compteur += 1
	final = cv2.drawContours(image, cnts, -1, (0,255,0), 1)
	cv2.imwrite(output,final)

	return compteur

def analyse(filename, parameters):

	workingImage = cv2.imread(filename)

	# traitement de l'image en nuance de gris
	# workingImage = cv2.cvtColor(workingImage1, cv2.COLOR_BGR2GRAY)
	# fait un flougaussien
	# workingImage = cv2.bilateralFilter(workingImage1, 18, 90,100)       # initialement à 6 , 157 , 157

	a,b,c,d,e,f,g,h=parameters
	print(f'minThreshold:{a} maxThreshold:{b} blobColor:{c} minArea:{d} maxArea:{e} minCircularity:{f} minConvexity:{g} minInertiaRatio:{h} ')
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


	cv2.imwrite(output,im_with_keypoints)
	nb_varroas=len(keyPoints)


	return nb_varroas,im_with_keypoints,workingImage



minThreshold = 99
maxThreshold = 168
blobColor = 0
minArea = 117
maxArea = 134
minCircularity = 79
minConvexity = 75
minInertiaRatio = 50
parameters=(minThreshold,maxThreshold,blobColor,minArea,maxArea,minConvexity,minConvexity,minInertiaRatio)


nbVarroas,im_with_keypoints,workingImage=analyse(filename,parameters)



# nbVarroas = comptage()


data['count'] = nbVarroas
data['image_height'] = workingImage.shape[0]
data['image_width'] = workingImage.shape[1]
# r = requests.post('https://varroacounter.jodaille.org/counter-results', json=json.dumps(data))
print(json.dumps(data))
# print(r)
