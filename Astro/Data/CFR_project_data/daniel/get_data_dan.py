import pandas as pd 
import illustris_python as il

# read in the data from my external hard drive
basePath = '/Volumes/Titan/TNG_all/'

# # looking at redshifts between 0.5 and 3
# z = [0.5, 1, 1.5, 2, 2.4, 3]
# snap = [67, 50, 40, 33, 29, 25] #corresponding simulation file numbers

# for i in range(len(snap)):
# 	#load all of the galaxies at that redshift with the parameters we want
# 	subhalos = il.groupcat.loadSubhalos(basePath,snap[i],fields=['SubhaloSFR', 'SubhaloStarMetallicity', 'SubhaloMassType'])
# 	print('read in subhalos')

# 	#limit the galaxies we look at based on stellar mass
# 	stellar_mass = subhalos['SubhaloMassType'].T[4] #in 1e10 Msun / h
# 	h = 0.704
# 	in_mass_range = (stellar_mass > (10**8.57 / 1e10) * h) & (stellar_mass < (10**8.66 / 1e10) * h)

# 	#grab the data we want for the galaxies within that range
# 	sfr = subhalos['SubhaloSFR'][in_mass_range]
# 	metal = subhalos['SubhaloStarMetallicity'][in_mass_range]

# 	# save to a file
# 	df = pd.DataFrame({'SFR [Msun / yr]':sfr, 'Stellar Metallicity [Mz/Mtot]':metal})
# 	df.to_csv('data_{}.csv'.format(z[i]), index=None)


# looking at redshifts between 0.5 and 3
z = 8.45
snap = 7

#load all of the galaxies at that redshift with the parameters we want
subhalos = il.groupcat.loadSubhalos(basePath,snap,fields=['SubhaloGasMetalFractions', 'SubhaloStarMetalFractions', 'SubhaloMassType'])
print('read in subhalos')

#limit the galaxies we look at based on stellar mass
stellar_mass = subhalos['SubhaloMassType'].T[4] #in 1e10 Msun / h
h = 0.704
in_mass_range = (stellar_mass > (10**8.57 / 1e10) * h) & (stellar_mass < (10**8.66 / 1e10) * h)

#grab the data we want for the galaxies within that range
o_gas = subhalos['SubhaloGasMetalFractions'].T[4][in_mass_range]
n_gas = subhalos['SubhaloGasMetalFractions'].T[3][in_mass_range]
fe_gas = subhalos['SubhaloGasMetalFractions'].T[5][in_mass_range]
c_gas = subhalos['SubhaloGasMetalFractions'].T[2][in_mass_range]
h_gas = subhalos['SubhaloGasMetalFractions'].T[0][in_mass_range]

o_star = subhalos['SubhaloStarMetalFractions'].T[4][in_mass_range]
n_star = subhalos['SubhaloStarMetalFractions'].T[3][in_mass_range]
fe_star = subhalos['SubhaloStarMetalFractions'].T[5][in_mass_range]
c_star = subhalos['SubhaloStarMetalFractions'].T[2][in_mass_range]
h_star = subhalos['SubhaloStarMetalFractions'].T[0][in_mass_range]

# save to a file
df = pd.DataFrame({'OHmass for gas':h_gas,'O mass for gas':o_gas, 'N mass for gas':n_gas, 'Fe mass for gas':fe_gas, 'C mass for gas':c_gas,'O mass for stars':o_star, 'N mass for stars':n_star, 'Fe mass for star':fe_star, 'C mass for stars':c_star, 'h mass for stars':h_star})
df.to_csv('metals_z.csv', index=None)