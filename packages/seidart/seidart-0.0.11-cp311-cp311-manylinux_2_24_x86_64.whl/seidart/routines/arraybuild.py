#!/usr/bin/env python3

# Create a receiver array and plot the timeseries

import numpy as np
import pandas as pd
from glob2 import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from seidart.routines.definitions import *

# from obspy import Trace, Stream, UTCDateTime

# =============================================================================
class Array:
    def __init__(
        self, 
        channel: str,
        prjfile: str, 
        receiver_file: str,
        receiver_indices: bool = False, 
        single_precision: bool = True,
        is_complex: bool = False
    ):
        """
        :param dt: Time step between measurements.
        :param receivers_xyz: Coordinates of the receivers in a numpy array of shape (n, 3).
        :param source_xyz: Location of the source as a tuple or list (x, y, z).
        """
        self.prjfile = prjfile 
        self.channel = channel
        self.receiver_file = receiver_file
        self.receiver_indices = receiver_indices
        self.single_precision = single_precision
        self.is_complex = is_complex
        self.stream = None
        self.build()
    
    # -------------------------------------------------------------------------
    def build(self):
        self.domain, self.material, self.seismic, self.electromag = loadproject(
            self.prjfile,
            Domain(), 
            Material(),
            Model(),
            Model()
        )
        if self.channel in ['Vx','Vy','Vz']:
            self.is_seismic = True
            self.dt = self.seismic.dt 
        else:
            self.is_seismic = False
            self.dt = self.electromag.dt
        
         
        # __, self.receivers_xyz = self.loadxyz()
        self.loadxyz()
        if self.channel == 'Vx' or self.channel == 'Vy' or self.channel == 'Vz':
            if self.domain.dim == '2.0':
                self.source = np.array(
                    [int(self.seismic.x), int(self.seismic.z)]
                )
            else:
                self.source = np.array(
                    [
                        int(self.seismic.x), 
                        int(self.seismic.y), 
                        int(self.seismic.z)
                    ]
                )
        else:
            if self.domain.dim == '2.0':
                self.source = np.array(
                    [int(self.electromag.x), int(self.electromag.z)]
                )
            else:
                self.source = np.array(
                    [
                        int(self.electromag.x), 
                        int(self.electromag.y), 
                        int(self.electromag.z)
                    ]
                )
        
        # Load the time series for all receivers
        self.getrcx()
        # self.streams = self._create_streams()
        
    # -------------------------------------------------------------------------
    # def _create_streams(self):
    #     streams = {}
    #     start_time = UTCDateTime()  # Using current time as a reference, adjust as necessary

    #     m, n = self.timeseries.shape 
    #     stream = Stream()
        
    #     for ind in range(n):
    #         dat = self.timeseries[:,ind]
    #         datc = self.timeseries_complex[:,ind]
    #         for loc in np.array(['00', '10']):
    #             header = {
    #                 'station': f"R{ind}", 'location': loc, 'network': 'SDRT',
    #                 'channel': self.channel,
    #                 'starttime': start_time,
    #                 'delta': self.dt,
    #                 'npts': m,
    #                 'coordinates': {
    #                     'latitude': self.receiver_xyz[ind][1],
    #                     'longitude': self.receiver_xyz[ind][0],
    #                     'elevation': self.receiver_xyz[ind][2],
    #                 },
    #             }
    #             if loc == '00':
    #                 trace = Trace(data=dat, header=header)
    #             if loc == '10' and 'E' in self.channel:
    #                 trace = Trace(data=datc, header=header)
                
    #             stream.append(trace)
        
    #     self.stream = stream
        # return stream

    # -------------------------------------------------------------------------
    def loadxyz(self):
        '''Load and sort the receiver locations'''
        xyz = pd.read_csv(self.receiver_file)

        # We need to make sure the recievers are ordered correctly and the 
        # absorbing boundary is corrected for
        # First check to see if the inputs are indices or
        cpml = int(self.domain.cpml)
        # Adjust the object fields relative to the cpml. The y-direction will be
        # adjusted when we are 2.5/3D modeling
        self.domain.nx = self.domain.nx + 2*cpml
        self.domain.nz = self.domain.nz + 2*cpml
        if self.domain.dim == 2.5:
            self.domain.ny = self.domain.ny + 2*cpml

        self.receiver_xyz = xyz.to_numpy() 
        
        if self.receiver_xyz.shape[1] == 1:
            self.receiver_xyz = self.receiver_xyz.T

        # We want to make sure the shape of the self.receiver_xyz array is in 
        # the correct shape. We won't be able to differentiate if the array is 
        # in correct shape if it is 3x3
        if self.receiver_xyz.shape[0] == 3 and np.prod(self.receiver_xyz.shape) > 9:
            self.receiver_xyz = self.receiver_xyz.T
        if self.receiver_xyz.shape[0] == 3 and np.prod(self.receiver_xyz.shape) == 6:
            self.receiver_xyz = self.receiver_xyz.T
        
        # If the receiver file contains values that are relative to the 
        # cartesian space of the domain, we want to change them to the indices
        # of the 
        if not self.receiver_indices:
            self.receiver_xyz = self.receiver_xyz / \
                np.array(
                    [
                        float(self.domain.dx), 
                        float(self.domain.dy), 
                        float(self.domain.dz) 
                    ]
                )
            self.receiver_xyz.astype(int)

        self.receiver_xyz = self.receiver_xyz + cpml
        # return(self.domain, self.receiver_xyz)
    
    # -------------------------------------------------------------------------
    def getrcx(self):
        # input rcx as an n-by-2 array integer values for their indices.
        src_ind = (
            self.source / \
            np.array([self.domain.dx, self.domain.dy, self.domain.dz])
        ).astype(int)
        if self.domain.dim == 2.5:
            all_files = glob(
                self.channel + '*.' + '.'.join(src_ind.astype(str)) + '.dat'
            )
        else: 
            all_files = glob(
                self.channel + '*.' + '.'.join(src_ind[np.array([0,2])].astype(str)) + '..dat'
            )
        
        all_files.sort()
        m = len(all_files)
        if len(self.receiver_xyz.shape) == 1:
            n = 1
            timeseries = np.zeros([m]) 
        else:
            n = len(self.receiver_xyz[:,0])
            timeseries = np.zeros([m,n])   
            
        timeseries_complex = timeseries.copy()
        
        if self.domain.dim == 2.0:
            self.domain.ny = None

        if self.domain.dim == 2.5:
            for i in range(m):
                npdat = read_dat(
                    all_files[i], 
                    self.channel, 
                    self.domain, 
                    self.is_complex, 
                    single = self.single_precision
                )
                if n == 1:
                    timeseries[:,i] = npdat.real[
                        int(self.receiver_xyz[2]), 
                        int(self.receiver_xyz[1]), 
                        int(self.receiver_xyz[0])
                    ]
                    timeseries_complex[:,i] = npdat.imag[
                        int(self.receiver_xyz[2]), 
                        int(self.receiver_xyz[1]), 
                        int(self.receiver_xyz[0])
                    ]
                else:
                    for j in range(0, n):
                        # Don't forget x is columns and z is rows
                        timeseries[i,j] = npdat.real[
                            int(self.receiver_xyz[j,2]),
                            int(self.receiver_xyz[j,1]),
                            int(self.receiver_xyz[j,0])
                        ]
                        timeseries_complex[i,j] = npdat.imag[
                            int(self.receiver_xyz[j,2]),
                            int(self.receiver_xyz[j,1]),
                            int(self.receiver_xyz[j,0])
                        ]
        else:
            for i in range(m):
                npdat = read_dat(
                    all_files[i], 
                    self.channel, 
                    self.domain, 
                    self.is_complex,
                    single = self.single_precision
                )
                if n == 1:
                    timeseries[:,i] = npdat.real[
                        int(self.receiver_xyz[2]), int(self.receiver_xyz[0])
                    ]
                    timeseries_complex[:,i] = npdat.imag[
                        int(self.receiver_xyz[2]), 
                        int(self.receiver_xyz[0])
                    ]
                else:
                    for j in range(n):
                        # Don't forget x is columns and z is rows
                        timeseries[i,j] = npdat.real[
                            int(self.receiver_xyz[j,2]),
                            int(self.receiver_xyz[j,0])
                        ]
                        timeseries_complex[i,j] = npdat.imag[
                            int(self.receiver_xyz[j,2]),
                            int(self.receiver_xyz[j,0])
                        ]
        
        # Store both of the time series in the array object
        self.timeseries_complex = timeseries_complex
        self.timeseries = timeseries
    
    # -------------------------------------------------------------------------
    def sectionplot(
            self, 
            gain: int = 100, 
            exaggeration: float = 0.5, 
            plot_complex: bool = False
        ):
        '''
        Create a gray scale section plot
        '''
        if plot_complex:
            # Use complex values 
            dat = self.timeseries_complex 
        else:
            dat = self.timeseries
        
        m,n = dat.shape
        
        if self.is_seismic:
            mult = 1e2
        else:
            mult = 1e6

        timelocs = np.arange(0, m, int(m/10) ) # 10 tick marks along y-axis
        rcxlocs = np.arange(0, np.max([n, 5]), int(np.max([n, 5])/5) ) # 5 tick marks along x-axis

        if self.is_seismic:
            timevals = np.round(timelocs*float(self.dt) * mult, 2)
        else:
            timevals = np.round(timelocs*float(self.dt) * mult, 2)

        if gain == 0:
            gain = 1
            
        if gain < m:
            for j in range(0, n):
                # Subtract the mean value
                # dat[:,j] = dat[:,j] - np.mean(dat[:,j])
                dat[:,j] = agc(dat[:,j], gain, "mean")


        self.fig = plt.figure()#figsize =(n/2,m/2) )
        self.ax = plt.gca()

        self.ax.imshow(dat, cmap = 'Greys', aspect = 'auto')
        self.ax.set_xlabel(r'Receiver #')
        self.ax.xaxis.tick_top()
        self.ax.xaxis.set_label_position('top')
        self.ax.set_xticks(rcxlocs)
        self.ax.set_xticklabels(rcxlocs)
        self.ax.set_ylabel(r'Two-way Travel Time (s)')
        self.ax.set_yticks(timelocs)
        self.ax.set_yticklabels(timevals)

        # Other figure handle operations
        self.ax.set_aspect(aspect = exaggeration)

        if self.is_seismic:
            self.ax.text(0, m + 0.03*m, 'x $10^{-2}$')
        else:
            self.ax.text(0, m + 0.03*m, 'x $10^{-6}$')
        
        self.ax.update_datalim( ((0,0),(m, n)))
        plt.show()
    
    # -------------------------------------------------------------------------
    def save(self):
        filename = '.'.join( 
            [
                self.prjfile.split('.')[:-1][0],
                self.channel, 
                '.'.join(self.source.astype(str)), 
                '.pkl'
            ]
        )
        # Pickle the object and save to file
        with open(filename, 'wb') as file:
            pickle.dump(self, filename)


# =============================================================================
# ========================== Command Line Arguments ===========================
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""This program creates a csv file of time series for each receiver location
        listed in the the specified receiver file.""" )
    
    parser.add_argument(
        '-p', '--prjfile',
        nargs = 1, type = str, required = True,
        help = 'The project file path'
    )
    
    parser.add_argument(
        '-r', '--rcxfile',
        nargs=1, type=str, required = True,
        help='the file path for the text file of receiver locations'
    )
    
    parser.add_argument(
        '-i', '--index',
        action = 'store_true', required = False,
        help = """Indicate whether the receiver file contains coordinate indices or
        if these are the locations in meters. Default (0 - meters)"""
    )
    
    parser.add_argument(
        '-c', '--channel',
        nargs = 1, type = str, required = True,
        help = """The channel to query. """
    )
    
    parser.add_argument(
        '-z', '--is_complex', action = 'store_true', required = False,
        help = """Flag whether the data will be complex valued. If the data is
        not flagged but is complex, only the real data will be returned. """
    )
    
    parser.add_argument(
        '-d', 'double_precision', action = 'store_false', required = False,
        help = '''Flag whether the model outputs are in double precision. 
        Default is single precision. '''
    )
    
    parser.add_argument(
        '-g', '--gain',
        nargs = 1, type = float, required = False, default = [None],
        help = "The smoothing length"
    )

    parser.add_argument(
        '-e', '--exaggeration',
        nargs=1, type = float, required = False, default = [None],
        help = """Set the aspect ratio between the x and y axes for
        plotting."""
    )
    
    parser.add_argument(
        '-s', '--save', action = 'store_true', required = False, 
        help = """Flag to save the array object as a .pkl file."""
    )
    
    # Get the arguments
    args = parser.parse_args()
    prjfile = ''.join(args.prjfile)
    receiver_file = ''.join(args.rcxfile)
    channel = ''.join(args.channel)
    rind = args.index
    is_complex = args.is_complex
    single_precision = args.double_precision 
    exaggeration = args.exaggeration[0] 
    gain = args.gain[0]
    
    # ==================== Create the object and assign inputs ====================    
    array = Array(
        channel,
        prjfile, 
        receiver_file,
        rind, 
        single_precision = single_precision,
        is_complex = is_complex
    )
    
    if gain and exaggeration:
        array.gain = gain
        array.exaggeration = exaggeration
        
    if save:
        array.save()
        