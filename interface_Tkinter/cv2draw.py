import cv2

def drawPoint(im,ce,amplitude=4,size=1, color=(0,0,255)):
	cv2.line(im,(ce[0]+amplitude,ce[1]),(ce[0]-amplitude,ce[1]),color,size)
	cv2.line(im,(ce[0],ce[1]+amplitude),(ce[0],ce[1]-amplitude),color,size)

def drawLineThro(im,coors,size=1, color=(0,0,255)):
	cv2.line(im,(coors[0][0],coors[0][1]),(coors[1][0],coors[1][1]),color,size)
	
		


