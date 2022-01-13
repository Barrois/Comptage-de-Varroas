#!/usr/bin/env python3
# encoding: utf-8

import sys,os,json
import time
from time import sleep
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
f, (ax1, ax2) = plt.subplots(1, 2) # create subplots

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
# https://www.codetd.com/en/article/12003434	
#print ('type x,y,srcW,refW,srcH,refH', x,type(x),y,type(y),srcW,type(srcW),refW,type(refW),srcH,type(srcH),refH,type(refH))
def addWeightedSmallImgToLargeImg(largeImg,alpha,smallImg,beta,gamma=0.0,regionTopLeftPos=(0,0)):
	srcW, srcH = largeImg.shape[1::-1]
	refW, refH = smallImg.shape[1::-1]
	y,x =  regionTopLeftPos
	print ('type x,y,srcW,refW,srcH,refH', x,type(x),y,type(y),srcW,type(srcW),refW,type(refW),srcH,type(srcH),refH,type(refH))
	if (refW>srcW) or (refH>srcH):
		#raise ValueError("img2's size must less than or equal to img1")
		raise ValueError(f"img2's size {smallImg.shape[1::-1]} must less than or equal to img1's size {largeImg.shape[1::-1]}")
	else:
		if (x+refW)>srcW:
			x = str(srcW-refW)
		if (y+refH)>srcH:
			y = str(srcH-refH)
		destImg = np.array(largeImg)
		x1 = int(x)
		y1 = int(y)
		x2 = int(x)+refW
		y2 = int(y)+refH
		print ('print 1 x1,x2,y1,y2', x1,type(x1),x2,type(x2),y1,type(y1),y2,type(y2))				
		tmpSrcImg = destImg[y1:y2,x1:x2]
		tmpImg = cv2.addWeighted(tmpSrcImg, alpha, smallImg, beta,gamma)
		destImg[y1:y2,x1:x2] = tmpImg
		return destImg

# Méthode : Villeurbanne
def comptage(image) :
	# lire l'image
	image = cv2.imread('final_blank_image.jpg')
	# ecrire ses dimensions
	print('Dimensions de l image de départ              :', image.shape)
	# transforme e nuance de gris
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# fait un flougaussien
	flougaussien = cv2.bilateralFilter(gray, 6, 157,157)
	#determine les contours
	edge = imutils.auto_canny(flougaussien)
	# calcul le perimetre des contours trouves (non fermes)
	(cnts,_) = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	print (" debut")
	borne_sup_sup = 1000
	borne_sup_inf = 700	
	#print(" borne_sup_sup = ",borne_sup_sup, " borne_sup_inf = ",borne_sup_inf)
	borne_inf_sup = 30
	borne_inf_inf = 20	
	#print(' borne_inf_sup = ',borne_inf_sup, ' borne_inf_inf = ',borne_inf_inf)
	for j in range(borne_sup_inf,borne_sup_sup,10):	
		for jj in range(borne_inf_inf,borne_inf_sup,1):				
				compteur = 0
				for i in range(len(cnts)):
					area = cv2.contourArea(cnts[i])
					if ( j>area>jj ):# initialement 120>area> 80
						compteur += 1 
						final = cv2.drawContours(image, cnts[i], -1, (255,0,0), 1) # entoure les varroas d'un cercle bleu 
	print(' RESULTATS pour ',j,'>area>',jj,'   Nombre de varroas     : ',compteur)
	cv2.imwrite('output.jpg',final)
	return compteur

def analyse(filename, parameters,image_height,image_width,blank_image): # méthode du Blob Vincent-Fabrice-Jody

	workingImage = cv2.imread(filename)

	# traitement de l'image en nuance de gris
	# workingImage1 = cv2.cvtColor(workingImage0, cv2.COLOR_BGR2GRAY)
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
	print(f'A:{a} B:{b} C:{c} D:{d} E:{e} F:{f} G:{g} H:{h} ')
	g1 = cv2.cvtColor(workingImage, cv2.COLOR_BGR2GRAY)

	keyPoints = detector.detect(g1)
	
	nb_varroas=len(keyPoints)

	im_with_keypoints = cv2.drawKeypoints(workingImage, keyPoints, np.array([]), (0, 0, 255),
									  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
									  
	ax1.imshow(im_with_keypoints) # plot 
	# https://stackoverflow.com/questions/35884409/how-to-extract-x-y-coordinates-from-opencv-cv2-keypoint-object/35884644
	# RETREIVE KEYPOINTS COORDINATES AND DRAW MANUALLY
	# Reade these and make numpy array
	pts = np.asarray([[p.pt[0], p.pt[1]] for p in keyPoints])
	cols = pts[:,0]
	rows = pts[:,1]
	ax2.imshow(cv2.cvtColor(workingImage, cv2.COLOR_BGR2RGB))
	ax2.scatter(cols, rows)
	
	# for i in len(keyPoints) :
	# print(int(cols[i]))
	h1 = 8 # demi-largeur du crop
	srcW, srcH = blank_image.shape[1::-1]  # taille de l'image blanche
	tailleW, tailleH = workingImage.shape[1::-1] # taille de l'image d'origine
	print('taille de la page blanche  srcW,srcH : ',srcW,srcH,type(srcH),type(srcH))	
	print('taille de la working tailleW,tailleH : ',tailleW,tailleH,type(tailleW),type(tailleH))	
	print('pts', pts)
	for point  in pts:  # on balaye la liste des varroas détectés : y=point[0] , x =point[1]
		print('position du varroa detecte y,x : ',point)
		b1 = int(point[0]-h1) # coin à gauche 
		if (b1>srcW) :
			b1=srcW
		b2 = int(point[0]+h1) # coin à droite
		if (b2>srcW) :
			b2=srcW				
		a1 = int(point[1]-h1) # coin en haut
		if (a1>srcH) :
			a1=srcH
		a2 = int(point[1]+h1) # coin en bas
		if (a2>srcH) :
			a2=srcH
		print('taille du crop : ',b1,b2,a1,a2)	
		crop_img = workingImage[a1:a2,b1:b2] # découpage d'un carré 2h1x2h1 de l'image d'origine autour du varroa détecté
		print('taille du crop : ',crop_img.shape)
		print('taille image   : ',workingImage.shape)
		y = int(point[0]) - h1 # point d'insertion en y
		x = int(point[1]) - h1 # point d'insertion en x
		print('point insertion y,x : ',y,x,type(y),type(x))			
		refW, refH = crop_img.shape[1::-1]
		print('taille de la page blanche srcW,srcH : ',srcW,srcH,type(srcH),type(srcH))	
		print('taille du crop            refW,refH : ',refW,refH,type(refW),type(refH))	# insertion du crop dans l'image blanche
		blank_image = addWeightedSmallImgToLargeImg(blank_image, 0.01, crop_img, 1,regionTopLeftPos=(x,y))	# !! inversion y,x en x,y !!!

	
	#cv2.imshow('image',blank_image)
	#cv2.waitKey(0)	
	#plt.show()	
	#cv2.imwrite(output,im_with_keypoints) #im_with_keypoints,
	cv2.imwrite('final_blank_image.jpg',blank_image)     # ecrit le fichier  sur le disque 
	scale_percent1 = 25
	width = int(blank_image.shape[1] * scale_percent1 / 100)
	height = int(blank_image.shape[0] * scale_percent1 / 100)
	dsize = (width, height)	
	output = cv2.resize(blank_image, dsize)
	cv2.imshow('image',output) # affiche la page blanche résultat

	plt.show()	# affiche toutes les images présentes
	cv2.waitKey(0)
	return nb_varroas,im_with_keypoints,g1 # workingImage



minThreshold = 99       # 99
maxThreshold = 168      # 168
blobColor = 0           # 0
minArea = 100           # 117
maxArea = 134           # 134
minCircularity = 0.8    # 0.8
minConvexity = 0.7      # 0.7
minInertiaRatio = 0.5   # 0.4
parameters=(minThreshold,maxThreshold,blobColor,minArea,maxArea,minConvexity,minConvexity,minInertiaRatio)

workingImage = cv2.imread(filename)
data['image_height'] = workingImage.shape[0]
data['image_width'] = workingImage.shape[1]

page_blanche = np.zeros((data['image_height'],data['image_width'],3), np.uint8) # fabrication d'une image
page_blanche.fill(255)  # remplit l'image de la couleur blanche

nbVarroas,im_with_keypoints,workingImage=analyse(filename,parameters,workingImage.shape[0],workingImage.shape[1],page_blanche)

print('nbVarroas premier passage : ',nbVarroas)	

nbVarroas = comptage(page_blanche)

print('nbVarroas second passage : ',nbVarroas)	

data['count'] = nbVarroas

# r = requests.post('https://varroacounter.jodaille.org/counter-results', json=json.dumps(data))
print(json.dumps(data))
# print(r)