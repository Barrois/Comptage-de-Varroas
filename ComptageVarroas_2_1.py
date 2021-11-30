  
print("tout debut")
# http://sammy76.free.fr/conseils/informatique/opencv.html
# http://www.tsdconseil.fr/log/opencv/demo/list/index.html
import time
from time import sleep
import cv2
import imutils
# image = cv2.imread('Michel_3_30%.jpg') # et 500>cv2.contourArea(c)>50  donne 72
# image = cv2.imread('Michel_2.jpg')     # et 400>cv2.contourArea(c)>70  donne 70 
# image = cv2.imread('Michel_1.jpg')     # et 500>cv2.contourArea(c)>50  donne 68
 
def comptage() :
	# lire l'image 
	image = cv2.imread('Michel_1.jpg')
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
	cv2.imwrite('final.jpg',final)
	cv2.imshow('final', final)
	cv2.waitKey(0)
	return compteur
#flouter image -> faire une moyenne des pixels   
	# cv2.image('grayscale.jpg',gray)                  # sauve l'image format nuance de gris
#determine les contours       
	#cv2.image('flougaussien.jpg',flougaussien)	 # sauve l'image format flougaussien
#ajoute dans une liste les contours qu'ils trouvent suivant les methodes de recherche                      
    #calcul le perimetre des contours trouves (non fermes)     
                                                                  
nbVarroas = comptage()
print("Nombre de varroas  : ")
print(nbVarroas)

# import everything from tkinter module
# from tkinter import *

# import messagebox from tkinter module
# import tkinter.messagebox
# tkinter.messagebox.showinfo("Nombre de varroas  : ",  nbVarroas)  
import tkinter
from tkinter import messagebox
top =  tkinter.Tk()
top.geometry("150x150")
messagebox.showinfo("Nombre de varroas  : ",  nbVarroas)
top.mainloop()


