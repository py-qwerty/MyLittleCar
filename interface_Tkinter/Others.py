def goToTheShape(self,im):
		#------Lista de Contornos------#
		cn = cnop.getColor(im,'black')
		ce = cl.getMidel(im,self.size,True,False)
		#-----Lista de Coordenadas de Objetos------#
		if len(cn):
			obList = cnop.getObOfCn(im,cn)
			#-------Calculamos el objeto mas cercano al centro de la camara------#
			ob = cl.lookForShor(im,obList,ce)
			c = cn[obList.index(ob)]
			(x,y,w,h)=cv2.boundingRect(c)
			#-----Calculamos el area psreal del objeto obtenido------#
			if cnop.detectShape(im,c) == 'Square':
				self.calculeAndMove(im,ob,ce,(20,20),True)
		
	def follow_ball(self,im):
		#------Lista de Contornos------#
		cn = cnop.getColor(im,'blue')
		ce = cl.getMidel(im,self.size,True,False)
		#-----Lista de Coordenadas de Objetos------#
		if len(cn):
			obList = cnop.getObOfCn(im,cn)
			#-------Calculamos el objeto mas cercano al centro de la camara------#
			ob = cl.lookForShor(im,obList,ce)
			c = cn[obList.index(ob)]
			(x,y,w,h)=cv2.boundingRect(c)
			#-----Calculamos el area psreal del objeto obtenido------#
			if cnop.detectShape(im,c) == 'Circle':
				self.calculeAndMove(im,ob,ce,(20,20),True)
		
                        
	def calculeAndMove(self,im, ob, ce,rec =(3,3), draw = False):
		coor = [ob[0]-ce[0],ob[1]-ce[1]]
		dis = math.hypot(coor[0],coor[1])
		rec = rec
		if draw:
			cl.getMidel(im,self.size,False,True,rec,(0,0,255))
			
		#-------Left--------#
		if self.dis >= 20:
			if not self.act == 'S':
				self.move('S')
		elif coor[0] > rec[0]:
			if not self.act == 'L':
				self.move('L')
		elif coor[0] < -rec[0]:
			if not self.act == 'R':
				self.move('R')
		else:
			if not self.act == 'F':
				self.move('F')
		
