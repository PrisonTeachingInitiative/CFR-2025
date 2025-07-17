import pandas as pd 
import illustris_python as il

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/'

# looking at redshifts between 0.5 and 3
z = [0.5, 1, 1.5, 2, 2.4, 3]
snap = [67, 50, 40, 33, 29, 25] #corresponding simulation file numbers

for i in range(len(snap)):
	#load all of the galaxies at that redshift with the parameters we want
	subhalos = il.groupcat.loadSubhalos(basePath,snap[i],fields=['SubhaloSFR', 'SubhaloStarMetallicity', 'SubhaloMassType'])
	print('read in subhalos')

	#limit the galaxies we look at based on stellar mass
	stellar_mass = subhalos['SubhaloMassType'].T[4] #in 1e10 Msun / h
	h = 0.704
	in_mass_range = (stellar_mass > (10**8.57 / 1e10) * h) & (stellar_mass < (10**8.66 / 1e10) * h)

	#grab the data we want for the galaxies within that range
	sfr = subhalos['SubhaloSFR'][in_mass_range]
	metal = subhalos['SubhaloStarMetallicity'][in_mass_range]

	# save to a file
	df = pd.DataFrame({'SFR [Msun / yr]':sfr, 'Stellar Metallicity [Mz/Mtot]':metal})
	df.to_csv('data_{}.csv'.format(z[i]), index=None)
