import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os 


from math import floor as fl
from math import ceil as cl
from mpl_toolkits.mplot3d import Axes3D
from time import sleep
#from matplotlib import cm

# Fixing random state for reproducibility
#np.random.seed(19680801)


#Create a donut

def donut(r1, r2, Theta):
	#Ndots = 10
	#Theta = np.linspace(0, 2*np.pi,Ndots)
	x = r1*np.cos(Theta) + r2*np.ones(len(Theta))
	y = r1*np.sin(Theta) + r2*np.ones(len(Theta))
	z = np.zeros(len(x))
	xd = []
	yd = []
	zd = []
	for ang in Theta:

		xr, yr, zr = Rotate_3D_Sphere(x, y, z, 'x', ang)
		#Adding coordinates of the rotated circles together
		xd = np.append(xd, xr)
		yd = np.append(yd, yr)
		zd = np.append(zd, zr)
	return xd,yd,zd
	
	
#Rotation function

def Rotate_3D_Sphere(x1, y1, z1, axis, angle):
 	
	n = len(x1)
	if axis == 'x':
		xr = x1
		yr = np.array([y1[i]*np.cos(angle) - z1[i]*np.sin(angle) for i in range(n)])
		zr = np.array([y1[i]*np.sin(angle) + z1[i]*np.cos(angle) for i in range(n)])

	elif axis == 'y':

		xr = np.array([x1[i]*np.cos(angle) - z1[i]*np.sin(angle) for i in range(n)])
		yr = y1
		zr = np.array([x1[i]*np.sin(angle) + z1[i]*np.cos(angle) for i in range(n)])

	else :

		xr = np.array([x1[i]*np.cos(angle) - y1[i]*np.sin(angle) for i in range(n)])
		yr = np.array([x1[i]*np.sin(angle) + y1[i]*np.cos(angle) for i in range(n)])
		zr = z1

	return xr , yr, zr

def porj2D(x,y,z,normvect,l,L,d,D):

	#l and L are the width and length of the projection window
	#The projection window will be on the y,z plan
	#d is the distance of the eye from the window (it's a kind of scaling factor)
	#D is the distance from ref center according to x>

	yp = []
	zp = []
	i = 0
	j = 0
	vlight  = [-1,0,0]
	marker = ['#','&','%','?','"',';',':','.',' ']
	marker_list = []
	indmark = 8
	donutmat = np.empty([42,42], dtype = str )

	#creating an empty canvas
	
	for p in range(42):

		for m in range(42):
			donutmat[p,m] = ' '
        #Calculating Projected coordinates :
	for xi,yi,zi in zip(x,y,z):
		#if xi > 0:

		y0 = yi*(d/(D-xi))
		z0 = zi*np.sqrt((y0**2 + d**2)/(yi**2 + (d + D - xi)**2))
		
		if y0 > l/2 :
			y0 = l/2
		elif y0 < -l/2:
			y0 = -l/2
		if z0 > L/2 :
			z0 = L/2
		elif z0 < -L/2:
			z0 = -L/2
		
		
		#Calculating the marker (Lit areas, for each set of 4 coordinates applied one marker) :

		if i%2 != 0:
			if j%2 != 0 :
				cos = vlight[0]*normvect[i-1,j-1][0] + vlight[1]*normvect[i-1,j-1][1] + vlight[2]*normvect[i-1,j-1][2]
			else:
				cos = vlight[0]*normvect[i-1,j][0] + vlight[1]*normvect[i-1,j][1] + vlight[2]*normvect[i-1,j][2]
			
		else:
			if j%2 != 0 :			
				cos = vlight[0]*normvect[i,j-1][0] + vlight[1]*normvect[i,j-1][1] + vlight[2]*normvect[i,j-1][2]
			else:			
				cos = vlight[0]*normvect[i,j][0] + vlight[1]*normvect[i,j][1] + vlight[2]*normvect[i,j][2]
			
		if cos > 0:
			indmark = 8
		elif -0.125 <= cos <= 0:
			indmark = 7
		elif -0.25 <= cos < -0.125:
			indmark = 6
		elif -0.375 <= cos < -0.25:
			indmark = 5
		elif -0.5 <= cos < -0.375:
			indmark = 4
		elif -0.625 <= cos < -0.5:
			indmark = 3
		elif -0.75 <= cos < -0.625:
			indmark = 2
		elif -0.875 <= cos < -0.75:
			indmark = 1
		elif -1 <= cos < -0.875:
			indmark = 0
		
		if indmark == 8:
			pass  #to ignore ploting non visible areas
		else:
			yp.append(y0)
			zp.append(z0)
			marker_list.append(marker[indmark])

		        # Scale adjustment + some offset for better ploting.
			indy = cl(y0*10) + 20 
			indz = cl(z0*10) + 20
			donutmat[indz,indy] = marker[indmark]

		i+=1
		if i== Ndots:
			i = 0
			j+= 1
		
		
	return [yp, zp, marker_list], donutmat

def norm_surf(x, y, z, Ndots, Theta):
	a = len(Theta)
	#print(a)
	d = 1
	#print('am here')
	normVect = np.zeros([Ndots - d, a - 1], dtype = object)
	#print('am here')
	for j in range(Ndots-1):
		#print('am here', j)
		for i in range(Ndots - d ):
			#print(i)
			v1 = [x[i+j*Ndots] - x[i+Ndots+j*Ndots], y[i+j*Ndots] - y[i + Ndots + j*Ndots], z[i+j*Ndots] - z[i + Ndots+j*Ndots] ]
			v2 = [x[i + d + Ndots + j*Ndots] - x[i+Ndots + j*Ndots], y[i+d+ Ndots + j*Ndots] - y[i + Ndots + j*Ndots], z[i+d+ Ndots+ j*Ndots] - z[i + Ndots + j*Ndots] ]
			a = v1[1]*v2[2] - v1[2]*v2[1]
			b = v1[2]*v2[0] - v1[0]*v2[2]
			c = v1[0]*v2[1] - v1[1]*v2[0]
			module = np.sqrt(a**2 + b**2 + c**2)
			#if module == 0: print('Null module')
			normVect[i,j] = [a/module,b/module,c/module]
			#print(normVect)
	return normVect

def termprint(donutmat):
	strn = ''
	for line in donutmat:
		#print(line,' ')
		for char in line:
			strn+= str(char)
		print(strn,"\n")

		#indy = cl(y*10) + 20
		#indz = cl(z*10) + 20


def update(i, line, x,y,z, Theta):
	#i is a dependancy so, the plot moves
	
	Rotation_axe = 'z'
	
	#Rotating coordinates
	x2, y2, z2 = Rotate_3D_Sphere(x,y,z,Rotation_axe,Theta[i])
	
	#Updating 3D data
	line.set_data(x2, y2)
	line.set_3d_properties(z2)

def update2D(i,line2, x,y,z, Theta):
	#i is a dependancy so, the plot moves
	
	Rotation_axe = 'z'
	
	#Rotating coordinates
	x2, y2, z2 = Rotate_3D_Sphere(x,y,z,Rotation_axe,Theta[i])
	
	normVect = norm_surf(x2, y2, z2, 50,Theta)
	#print(normVect)
	
	#Calculatin projection data

	#yp , zp = porj2D(x2,y2,z2,4,4,2,10)
	data, donutmat = porj2D(x2,y2,z2,normVect,4,4,2,10)
	#print(data[2])
	#print(donutmat)
	termprint(donutmat)
	#Updating projection data
	sleep(0.08)
	os.system('clear')
	line2.set_data(data[0],data[1])

#Creating subplot
fig = plt.figure()

axe = Axes3D(fig)

fig2 = plt.figure()
axe2 = fig2.add_subplot(1,1,1)
l, = axe.plot3D([],[],[],'xk')
l2, = axe2.plot([],[],'xk')


#Setting limits

axe.set_xlim3d([0.0, 10])
axe.set_xlabel('X')
axe.set_ylim3d([0.0, 10])
axe.set_ylabel('Y')
axe.set_zlim3d([0.0, 10])
axe.set_zlabel('Z')
axe.set_title('3D Rotation')

axe2.set_xlim([-2, 2])
axe2.set_xlabel('Y')
axe2.set_ylim([-2, 2])
axe2.set_ylabel('Z')
axe2.set_title('2D Proj of a 3D Donut')

#Creating An initial shape ; 

Ndots = 50
Theta = np.linspace(0, 2*np.pi,Ndots)
#radius = 0.9

#Creating a 3D donut

x, y, z = donut(2, 4, Theta)

#Creating animation object :
line_ani = animation.FuncAnimation(fig, update,fargs=(l,x, y, z, Theta), frames = len(Theta), interval = 1)

line_an = animation.FuncAnimation(fig2, update2D,fargs=(l2,x, y, z, Theta), frames = len(Theta), interval = 1)

plt.show()

