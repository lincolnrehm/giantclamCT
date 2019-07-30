import numpy as np
import sys
import matplotlib.pyplot as plt
import os

#printdata = True

class clamname:
	def __init__(self, name, b= None, g= None, y= None):
		self.name = name
		#self.circle = circle
		self.b = b
		self.g = g
		self.y = y
	
	def lenb(self):
		self.lens= [len(self.b), len(self.g), len(self.y)]
		
def detect_data_type(name):
	try:
		return name.split('.')[0].split('CLM')[-1].split('hst')[0][-1]
	except:
		return None

#def read_y(fil):
#	y = []
#	for line in open(fil):
#		try:
#			y.append(float(line.split()[0]))
#		except:
#			continue
#	return np.array(y)

directory = ("/Users/lincolnrehm/Documents/Manuscripts/Photo_transect/transect_clam/data/histygb3/") 

clamphoto = []
bgy = {}

for f in sorted(os.listdir(directory)):#[:100]:#100samples at first
	if 'CLM' not in f: continue
	filename=directory+f
	data_type = detect_data_type(filename)
	if data_type in ['b', 'g', 'y']:
#		if data_type == 'y':
#			bgy[data_type] = read_y(filename)
#		else:
		bgy[data_type] = np.loadtxt(filename)
		try:
			len(bgy[data_type])
		except:
			bgy[data_type] = [0]
		if len(bgy[data_type]) == 0:
			 bgy[data_type] = [0]
	if len(bgy) == 3:
		obj = clamname(f,bgy['b'],bgy['g'],bgy['y'])
		clamphoto.append(obj)
		bgy = {}
#if printdata:
	#n = clamphoto.shape[0] #### these two lines take a string of numbers (our data) and then creates a row of three elements (z,x,y) 
	#vecs = int(n/4)
	#np.savetxt('transectcolor.csv',data.reshape(vecs,3),delimiter = ',',fmt='%i') #### creates the final .csv file

for c in clamphoto:
	print((c.name),(len(c.b)),(len(c.g)),(len(c.y)))

#	print(c.name)
#	print(len(c.b))
#	print(len(c.g))
#	print(len(c.y))

