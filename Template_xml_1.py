# détecte trois fois avec trois images de varroas différentes crop_3, crop_25 et crop_89
# MAIS il ne décompte qu'une fois les varroas grace à la fonction count(listOfTuple) 
import cv2
import numpy as np
import math
import collections


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
def detect_crop (filecrop,image_avant,couleur1,couleur2,couleur3,cmp) :
    template = cv2.imread(filecrop, cv2.IMREAD_UNCHANGED)
    hh, ww = template.shape[:2]
    # extract pawn base image and alpha channel and make alpha 3 channels
    pawn = template[:,:,0:3] # pawn = le piont 
    alpha = template[:,:,0]  # pourquoi 2 ? au lieu de 3 ??? et en plus ce n'est pas un PNG mais ça fonctionne !!
    alpha = cv2.merge([alpha,alpha,alpha]) 
    # do masked template matching and save correlation image 
    corr_img = cv2.matchTemplate(img, pawn, cv2.TM_CCORR_NORMED, mask=alpha) # on utilise l'image de base lu : img
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
            fichier.write('  <object> \n')
            fichier.write('        <name>crop_'+str(cmp)+'</name> \n')
            # fichier.write(' ww : '+str(ww)+' hh '+str(hh)+' max_loc[0] : '+str(max_loc[0])+' max_loc[1]'+str(max_loc[1])+'\n')
            fichier.write('        <pose>Unspecified</pose> \n')
            fichier.write('        <truncated>0</truncated> \n')  
            fichier.write('        <difficult>0</difficult> \n')
            fichier.write('        <bndbox> \n')  
            fichier.write('             <xmin>'+str(max_loc[0])+'</xmin> \n')  
            fichier.write('             <ymin>'+str(max_loc[1])+'</ymin> \n') 
            fichier.write('             <xmax>'+str(max_loc[0]+ww)+'</xmax> \n')  
            fichier.write('             <ymax>'+str(max_loc[1]+hh)+'</ymax> \n')
            fichier.write('        </bndbox> \n')  
            fichier.write('  </object> \n')  
            cmp  +=1
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
    return aa,result,cmp

# set threshold
threshold = 0.992
# read  image
filename = 'Michel1530_3'
# img = cv2.imread('Michel1530_3.JPG') # Michel1530_3.jpg CM_10v_1.JPG
img = cv2.imread(filename+'.jpg')
ww_img = int(img.shape[1])
hh_img = int(img.shape[0])

# on écrit le chapeau du fichier xml
fichier = open(filename+'.xml', 'a')
# texte chapeau   f.write(str(123) + '\n')
fichier.write('  <annotation> \n')
fichier.write('    <folder>Documents</folder> \n')
fichier.write('    <filename>' +filename+'.JPG</filename> \n')
fichier.write('    <path>/home/pi/Documents/' +filename+'.JPG</path> \n')
fichier.write('    <source>} \n')
fichier.write('         <database>Unknown</database> \n')
fichier.write('    </source>} \n')
fichier.write('    <size>} \n')
fichier.write('          <width>'+str(ww_img)+'</width> \n')
fichier.write('          <height>'+str(hh_img)+'</height> \n')
fichier.write('          <depth>3</depth> \n')
fichier.write('    </size> \n')
fichier.write('    <segmented>0</segmented> \n')
cmpt = 0  # compteur pour les crop de varroas détectés
#'crop_3.jpg'
a0,retour_0,cmpt = detect_crop('crop_3.jpg',img,0,255,0,cmpt) 

# 'crop_25.jpg'
a1,retour_1,cmpt = detect_crop('crop_25.jpg',retour_0,255,0,0,cmpt)

#'crop_89.jpg'
a2,retour_2,cmpt = detect_crop('crop_89.jpg',retour_1,0,0,255,cmpt)

#'crop_22.jpg'
a3,retour_3,cmpt = detect_crop('crop_22.jpg',retour_2,255,0,255,cmpt)

#'crop_59jpg'
a4,retour_4,cmpt = detect_crop('crop_59.jpg',retour_3,255,255,0,cmpt)

# décompte avec suppression des doublons 
listOfTuple = (a0+a1+a2+a3+a4)
uniqueList = count(listOfTuple) 



# sauvegarde de la dernière image
cv2.imwrite('resultat_Template_xml.jpg', retour_4)

# mySet = set(a0+a1+a2+a3+a4) # la fonction SET élimine les doublons de la liste (un peu simpliste)
print('Fichier : ',filename,' Seuil : ',threshold, ' Nombre de varroas vraiment détectés    : ',len(uniqueList))

output = mon_resize(retour_4,40)
cv2.imshow('resultat_0',output)
cv2.waitKey(0)
cv2.destroyAllWindows()




