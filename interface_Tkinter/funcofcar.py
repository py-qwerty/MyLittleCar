import time
import cv2
import calcule as cl
import os
import math
import contoursop as cnop
import numpy as np
import cv2draw
import serial
import main

class Ardu:
	def __init__(self,src,port):
		self.arduino = serial.Serial('/dev/'+src,port)
		self.theLastInf = ''
	def move(self,data):
		msg = ','.join(str(i) for i in data)
		if not msg == self.theLastInf:
			self.arduino.write(msg+','+'\n')	
		self.theLastInf = msg
ardu = Ardu('ttyUSB0',115200)
try:	
	pass
except:
	ardu = False
	print('No se ha conectado con Arduino Correctamente')
class Control:
	def __init__(self,size):
		self.toSend = [0,0,135,0,0] #--RIGHT-LEFT-SERVO--#
		self.act = 'S'
		self.dis = 0
		self.size = size
		print('Image Size', self.size)
		self.frame = 0
		self.trainingState = False
		self.X = np.empty((0,(int(self.size[1]/2))*self.size[0]))
		self.Y = np.empty((0, 4))
		self.K = np.zeros((4,4),'float')
		self.im = None
		self.Finish = False
		for i in range(4):
			self.K[i,i] = 1
	def move(self,side,vel = 40):
		vel2 = str(int(0))
		vel  = str(vel)
		
		self.act = side
		if side == 'R':
			self.toSend[1] = vel
			self.toSend[0] = vel2
		elif side == 'L':
			self.toSend[0] = vel
			self.toSend[1] = vel2
		elif side== 'F':
			self.toSend[0] = vel
			self.toSend[1] = vel
		elif side=='S':
			self.toSend[1] = '0'
			self.toSend[0] = '0'
		elif side=='B':
			self.toSend[0] = '-'+vel
			self.toSend[1] = '-'+vel
		if ardu:
			ardu.move(self.getInfo())
			

	def setTrainingState(self,value):
		self.trainingState = value
	def setLight(self,L,R):
		if L:
			self.toSend[3] = '1'
		else:
			self.toSend[3] = '0'
		if R:
			self.toSend[4] = '1'
		else:
			self.toSend[4] = '0'
		ardu.move(self.getInfo())	
	def setRadCam(self, rad):
		if ardu:
			self.toSend[2] = str(rad)
			ardu.move(self.getInfo())
	def getInfo(self):
		return self.toSend
		
	def setDis(self,dis):
		self.dis = dis
		
	def update(self,im,gray):
		cv2.imshow('im',im)
		cn,mask=cnop.getColor(im,'white')
		cv2.imshow('mask',mask)
		cv2.imshow('gary',gray)
		self.im  = gray
	def getInformationOfCapturing(self):
		return (self.frame,self.trainingState)
		
	#--------IA Section-------#
	def calculesIA(self,im):
		mov = main.predict(im)
		print(mov)
		
	#----------Carpture Image Section------#
	def SaveCaptured(self):
		print('+ Saving...')
		self.Finish = False
		self.trainingState = False
		self.finish()
			
	def getImage(self,direc):
		
			if self.trainingState:
				roi = self.im[int(self.size[1]/2):self.size[1], :]
				#-----Convertimos la fraccion de la imagen en un vector------#
				temp_array = roi.reshape(1, int(self.size[1]/2) * self.size[0]).astype(np.float32)
		
				if direc == 'F':
					self.Y = np.vstack((self.Y,self.K[0]))
					self.X = np.vstack((self.X, temp_array))
			
				elif direc == 'R':
					self.Y = np.vstack((self.Y,self.K[1]))
					self.X = np.vstack((self.X, temp_array))
				elif direc == 'L':
					self.Y = np.vstack((self.Y,self.K[2]))
					self.X = np.vstack((self.X, temp_array))
				elif direc == 'B':
					self.Y = np.vstack((self.Y,self.K[3]))
					self.X = np.vstack((self.X, temp_array))
				elif direc == 'T':
					if not self.Finish:
						SaveCaptured()
				self.frame += 1
				if not direc == 'T':
					self.Finish = False
	
	def finish (self):
		self.frame = 0
		file_name = str(int(time.time()))
		directory = "training_data"
		if not os.path.exists(directory):
			os.makedirs(directory)
		try:
			np.savez(directory + '/' + file_name + '.npz', train=self.X, train_labels=self.Y)
			#--------Reseteamos las variables de entrenamiento---------#
			self.X = np.empty((0,(int(self.size[1]/2))*self.size[0]))
			self.Y = np.empty((0, 4))
		except IOError as e:
			print(e)

		
		
		

		#if len(cn):
		#	m = cnop.getRect(im,cn) #Dibuja una linea Regresiva del contorno 
			
			
	
		
		#if coor[1] > rec[1]:
		#	self.toSend[2] = -1
		#elif coor[1] < -rec[1]:
		#	self.toSend[2] = -2
			
	
					
