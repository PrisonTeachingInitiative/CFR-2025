import numpy as np
from scipy.integrate import simps
import h5py
import pandas as pd 

# looking at our redshift range of 0-1
z = [0, 0.26, 0.44, 0.68, 0.82, 1]
snaps = [99, 80, 70, 60, 55, 50] #corresponding simulation timestamps


#convert snapshot to time
def snapnum2z(snap):
    zs = [20.05, 14.99, 11.98, 10.98, 10, 9.39, 9., 8.45, 8.01, 7.6, 7.24, 7.01, 6.49, 6.01, 5.85, 5.53, 5.23, 5., 4.66, 4.43, 4.18, 4.01, 3.71, 3.49, 3.28, 3.01, 2.9, 2.73, 2.58, 2.44 ,2.32, 2.21, 2.1, 2., 1.9, 1.82, 1.74, 1.67, 1.6, 1.53, 1.5, 1.41, 1.36, 1.3, 1.25, 1.21, 1.15, 1.11, 1.07, 1.04, 1., 0.95, 0.92, 0.89, 0.85, 0.82, 0.79, 0.76, 0.73, 0.7, 0.68, 0.64, 0.62, 0.6, 0.58, 0.55, 0.52, 0.5, 0.48, 0.46, 0.44, 0.42, 0.4, 0.38, 0.36, 0.35, 0.33, 0.31, 0.3, 0.27, 0.26, 0.24, 0.23, 0.21, 0.2, 0.18, 0.17, 0.15, 0.14, 0.13, 0.11, 0.1, 0.08, 0.07, 0.06, 0.05, 0.03, 0.02, 0.01, 0.]

    snaps = np.arange(0,100, 1)

    if snap == -1:
        z = 1000.
    else:
        z = zs[np.where(snaps == snap)[0][0]]
    return z

def time(z):
    '''
    Calculate lookback time for a flat cosmology
    '''
    t = 0.
    if z == 0.:
        t = 0.001

    if z == 1000.:
        t = 13.8

    if 0. < z < 1000.:
        #print z
        h = 0.704
        H0 = h*100
        OM = 0.2726
        OL = 0.7274
        H0 = (H0 * 3.241e-20)/ 3.171e-17 # final units of[Gyr ^-1]

        def f(z):
            return 1/((H0*(1+z)*np.sqrt(OM*(1+z)**3 + OL)))

        zs = np.arange(0., z, 1e-5)
        y = f(zs)
        t = simps(y,zs)
    return t #in Gyrs


#for each redshit, get data
for i in range(len(snaps)):
	#get the merger data file
	merger_data = h5py.File('/Volumes/Titan/TNG_all/merger/MergerHistory_0{}.hdf5'.format(snaps[i]), 'r')

	#pull out the params we want: time of last major merger, number of major mergers, and number of minor mergers and match the data to our analogs
	last_major_snap = merger_data['SnapNumLastMajorMerger']
	num_major = merger_data['NumMajorMergersTotal']

	#randomly select 5000 galaxies so the amount of data is manageable
	inds = np.random.choice(range(0, len(last_major_snap)), size=10000, replace=False)
	last_major_snap = last_major_snap[sorted(inds)]
	num_major = num_major[sorted(inds)]

	#use functions about to calculate time since last major meger
	print('starting time calculation')
	last_major_time = [time(snapnum2z(snap)) for snap in last_major_snap]

	#save data
	df = pd.DataFrame({'Time Since Last Major Merger [Gyr]':last_major_time, 'Number of Major Mergers':num_major})
	df.to_csv('mergers_{}.csv'.format(z[i]), index=None)






