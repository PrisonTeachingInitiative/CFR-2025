import h5py
import pandas as pd 

# load the data file from my external hard drive
morph = h5py.File('/Volumes/Titan/TNG_all/TNG50/morphologies_deeplearn.hdf5', 'r')

# snapshots that corredspond to the redshifts we are interested in (z=0.5, 1, 1.5, 2, 2.5, 3)
snaps = [67, 50, 40, 33, 29, 25]
z = [0.5, 1, 1.5, 2, 2.5, 3]

# loop through the snapshots and pull out the spiral probabilities and save to an individiual file
for i in range(len(snaps)):
	p_spiral = morph['Snapshot_{}/P_Disk'.format(snaps[i])][()] # grabbing the right column

	# saving the data to a file using pandas
	df = pd.DataFrame({'Probability is spiral (decimal)': p_spiral})
	df.to_csv('p_spiral_{}.csv'.format(z[i]), index=None)


