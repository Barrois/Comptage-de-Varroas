#!/usr/bin/env python3
# encoding: utf-8

import sys,os,json,requests
import time
from time import sleep
import cv2
import imutils

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


nbVarroas = comptage()

data['count'] = nbVarroas
r = requests.post('http://varroacounter.jodaille.org/counter-results', json=json.dumps(data))
print(json.dumps(data))
print(r)
