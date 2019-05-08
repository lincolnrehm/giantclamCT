import numpy as np
from PIL import Image
import sys
import timeit
import pydicom
import matplotlib.pyplot as plt

#from joblib import Parallel,delayed
binarize = False
start = timeit.default_timer()
coarse_grain = True
save_every = True

THRESHOLD = 175000

images = sys.argv[1] ###takes argument from commandline
data = np.array([])

d=5 #coarse grain size
save_imarray = []
three_d_array = []

for it,im in enumerate(open(images)): #### enumerate(open(...)) is opening the files and giving the file an index value
	im = im.split('\n')[0] #### the text file with names was opened and found /n (which is at the end of every .txt) gave it a 1 value, then we specified that we want img name
	if im.split(".")[-1]=="tif":
		im = Image.open(im) #### opened im(images in .txt file)
		imarray = np.array(im) #### created matrix of image xy
	elif im.split(".")[-1]=="dcm":
		imarray = pydicom.dcmread(im, force = True).pixel_array
		#imarray = imarray * 0.5102207 - 1000
	else: 
		print ("file type not recognized")
		exit()
	
	if coarse_grain:
		save_imarray.append(imarray)
		if len(save_imarray) == d:
			imarray = np.array(save_imarray)
			save_imarray = []
		else:
			continue
		d0,d1,d2 = imarray.shape 
		new = np.zeros((d1//d+1, d2//d+1))
		for x1 in range(d1)[::d]:
			for x2 in range(d2)[::d]:
				s = sum([sum(sum(imarray[i][x1:x1+3].T[x2:x2+3].T)) for i in range(d)])
				if s>THRESHOLD:
					new[x1//d][x2//d]=1
				else:
					new[x1//d][x2//d]=0

		ind = np.where(new==1)
		coors = list(zip([it for _ in range(len(ind[0]))],ind[0],ind[1]))
		three_d_array.append(coors)
		if save_every:
			if it == d-1:
				np.savetxt('D0013871_CG.csv',coors,delimiter=',',fmt='%i')
			else:
				np.savetxt(open('D0013871_CG.csv','a'),coors,delimiter=',',fmt='%i')
			plt.imshow(new)
			plt.savefig(im.split('.')[0]+'_CG.tif')
	if binarize:
		ind = np.where(imarray>THRESHOLD) #### searched for values greater than THRESHOLD!!!!!!!!!!!!!!
		print(ind)
		z = [it for _ in range(len(ind[0]))] #### creating a variable that is the z-coordinate, which we created in the first step of the for-loop 
		mat = np.vstack((z,ind[0],ind[1])).T #### created a matrix of our coordinates and transposed into (z,x,y) format that we are targeting but as a array
		data = np.append(data,mat) #### created a varriable and appened an array with our data

if binarize:
	n = data.shape[0] #### these two lines take a string of numbers (our data) and then creates a row of three elements (z,x,y) 
	vecs = int(n/3)

	np.savetxt('D0013871_CG.csv',data.reshape(vecs,3),delimiter = ',',fmt='%i') #### creates the final .csv file

	stop = timeit.default_timer()
	print(stop-start)



#need to rewrite some of this code to import DICOM and threshold the raw data from it, THEN we can work on averaging points so 
#we can figure out what the actual algal distribution is



"""
ds = pydicom.dcmread("D0013058_00330.dcm", force = True)
plt.imshow(ds.pixel_array)
"""
