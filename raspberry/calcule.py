import cv2
import numpy
import math

def lookForShor(im,coor,act, draw = True):
	antDis = 0
	save_coor = act
	for i in coor:
		if i != act:
			vec = [i[0]-act[0],i[1]-act[1]]
			dis = math.hypot(vec[0],vec[1])
			if dis<antDis or antDis == 0:
				save_coor = i
				antDis = dis
	if draw:
		cv2.line(im,(save_coor[0],save_coor[1]),(act[0],act[1]),(255,0,255),2)
	return save_coor



#--------Calculo del centro de la pantalla----------#
def getMidel(im,size,draw1 = True,draw2=False,rec=(3,3),color=(255,255,0)):
	am= 10
	si = 2
	WIDTH,HEIGHT= size[0],size[1]
	ce = [int(WIDTH/2-si/2),int(HEIGHT/2-si/2)]
	if draw1:
		cv2.line(im,(ce[0]+am,ce[1]),(ce[0]-am,ce[1]),color,si)
		cv2.line(im,(ce[0],ce[1]+am),(ce[0],ce[1]-am),color,si)
	if draw2:
		cv2.rectangle(im, (ce[0]-rec[0], ce[1]-rec[1]), (ce[0] + rec[0], ce[1] + rec[1]), color, 1, cv2.LINE_AA)
	return ce

