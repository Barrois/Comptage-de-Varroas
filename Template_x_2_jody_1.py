#!/usr/bin/env python3
# encoding: utf-8

# détecte trois fois avec trois images de varroas différentes crop_3, crop_25 et crop_89
# MAIS il ne décompte qu'une fois les varroas grace à la fonction count(listOfTuple)

import sys,os,json,requests
import time
from time import sleep
import cv2
import collections
import imutils
import math
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

def count(listOfTuple):
    flag = False
    val = collections.Counter(listOfTuple)
    uniqueList = list(set(listOfTuple))
    for i in uniqueList:
        if val[i]>= 2:
            flag = True
            # print(i, "-", val[i])
    if flag == False:
        print("Duplicate doesn't exist")
    return uniqueList

def mon_resize (image,taille):
	width = int(image.shape[1] * taille / 100)
	height = int(image.shape[0] * taille / 100)
	dsize = (width, height)
	output = cv2.resize(image, dsize)
	return output

# https://stackoverflow.com/questions/61779288/how-to-template-match-a-simple-2d-shape-in-opencv
def detect_crop (filecrop,image_avant,couleur1,couleur2,couleur3,img_0) :
    template = cv2.imread(filecrop, cv2.IMREAD_UNCHANGED)
    hh, ww = template.shape[:2]
    # extract pawn base image and alpha channel and make alpha 3 channels
    pawn = template[:,:,0:3] # pawn = le piont
    # cv2.imshow('pawn',pawn)
    # cv2.waitKey(0)
    alpha = template[:,:,0]  # pourquoi 2 ? au lieu de 3 ???
    # cv2.imshow('alpha',alpha)
    # cv2.waitKey(0)
    alpha = cv2.merge([alpha,alpha,alpha])
    # cv2.imshow('alpha merge',alpha)
    # cv2.waitKey(0)
    # do masked template matching and save correlation image
    corr_img = cv2.matchTemplate(img_0, pawn, cv2.TM_CCORR_NORMED, mask=alpha) # on utilise l'image de base lu : img
    # search for max score
    result = image_avant.copy()  # sauvegarde de l'image avant => on utilise result
    max_val = 1
    rad = int(math.sqrt(hh*hh+ww*ww)/4)
    aa = []
    while max_val > threshold:
        # find max value of correlation image
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corr_img)
        # print(max_val, max_loc_0)
        aa.append(max_loc)  # on compte les varraos détectés
        if max_val > threshold:
            # draw match on copy of input encadre les varraos trouvés
            cv2.rectangle(result, max_loc, (max_loc[0]+ww, max_loc[1]+hh), (couleur1,couleur2,couleur3), 2)
            # write black circle at max_loc in corr_img
            cv2.circle(corr_img, (max_loc), radius=rad, color=0, thickness=cv2.FILLED)
        else:
            break
    print('fichier template :' , filecrop, ' Nombre de varroas vus : ',len(aa))
    # cv2.imwrite('corr_img.jpg', corr_img)
    # output = mon_resize(alpha,40)
    # cv2.imshow('resultat_0',output)
    # cv2.waitKey(0)
    # output = mon_resize(result,40)
    # cv2.imshow('resultat_0',output)
    # cv2.waitKey(0)
    return aa,result

# set threshold
threshold = 0.992
# read  image

# img = cv2.imread('Michel1530_3.JPG') # Michel1530_3.jpg CM_10v_1.JPG
workingImage = cv2.imread(filename)
img_de_base = workingImage

#'crop_3.jpg'
a0,retour_0 = detect_crop('crop_3.jpg',workingImage,0,255,0,img_de_base)

# 'crop_25.jpg'
a1,retour_1 = detect_crop('crop_25.jpg',retour_0,255,0,0,img_de_base)

#'crop_89.jpg'
a2,retour_2 = detect_crop('crop_89.jpg',retour_1,0,0,255,img_de_base)

#'crop_22.jpg'
a3,retour_3 = detect_crop('crop_22.jpg',retour_2,255,0,255,img_de_base)

#'crop_59jpg'
a4,retour_4 = detect_crop('crop_59.jpg',retour_3,255,255,0,img_de_base)

# décompte avec suppression des doublons
listOfTuple = (a0+a1+a2+a3+a4)
uniqueList = count(listOfTuple)

# sauvegarde de la dernière image
cv2.imwrite(output, retour_4)

nbVarroas = len(uniqueList)
# mySet = set(a0+a1+a2+a3+a4) # la fonction SET élimine les doublons de la liste (un peu simpliste)
print('Fichier : ',filename,' Seuil : ',threshold, ' Nombre de varroas vraiment détectés    : ',len(uniqueList))


data['count'] = nbVarroas
data['image_height'] = workingImage.shape[0]
data['image_width'] = workingImage.shape[1]
# r = requests.post('https://varroacounter.jodaille.org/counter-results', json=json.dumps(data))
print(json.dumps(data))
# print(r)

# output = mon_resize(retour_4,40)
# cv2.imshow('resultat_0',output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
