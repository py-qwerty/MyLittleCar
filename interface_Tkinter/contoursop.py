import cv2
import numpy as np
import math


def filterCanny (mask):
	kernel = np.ones((3,3),np.uint8)
	mask = cv2.erode(mask,kernel,iterations = 1)
	mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	edged = cv2.Canny(mask,50,150)
	_,cn,_ = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cn

def drawRectangle(im,c,typeOf = False,color=(0,0,255)):
	if typeOf:
		for i in c:
			drawRectangle(im,c,False,color)
	else:
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(im, (x, y), (x + w, y + h), color, 1, cv2.LINE_AA)
		return [x,y,w,h]

def drawCenter(im,c,typeOf=False, color=(0,0,255)):
	if typeOf:
		for i in c:
			drawCenter(im,i,typeOf=False,color=(0,0,255))
	else:
		m = cv2.moments(c)
		am= 4
		si = 1
		if m['m00'] > 0:
			ce = [int(m['m10']/m['m00']),int(m['m01']/m['m00'])]
			cv2.line(im,(ce[0]+am,ce[1]),(ce[0]-am,ce[1]),color,si)
			cv2.line(im,(ce[0],ce[1]+am),(ce[0],ce[1]-am),color,si)
			return ce
	return [0,0]

def MEC (c,im, draw = True):	
	(x,y),radius = cv2.minEnclosingCircle(c)
	center = (int(x),int(y))
	radius = int(radius)
	if draw:
		cv2.circle(im,center,radius,(0,255,0),2)
	area = math.pi*radius**2
	return area
def getRect (self,im,cnt):
	m = [0,0]
	if len(cnt):
		rows,cols = im.shape[:2]
		[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
		m = [vx,vy]
		lefty = int((-x*vy/vx) + y)
		righty = int(((cols-x)*vy/vx)+y)
		im = cv2.line(im,(cols-1,righty),(0,lefty),(0,255,0),2)
	return m
	
	

	
def getColor (im,typeOf):
	if typeOf.lower() == 'dark_blue':
		low = np.array([0, 70, 50],dtype= np.uint8)
		high = np.array([130,255,255],dtype=np.uint8)
	if typeOf.lower() == 'white':
		low = np.array([0,0,200],dtype= np.uint8)
		high = np.array([255,255,255],dtype=np.uint8)
	if typeOf.lower() == 'light_red':
		low = np.array([150,65,75],dtype= np.uint8)
		high = np.array([254,255,255],dtype=np.uint8)
	if typeOf.lower() == 'dark_red':
		low = np.array([100,65,75],dtype= np.uint8)
		high = np.array([130,255,255],dtype=np.uint8)
	if typeOf.lower() == 'blue':
		low = np.array([78,158,124],dtype= np.uint8)
		high = np.array([138,255,255],dtype=np.uint8)     
	if typeOf.lower() == 'green':
		low = np.array([49,50,50],dtype= np.uint8)
		high = np.array([80, 255, 210],dtype=np.uint8)
	if typeOf.lower() == 'black':
		low = np.array([0,0,0],dtype= np.uint8)
		high = np.array([0, 0, 0],dtype=np.uint8)
	hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,low,high)
	cn = filterCanny(mask)
	return (cn,mask)

def getObOfCn(im,cn):
	ob=[]
	for c in cn:
		center = drawCenter(im,c)
		try:
			ob.append(center)
		except:
			print('Error to take de coors')
	return ob

def detectShape (im,c):
	shape = 'unidentified'
	peri = cv2.arcLength(c,True)
	approx = cv2.approxPolyDP(c,0.04*peri,True)
	if len(approx) == 3:
		shape = 'Triangle'
	elif len(approx) == 4:
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w/float(h)
		if ar >= 0.95 and ar <= 1.1:
			shape =  'Square'
		else:
			shape = 'Rectangle'
	elif len(approx) >= 5:
		shape = 'Circle'
	return shape


		

	
