import numpy as np
import scipy.interpolate as interp
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#read in algae coordintae csv file
#algaefile = "D0012997_CG.csv"
import sys
algaefile = sys.argv[1]
dl = 100
N_irid = 100000
blanket_thickness = 200
make_plot = False

def get_mesh_pnt(x,y):
	"""
	Convert coordinate to mesh point

	"""
	return (int(x//dl),int(y//dl))

def make_coor_dict(algaefile):
	"""
	Read in all algal positions and map (x,y) to a grid of width dl
	Record all z-coordinates for (x,y) keys
	

	"""
	coor_dict = dict()
	with open(algaefile,"r") as algaecoord:
		csvcoord = 3.5*np.array(list(csv.reader(algaecoord))).astype(float)
		z,x,y = csvcoord.T
		for _ in range(len(x)):
			coor = get_mesh_pnt(x[_],y[_])
			if coor in coor_dict:
				coor_dict[coor].append(z[_])
			else:
				coor_dict[coor] = [z[_]]
	return coor_dict

def z_function(z_list):
	"""	
	MODIFY

	"""
	z_height = max(z_list) # you should put in a more complex function here
	return z_height

def compress_z(coor_dict):
	"""
	Examples of how to manipulate coor_dict
	Work with if len...... line and below

	"""
	floor_map = dict()
	for coor in coor_dict:
		if len(coor_dict[coor]) < 1: # if you want to throw out grid points with few cells
			continue
		floor_map[coor] = z_function(coor_dict[coor])
	return floor_map

def convert_mesh_to_array(floor_map):
	"""
	dict object might be confusing to work with. This converts the floor_map back
	to an array

	"""
	coor_array = []
	for coor in floor_map:
		coor_array.append([coor[0],coor[1],floor_map[coor]])
	return np.array(coor_array)

def get_dimensions(coors):
	"""
	Get dimensions of system

	"""
	return dl*max(coors.T[0]), dl*max(coors.T[1])

def plot_surface(coors,irid_coors):
	"""
	make surface plot with matplotlib

	"""
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	X = irid_coors.T[0]
	Y = irid_coors.T[1]
	Z = irid_coors.T[2]
	ax.scatter(X, Y, Z, c=Z, marker='o')

	X = dl*coors.T[0]
	Y = dl*coors.T[1]
	Z = coors.T[2]
	ax.scatter(X, Y, Z, c='r', marker='o')

	plt.show()

def generate_irid(surf,xmax,ymax):
	vecs = np.random.rand(N_irid,3)
	vecs.T[0] = vecs.T[0]*xmax
	vecs.T[1] = vecs.T[1]*ymax
	vecs.T[2] = vecs.T[2]*blanket_thickness 

	bad_pnts = []

	irid_coors = []

	for pnt in vecs:
		mesh_pnt = get_mesh_pnt(pnt[0],pnt[1])
		if mesh_pnt not in surf:	
			if mesh_pnt not in bad_pnts:
				bad_pnts.append(mesh_pnt)
		else:
			# save randomly generated x and y, and save randomly generated z + height of floor mesh
			irid_coors.append([pnt[0],pnt[1],surf[mesh_pnt]+pnt[2]])

	return np.array(irid_coors)


coor_dict = make_coor_dict(algaefile)
floor_map = compress_z(coor_dict)
coors = convert_mesh_to_array(floor_map)
xmax, ymax = get_dimensions(coors)
if make_plot:
	plot_surface(coors)
irid_coors = generate_irid(floor_map,xmax,ymax)

plot_surface(coors,irid_coors)

