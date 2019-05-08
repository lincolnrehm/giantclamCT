import numpy as np
import scipy.interpolate as interp
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#read in algae coordintae csv file
algaefile = "D0012997_CG.csv"
with open(algaefile,"r") as algaecoord:
	csvcoord = 3.5*np.array(list(csv.reader(algaecoord))).astype(float)
	z,x,y = csvcoord.T
	print(x,y)



#TURN IN GRID IN SMART WAY
	#fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')
	#ax.scatter(x,y,z,c='r',marker='o',s=5)
	#ax.scatter(X,Y,Z,c='k',marker='o',s=10)
	#plt.show()
