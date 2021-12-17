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
 
# lit l'image 
image = cv2.imread('CM_Cal_22V_A3_1.jpg')
# écrit ses dimensions
print('Dimensions de l image de départ              :', image.shape)
# transforme en nuance de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# fait un flougaussien
flougaussien = cv2.bilateralFilter(gray, 6, 157,157)
# crée les contours      
edge = imutils.auto_canny(flougaussien) 
# calcule le perimetre des contours trouves (non fermes)     
(cnts,_) = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
#(cnts,contours,hierarchy) = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print (" debut")
borne_sup_sup = 1000
borne_sup_inf = 700
print(" borne_sup_sup = ",borne_sup_sup, " borne_sup_inf = ",borne_sup_inf)
for j in range(borne_sup_inf,borne_sup_sup,10):
	borne_inf_sup = 30
	borne_inf_inf = 20		
	for jj in range(borne_inf_inf,borne_inf_sup,1):
			print(' borne_sup = ',j, ' borne_inf = ',jj)
			compteur = 0
			for i in range(len(cnts)):
				area = cv2.contourArea(cnts[i])
				if ( j>area>jj ):# initialement 120>area> 80
					compteur += 1 
			if compteur in range(70,72):  # Michel_3.jpg
			# if compteur in range(290,300): # Michel_4.jpg
				print(' RESULTATS pour ',j,'>area>',jj,'   Nombre de varroas     : ',compteur)
				
    

# import everything from tkinter module
# from tkinter import *

# import messagebox from tkinter module
# import tkinter.messagebox
# tkinter.messagebox.showinfo("Nombre de varroas  : ",  nbVarroas)  
# import tkinter
# from tkinter import messagebox
# top =  tkinter.Tk()
# top.geometry("150x150")
# messagebox.showinfo("Nombre de varroas  : ",  nbVarroas)
# top.mainloop()


