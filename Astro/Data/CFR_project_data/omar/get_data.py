import pandas as pd 
import illustris_python as il

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/'

# looking at redshifts between 0.5 and 3
z = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11.98]
snap = [99, 50, 33, 25, 20, 17, 12, 11, 8, 9, 4, 3, 2] #corresponding simulation file numbers

for i in range(len(snap))[6:]:
	#load all of the galaxies at that redshift with the parameters we want
	subhalos = il.groupcat.loadSubhalos(basePath,snap[i],fields=['SubhaloStellarPhotometrics'])
	print('read in subhalos')

	#get the UV brightness
	u = subhalos[:,1]

	# save to a file
	df = pd.DataFrame({'u band':u})
	df.to_csv('data_{}.csv'.format(z[i]), index=None)
