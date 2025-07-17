import pandas as pd 
import illustris_python as il

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/'

# looking at redshifts between 0.5 and 3
time_ago = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
snap = [99, 96, 93, 90, 87, 84, 81, 78, 74, 71, 68] #corresponding simulation file numbers

for i in range(len(snap)):
	#load all of the galaxies at that redshift with the parameters we want
	subhalos = il.groupcat.loadSubhalos(basePath,snap[i],fields=['SubhaloSFR', 'SubhaloStarMetallicity', 'SubhaloGasMetallicity', 'SubhaloMassType'])
	print('read in subhalos')

	#limit the galaxies we look at based on stellar mass
	stellar_mass = subhalos['SubhaloMassType'].T[4] #in 1e10 Msun / h
	h = 0.704
	in_mass_range = (stellar_mass > (10**7 / 1e10) * h) & (stellar_mass < (10**10 / 1e10) * h)

	#grab the data we want for the galaxies within that range
	sfr = subhalos['SubhaloSFR'][in_mass_range]
	star_metal = subhalos['SubhaloStarMetallicity'][in_mass_range]
	gas_metal = subhalos['SubhaloGasMetallicity'][in_mass_range]

	# save to a file
	df = pd.DataFrame({'SFR [Msun / yr]':sfr, 'Stellar Metallicity [Mz/Mtot]':star_metal, 'Gas Metallicity [Mz/Mtot]':gas_metal})
	df.to_csv('data_{}.csv'.format(time_ago[i]), index=None)
