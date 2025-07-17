import pandas as pd 
import illustris_python as il
import numpy as np

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/'

# first sets of data
# looking at redshifts between 0 and 2.96
z = [0, 0.5, 1, 1.5, 2, 2.4, 2.9]
snap = [99, 67, 50, 40, 33, 29, 26] #corresponding simulation file numbers

for i in range(len(snap)):
	#load all of the galaxies at that redshift with the parameters we want
	subhalos = il.groupcat.loadSubhalos(basePath,snap[i],fields=['SubhaloMass', 'SubhaloStarMetalFractions'])
	print('read in subhalos')

	#limit the galaxies we look at based on the oxygen abundance
	hydrogen = subhalos['SubhaloStarMetalFractions'].T[1] 
	oxygen = subhalos['SubhaloStarMetalFractions'].T[4] 

	#calculating abundance 
	mass_ratio = oxygen / hydrogen
	number_ratio = mass_ratio * (1.008 / 15.999)
	abundance = 12 + np.log10(number_ratio)

	#limiting the galaxies based on oxgen abundance
	in_oxygen_range = (abundance < 8.07) & (abundance > 8.03)

	#grab the data we want for the galaxies within that range
	h = 0.704 # used to convert the mass to Msun
	mass = subhalos['SubhaloMass'][in_oxygen_range] * 1e10 / h 

	# save to a file
	df = pd.DataFrame({'Mass Oxygen / Star mass':oxygen[in_oxygen_range], 'Mass Hydrogen / Star mass':hydrogen[in_oxygen_range], 'Mass of Galaxy [Msun]':mass})
	df.to_csv('data_{}.csv'.format(z[i]), index=None)

# second set of data
subhalos = il.groupcat.loadSubhalos(basePath,26,fields=['SubhaloStarMetalFractions'])

# grab the columns needed to calucate oxygen abundances
hydrogen = subhalos.T[1] 
oxygen = subhalos.T[4] 

#save the data
df = pd.DataFrame({'Mass Oxygen / Star mass':oxygen, 'Mass Hydrogen / Star mass':hydrogen})
df.to_csv('oxygen_hydrogen_2.9.csv', index=None)



