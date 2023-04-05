# Library for General Utilities
# Written by Simone Frasca

import os
import sys
import scipy.io
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from io import StringIO
import csv


def get_path_separator_character(user_name):
    if user_name == 'Simone':
        separator = '/'
    elif user_name == 'BlueFors': 
        separator = '/'
    elif user_name == 'MacMini':
        separator = '/'
    elif user_name == 'Simo_PC':
        separator = '\\'
    return separator

def get_data_filepath(user_name):
    if user_name == 'Simone':
        data_filepath = '/Volumes/GoogleDrive/My Drive/Data/'
    elif user_name == 'Simo_PC':
        data_filepath = 'G:\\My Drive\\Data\\'
    elif user_name == 'BlueFors':
        data_filepath = '/home/arabadzh/ownCloud/Data Management/Data/'
    elif user_name == 'Sebastien':
        data_filepath = 'C:\\Users\\sebastien\\Google Drive\\Data\\'
    elif user_name == 'Ivo':
        data_filepath = 'C:\\Users\\ivoar\\My Drive\\Data\\'
    else:
        raise NameError("The user name: "+user_name+" has no data_filepath")
    return data_filepath        

def save_data_mat(dataname, data, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID + MeasurementType + sep + today + sep + roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    scipy.io.savemat(filepath + sep + filename + '.mat'  , mdict = {dataname : data})

def save_multidata_mat(multidata, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID + MeasurementType + sep + today + sep + roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    if user_name == 'Simo_PC':
        os.chdir(filepath)
        scipy.io.savemat(filename + '.mat'  , mdict = multidata) 
    else:
        scipy.io.savemat(filepath + sep + filename + '.mat'  , mdict = multidata) 

def save_data(data, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')

    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    np.savetxt(filepath+sep+filename+'.txt', data, newline = ' ')

def save_row(row, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    file = filepath+sep+filename+'.txt'
    f = open(file, 'ab')
    f.write(b'\n')
    f.close()
    with open(file, 'ab') as myfile:
        np.savetxt(myfile, row, newline = ' ')

def save_fig(figure, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    pl.savefig(filepath+sep+filename+'.png', bbox_inches='tight')
    plt.close(figure)

def save_waveform(data, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    scipy.io.savemat(filepath+sep+filename+'.mat'  , mdict = {'waveform' : data})

def save_jitter_waveforms(oscope, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    reference_data = oscope.acquire_waveform_data(2)
    channel_data = oscope.acquire_waveform_data(4)
    average_data = oscope.acquire_waveform_data(1, 'function')
    #waveforms = np.hstack([reference_data, channel_data[:,1], average_data[:,1]])
    multidata = {'time':reference_data[:,0], 'reference':reference_data[:,1], 'channel':channel_data[:,1], 'average':average_data[:,1]}
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    scipy.io.savemat(filepath+sep+filename+'.mat'  , multidata)

def write_logfile(rootsID, roots, MeasurementType, comment, user_name = 'Simone'):
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    f = open(filepath+sep+'logfile.txt','a+')
    f.write(comment+'\n')
    f.close()    

def save_hist(delay, binsize, rootsID, roots, filename, MeasurementType, user_name = 'Simone'):
    fig = plt.figure()
    maxDelay = float('%0.2e' % np.amax(delay))
    minDelay = float('%0.2e' % np.amin(delay))
    bins = int((maxDelay - minDelay)/binsize)+1
    plt.hist(delay, bins)
    today = time.strftime('%m-%d-%Y')
    filepath = get_data_filepath(user_name)
    sep = get_path_separator_character(user_name)
    filepath += rootsID+MeasurementType+sep+today+sep+roots
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    pl.savefig(filepath+sep+filename+'.png', bbox_inches='tight')
    plt.close(fig)

def readTemperature(chan, user_name = 'Simone'):
    today = time.strftime('%Y%m%d')
    # filepath = 'Z:\\@DATA_ICE\\@measurement data\\'
    if user_name == 'Simone':
        filepath = '/Users/simonefrasca/Desktop/freezecontrol2.1.8.epfl/log/'
    elif user_name == 'Ivo':
        filepath = 0
    elif user_name == 'Sebastien':
        filepath = 'C:\\Users\\seb-debros\\DATA\\Google_Drive\\freezecontrol2.1.8.2.epfl\\log\\'
    if not os.path.exists(filepath):
        return 0
    else:
        with open(filepath+today+'_log.csv', 'r') as file:
            lastLine = file.readlines()[-1]
            start = 0
            for i in np.arange(chan):
                edge = start
                start = lastLine.find(',',edge)
                start = start + 1
            end = lastLine.find(',',start)
            temperature = lastLine[start:end]
        return temperature

class ProgressBar(object):
    """Custom Progress Bar"""
    def __init__(self, maximum):
        self.max = maximum
        self.j = -1
    def update(self, i):
        perc = int(100*i/self.max)
        if perc > self.j:
            sys.stdout.write("\r"+'   |' + int(0.5*perc)*'#' + (50-int(0.5*perc))*' ' +
                             '|  ' + str(perc) + '%')
            sys.stdout.flush()
            self.j = perc
