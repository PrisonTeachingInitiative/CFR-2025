import requests 
import numpy as np 
from astropy.io import fits
import matplotlib.pyplot as plt

#function that gives path to data
def get(path, params=None):
	# make HTTP GET request to path
	headers = {"api-key":"673159e0bdccc360baf42bfb32017ec7"}
	r = requests.get(path, params=params, headers=headers)
	
	# raise exception if response code is not HTTP SUCCESS (200)
	r.raise_for_status()
	
	if r.headers['content-type'] == 'application/json':
	    return r.json() # parse json responses automatically
	
	if 'content-disposition' in r.headers:
	    filename = r.headers['content-disposition'].split("filename=")[1]
	    with open(filename, 'wb') as f:
	        f.write(r.content)
	    return filename # return the filename string
	
	return r

ids = [402293.0,430683.0,445567.0,449267.0,449972.0,452839.0,453081.0,453134.0,453961.0,454306.0,454539.0,455198.0,456456.0,456725.0,457169.0,457604.0,458604.0,459360.0,459959.0,460823.0,461136.0,467011.0,467958.0,468064.0]


def get_image(subhalo_id):
	url = "http://www.tng-project.org/api/TNG100-1/snapshots/99/subhalos/{}/skirt/broadband_sdss.fits".format(str(int(subhalo_id)))
	get(url)

	h = fits.open('broadband_{}.fits'.format(str(int(subhalo_id))))
	data = h[0].data

	plt.imshow(data[0], cmap='gray', vmin=0, vmax=5)
	plt.colorbar()
	plt.ylim(0, 360)
	plt.xlim(0, 360)
	plt.axis('off')
	plt.savefig('mock_image_{}.png'.format(str(int(subhalo_id))))
	plt.close()	

# for subhalo in ids:
# 	get_image(subhalo)


def make_png(subhalo_id):
	h = fits.open('../fits/broadband_{}.fits'.format(str(int(subhalo_id))))
	data = h[0].data

	plt.imshow(data[0], cmap='gray', vmin=0, vmax=5)
	plt.colorbar()
	plt.ylim(0, 360)
	plt.xlim(0, 360)
	plt.axis('off')
	plt.savefig('mock_image_{}.png'.format(str(int(subhalo_id))))
	plt.close()	

for subhalo in ids:
	make_png(subhalo)