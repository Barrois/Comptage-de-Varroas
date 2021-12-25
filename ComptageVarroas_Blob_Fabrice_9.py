#
# This project describes the detection of varroas using opencv's 
# Simple Blob Detector with some arbitrary but seemingly working parameters
#
# version originale de Vincent SAHLER : https://gist.github.com/vsahler/9686d9b12d63bb1f1481aa957bd1933e
#
# documentation : https://learnopencv.com/blob-detection-using-opencv-python-c/
#               : https://docs.opencv.org/3.4/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
#
# rapport entre longueur et largeur de l'ellipse : 1.6 /1.1  surface 1.3816 

import cv2
import numpy as np
import sys
import time
import imutils
import csv;



#names=["./Michel_0_3_1080p.jpg","./Michel_0_4_1080p.jpg","./Image_4_246.jpg","./Image_4_89.jpg","./CM_Cal_22V_A4.jpg","./CM_Cal_50V_A4.jpg"]
#detect_names=["./detect_Michel_0_3_1080p.jpg","./detect_Michel_0_4_1080p.jpg","./detect_Image_4_246.jpg","./detect_Image_4_89.jpg","./detect_CM_Cal_22V_A4.jpg","./detect_CM_Cal_50V_A4.jpg"]
#targets=[71,335,246,89,22,50]
#kii =6

names=["./Michel_0_6.jpg","./Michel_0_7.jpg","./Michel_0_8.jpg"]
detect_names=["./detect_Michel_0_6.jpg","./detect_Michel_0_7.jpg","./detect_Michel_0_8.jpg"]
targets=[4,5,5]
kii =3

#names=["./Michel_0_3_1080p.jpg"]
#detect_names=["./detect_Michel_0_3_1080p.jpg"]
#targets=[71]
#kii =1


# dataset71 = cv2.imread("./Michel_0_3_1080p.jpg")  # 74  /  71 comptés   4% prés  propre
# dataset335 = cv2.imread("./Michel_0_4_1080p.jpg") # 415 / 335 comptés  23% prés  assez sale
# dataset246 = cv2.imread("./Image_4_246.jpg")      # 313 / 246 comptés  27% prés  assez sale
# dataset89 = cv2.imread("./Image_4_89.jpg")        # 100 /  89 comptés  12% prés  assez sale
# datasetCM22 = cv2.imread("./CM_Cal_22V_A4.jpg")   #  21 /  22 comptés   5% prés  propre
# datasetCM30 = cv2.imread("./CM_Cal_30V_A4.jpg")   #   1 /  30 comptés  99% prés  propre !!!
# datasetCM50 = cv2.imread("./CM_Cal_50V_A4.jpg")   #  40 /  50 comptés   5% prés  propre
# datasetCM100 = cv2.imread("./CM_Cal_100V_A4.jpg") #   1 / 100 comptés  99% prés  propre mais flou !!!


# Thresholds
# params.minThreshold = 15   #  original 10
# params.maxThreshold = 180  #  original 200

# Filter by filterByColor  => blobColor = 0 sombre / blobColor = 255 clair
# eviter les taches de pollen 
# params.filterByColor  = True
# params.blobColor  = 10

# Filter by Area
# params.filterByArea = True
# params.minArea = 70   #  23 mais avec une marge  50
# params.maxArea = 110  # 120 mais avec marge     150

# Filter by Circularity : un cercle a une circularité de 1, la circularité d'un carré est de 0,785,
# params.filterByCircularity = True
# params.minCircularity = 0.1  

# Filter by Convexity : Aire du Blob / Aire de son enveloppe convexe  1.38/2 =0.69
# params.filterByConvexity = True
# params.minConvexity = 0.69

# Filter by Inertia # un cercle, cette valeur est 1, par une ellipse , il est compris entre 0 et 1, et pour une ligne est de 0
# params.filterByInertia = True
# params.minInertiaRatio = 0.52

def analyse(ki,parameters):
	name=names[ki]
	target=targets[ki]
	workingImage = cv2.imread(name) 
	
	# traitement de l'image en nuance de gris
	# workingImage = cv2.cvtColor(workingImage1, cv2.COLOR_BGR2GRAY)
	# fait un flougaussien
	# workingImage = cv2.bilateralFilter(workingImage1, 18, 90,100)       # initialement à 6 , 157 , 157
	
	a,b,c,d,e,f,g,h=parameters
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

	im_with_keypoints = cv2.drawKeypoints(workingImage, keyPoints, np.array([]), (0, 0, 255), # vert
									  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	nb_varroas=len(keyPoints)
	return nb_varroas,abs(nb_varroas-target),im_with_keypoints

minv=1000000
mina=[]

A=range(108,109,1)            #Thresholds  = 15   #  original 10  Seuil bas                     
B=range(155,156,1)            #Thresholds  = 180  #  original 200 Seuil haut                   
C=range(0,1,1)                #blobColor                        Color : 0 sombre  et 255 clair  
D=range(109,110,1)            #Area  23 mais avec une marge  50    Aire mini              
E=range(129,130,1)            #Area 120 mais avec marge     150    Aire maxi                
F=np.arange(0.66,0.67,0.1)      #Circularity  = (0.8,1,0.1)    Circularity : un cercle a une circularité de 1, la circularité d'un carré est de 0,785,             
G=np.arange(0.72,0.73,0.1)      #Convexity    = (0.5,0.7,0.1)    Convexity : Aire du Blob / Aire de son enveloppe convexe  1.38/2 =0.69          
H=np.arange(0.44,0.45,0.1)      #InertiaRatio = (0.4,0.6,0.1)    Inertia : pour un cercle : 1, par une ellipse compris entre 0 et 1, pour une ligne : 0
nb_tests = len(A)*len(B)*len(C)*len(D)*len(E)*len(F)*len(G)*len(H)
print(nb_tests,'tests ', time.ctime(), 'duree estimée : ', int(0.5 + nb_tests * 0.1386 / 60) , 'minutes par image sur mon i5 8G') 
# sur mon i5 il faut 0.1386 secondes par itération
	
KI=range(0,kii,1)  # domaine des photos
for ki in KI:    # indice de la photo 
	print('nom de la photo : ', names[ki], ' nb de varroas comptés manuellement :', targets[ki])
	k1=0
	for h in H:
		for g in G:
			for f in F:
				for c in C:
					for b in B:
						for a in A:
							for e in E:
								for d in D:
									if a<b and d<e:
									
										# print(a,b,d,e)
										parameters=(a,b,c,d,e,f,g,h)

										_,diff,im_with_keypoints=analyse(ki,parameters)
										
										if diff<minv:
											minv=diff
											mina=(a,b,c,d,e,f,g,h)
										
										if (k1%100)==0:
											print('.',end='')
											sys.stdout.flush()
										k1+=1

	a,b,c,d,e,f,g,h=mina
	parameters=(a,b,c,d,e,f,g,h)
	nb_varroas,diff,im_with_keypoints=analyse(ki,parameters)
	print(f'A:{a} B:{b} C:{c} D:{d} E:{e} F:{f} G:{g} H:{h} ', nb_varroas, 'varroas détectés  pourcentage : ', int(100*(nb_varroas-targets[ki])/targets[ki]), ' %', time.ctime())
	
	params = cv2.SimpleBlobDetector_Params()
	# Thresholds
	params.minThreshold = a   #  original 10
	params.maxThreshold = b  #  original 200

	# Filter by filterByColor  => blobColor = 0 sombre / blobColor = 255 clair
	# eviter les taches de pollen 
	params.filterByColor  = True
	params.blobColor  = c

	# Filter by Area
	params.filterByArea = True
	params.minArea = d   #  23 mais avec une marge  50
	params.maxArea = e  # 120 mais avec marge     150

	# Filter by Circularity : un cercle a une circularité de 1, la circularité d'un carré est de 0,785,
	params.filterByCircularity = True
	params.minCircularity = f  

	# Filter by Convexity : Aire du Blob / Aire de son enveloppe convexe  1.38/2 =0.69
	params.filterByConvexity = True
	params.minConvexity = g

	# Filter by Inertia : un cercle, cette valeur est 1, par une ellipse , il est compris entre 0 et 1, et pour une ligne est de 0
	params.filterByInertia = True
	params.minInertiaRatio = h

	workingImage = cv2.imread(names[ki])
	detector = cv2.SimpleBlobDetector_create(params)

	g1 = cv2.cvtColor(workingImage, cv2.COLOR_BGR2GRAY)

	keyPoints = detector.detect(g1)

	im_with_keypoints = cv2.drawKeypoints(workingImage, keyPoints, np.array([]), (4, 178, 16),cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
	#									  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	print(f'Il y a : {len(keyPoints)} varroas détectés ')
	print(f'A:{a} B:{b} C:{c} D:{d} E:{e} F:{f} G:{g} H:{h} ', nb_varroas, 'varroas détectés  pourcentage : ', int(100*(nb_varroas-targets[ki])/targets[ki]), ' %', time.ctime())
	detect_names[ki] = cv2.rotate(im_with_keypoints, cv2.cv2.ROTATE_90_CLOCKWISE) # tourne l'image 90° à droite
	cv2.imwrite('final_'+str(ki)+'.jpg',detect_names[ki])     # ecrit le fichier  sur le disque
	print ('  ')
	print ('  ')
	#cv2.imshow('final', detect_names[ki])


cv2.waitKey(0)
cv2.destroyAllWindows()
