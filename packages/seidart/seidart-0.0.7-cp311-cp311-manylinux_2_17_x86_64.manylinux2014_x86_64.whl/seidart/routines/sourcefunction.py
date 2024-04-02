#!/usr/bin/env python3

"""Build the source function. The default is an impulse function with center 
frequency f0, but we can also generate other wavelets and chirplets."""

import argparse
import numpy as np 
from seidart.routines.definitions import *
from scipy import signal
import matplotlib.pyplot as plt 
from scipy.io import FortranFile 
import scipy.signal

# ================================ Definitions ================================
def wavelet(timevec, f, stype):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :param :  
    :type : 
    
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # Create the wavelet given the parameters
    a = np.pi**2 * f**2
    to = 1/f
    if stype == 'gaus0':
        x = np.exp(-a*(timevec - to)**2)
    if stype == "gaus1":
        x = - 2.0 * a * (timevec - to) * np.exp(-a * ((timevec - to)**2))    
    if stype == "gaus2":
        x = 2.0 * a * np.exp(-a * (timevec - to)**2) * (2.0 * a * (timevec - to)**2 - 1)
    if stype == "chirp":
        f
        x = signal.chirp(timevec, 10*f, to, f, phi = -90)    
    if stype == "chirplet":
        x = signal.chirp(timevec, f, to, 20*f, phi = -90)
        g = np.exp(-(a/4)*(timevec - to)**2)
        x = x * g        
    x = x/x.max()
    return(x)

def multimodesrc(timevec, f, stype):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # Create a double octave sweep centered at f0 from the addition of multiple
    # sources. 
    # The change will be linear in 1/8 octave steps
    fmin = f0/4 
    fmax = f0
    df = (f0 - f0/2)/8
    f = np.arange(fmin, fmax, df)
    stf = np.zeros([len(timevec)])
    for freq in f:
        stf = stf + wavelet(timevec, freq, stype)
    return(stf)

def plotsource(t, x):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    fs = 1/np.mean(np.diff(t) )
    f, pxx = signal.welch(x, fs = fs)
    db = 10*np.log10(pxx)
    fig, ax = plt.subplots(2)
    ax[0].plot(t, x, '-b')
    ax[0].set( xlabel = 'Time (s)', ylabel= 'Amplitude')
    ax[1].plot(f, db, '-b')
    ax[1].set(xlabel = 'Frequency (Hz)', ylabel = 'Power (dB)')
    ax[1].set_xlim([f.min(), np.min([20*f0, f.max()])] )
    return(fig,ax)

def writesrc(fn, srcarray):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    f = FortranFile(fn, 'w')
    f.write_record(srcarray)
    f.close()

def sourcefunction(modelclass, factor, source_type, model_type, multimodal = False):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # Create the source 
    N = int(modelclass.time_steps)
    timevec = np.linspace(1, N, num = N ) * \
        float(modelclass.dt)
    f0 = float(modelclass.f0)

    # Create the source function
    if multimodal:
        srcfn = factor * multimodesrc(timevec, f0, source_type)
    else:
        srcfn = factor * wavelet(timevec, f0, source_type)
    # rotate 
    theta = np.pi * modelclass.theta * 180
    phi = np.pi * modelclass.phi * 180
    forcex = np.sin( theta ) * np.cos( phi ) * srcfn
    forcey = np.sin( theta ) * np.sin( phi ) * srcfn
    forcez = np.cos( theta ) * srcfn
    if model_type == 's' or model_type == 'seismic':
        writesrc("seismicsourcex.dat", forcex)
        writesrc("seismicsourcey.dat", forcey)
        writesrc("seismicsourcez.dat", forcez)
    if model_type == 'e' or model_type == 'electromag':
        writesrc("electromagneticsourcex.dat", forcex)
        writesrc("electromagneticsourcey.dat", forcey)
        writesrc("electromagneticsourcez.dat", forcez)
    return(timevec, forcex, forcey, forcez, srcfn)

# --------------------------- Command Line Arguments --------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = """We support building a few different source time 
        functions and writing them to a text file. From a specified project 
        file we can create the time series for a source function and save it 
        in a Fortran formatted .dat file. 
        """
    )

    parser.add_argument(
        '-p', '--projectfile', nargs = 1, type = str, required = True,
        help = """The path to the project file"""
    )

    parser.add_argument(
        '-S', '--sourcetype', nargs = 1, type = str, required = False, 
        default = "gaus0",
        help = """Specify the source type. Available wavelets are: 
        gaus0, gaus1, gaus2 (gaussian n-th derivative), chirp, chirplet, 
        multimodal. (Default = gaus0)"""
    )

    parser.add_argument(
        '-m', '--modeltype', nargs = 1, type = str, required = False, 
        default = 's',
        help = """Specify whether to construct the source for an em or seismic
        model. s-seismic, e-electromagnetic, b-both"""
    )

    parser.add_argument(
        '-a', '--amplitude', nargs = 1, type = float, required = False,
        default = 1.0,
        help = """Input the scalar factor for source amplification. 
        (Default = 1.0)"""
    )

    parser.add_argument(
        '-M', '--multimodal', action='store_true',
        help = """Multimodal source is computed across 2 octaves at 1/8 steps 
        and centered at f0 """
    )

    parser.add_argument(
        '-P', '--plot', action='store_true',
        help = """Plot the source and spectrum"""
    )


    args = parser.parse_args()
    prjfile = ''.join(args.projectfile)
    source_type = ''.join(args.sourcetype)
    factor = args.amplitude[0]
    model_type = ''.join(args.modeltype)
    multimodal = args.multimodal 
    plotbool = args.plot
    #
    # Load the project file 
    # Let's initiate the domain
    domain, material, seismic, electromag = loadproject(
        prjfile, 
        Domain(), 
        Material(), 
        Model(), 
        Model()
    )
    if model_type == 's' or model_type == 'seismic':
        timevec, fx, fy, fz, srcfn = sourcefunction(
            seismic, 
            factor, 
            source_type, 
            model_type, 
            multimodal = multimodal
        )
    if model_type == 'e' or model_type == 'electromagnetic':
        timevec, fx, fy, fz, srcfn = sourcefunction(
            electromag, 
            factor, 
            source_type, 
            model_type, 
            multimodal = multimodal
        )
    if plotbool:
        plotsource(timevec, srcfn)
        plt.show()







