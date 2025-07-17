import requests 
import numpy as np 
import h5py 
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u 
import pandas as pd 
import illustris_python as il

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/TNG50'

# get the galaxies
subhalos = il.groupcat.loadSubhalos(basePath,29,fields=['SubhaloStellarPhotometrics']) #mass in code units, vmax in km/s
print('Read in the subhalos')

# pull out the magnitudes
g = subhalos[:,4]
r = subhalos[:,5]

# read in the file with the spiral probabilities
morph = h5py.File('/Volumes/Titan/TNG_all/TNG50/morphologies_deeplearn.hdf5', 'r')
SubfindID = morph['Snapshot_29/SubhaloID'][()] #IDs of galaxies
p_spiral = morph['Snapshot_29/P_Disk'][()] 

# not all of the galaxies have a p_spiral, so we are going to grab only those that do
g = g[SubfindID]
r = r[SubfindID]

# pull the star ages for each of the galaxies
# function that gives path to data
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

# grab the star information
def save_particle_data(subhalo_id):
	params = {'stars':'GFM_StellarFormationTime'} 
	url = "https://www.tng-project.org/api/TNG50-1/snapshots/29/subhalos/" + str(int(subhalo_id))
	saved_filename = get(url + "/cutout.hdf5",params) #hdf5 file with all the data
	f = h5py.File(saved_filename, 'r') #read the file in order to save the data
	star_factor = f['PartType4']['GFM_StellarFormationTime']
	#print('loaded star factors')
	avg_star_factor = np.median(star_factor)
	#print('calculated median')

	# convert from scale factor to age
	def star_age(scale_factor):
		zform = (1./scale_factor) -1.
		cosmo = FlatLambdaCDM(H0=70.4, Om0=0.2726, Ob0=0.0456)
		tform = float(cosmo.age(zform)/u.Gyr)  #time the stars formed in lookback time, not age
		tage = 13.8-tform 
		return tage #Gyr

	return star_age(avg_star_factor)

# apply our function to get all of the average ages
age = []
for subhalo in SubfindID: #362 is no good
	print(subhalo)
	age.append(save_particle_data(subhalo))

# save file
df = pd.DataFrame({'g band':g, 'r band':r, 'average stellar age [Gyr]':age})
df.to_csv('galaxy_info_2.44.csv', index=None)
