import urllib.request
import requests

def usr_input(text="What is the value?: "):
	return input(text)

def file_download(url_name,file_name,store_name,start_val,end_val):
	print("Begin file download...")
	array = []
	for value in range(start_val,end_val+1):
		array.append(value)
		value+=1

	for index in range(start_val,end_val+1):
		index=str(index).rjust(5,'0')
		response = requests.get('%s/%s_%s.DCM'%(url_name,file_name,index),verify=True,auth=("microCT","made1in2ch"))
		#response = requests.get('http://130.91.97.250/DISK5/MICROCT/DATA/00006028/00015512/D0013175_%s.DCM'%index,verify=True,auth=("microCT","made1in2ch"))
		with open('%s/%s_%s.dcm'%(store_name,file_name,index),'wb') as fout:
			fout.write(response.content)

	
def main():
	url = usr_input("What is the url of the folder you are downloading from?: ")
	filename = usr_input("What is the name of the file you want to download? (i.e. D00#####): ")
	storename = usr_input("Where do you want to store this file?: ") 
	startval = int(usr_input("What is the first file number?: "))
	endval = int(usr_input("What is the last file number?: "))
	
	file_download(url,filename,storename,startval,endval)
	print("Download complete...")
main()

