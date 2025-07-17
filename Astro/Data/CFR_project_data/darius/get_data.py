import requests 
import numpy as np 
import h5py 
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u 
import pandas as pd 
import illustris_python as il


# read in a file I had with info on MW-like galaxies
IDs, merger_times, num_major, num_minor = np.loadtxt('/Volumes/Titan/Research/analogs/IllustrisAD/TNG_v2/M31analogs_merger_props_TNG100_revised.txt', usecols=(0,2,3,4,), unpack=True) 

# loop through all of the galaxies and get the average age of all the stars
IDs = [int(a) for a in IDs]

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
	url = "https://www.tng-project.org/api/TNG100-1/snapshots/99/subhalos/" + str(int(subhalo_id))
	saved_filename = get(url + "/cutout.hdf5",params) #hdf5 file with all the data
	f = h5py.File(saved_filename, 'r') #read the file in order to save the data
	star_factor = f['PartType4']['GFM_StellarFormationTime']
	avg_star_factor = np.median(star_factor)

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
for subhalo in IDs: #362 is no good
	print(subhalo)
	age.append(save_particle_data(subhalo))

# save file
df = pd.DataFrame({'Time Since Last Major Merger [Gyr]':merger_times, 'Number of Major Mergers':num_major, 'Number of Minor Mergers':num_minor, 'average stellar age [Gyr]':age})
df.to_csv('merger_info.csv', index=None)