# Class Library for Rohde & Schwartz Hardware
# Written by Simone Frasca

import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
import struct
import sys


class ZNB(object):
    """This python class is developed in order to have a fully operational
    script for the Vector Network Analyzer from Rodhe Schwartz.
    Written by Simone Frasca"""

    def __init__(self, visa_name):
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visa_name)
        self.pyvisa.timeout = 10000 # Set response timeout (in milliseconds)
    
    def read(self):
        return self.pyvisa.read()

    def write(self, string):
        self.pyvisa.write(string)

    def query(self, string):
        return self.pyvisa.query(string)

    def set_avgfact(self, chan = 1, avgfact = 15):
        "Average Factor ranges from 1 to 15"
        self.write('sens'+str(chan)+':average 1')
        self.write('sens'+str(chan)+':average:count '+str(avgfact))
        
    def set_avgoff(self, chan = 1):
        "Sets Average Off"
        self.write('sens'+str(chan)+':average 0')
        
    def set_IFBW(self, bandwidth):
        "Sets the proper Bandwidth"
        self.write('sens1:bandwidth '+str(bandwidth))
        
    def set_trigger(self):
        "Sets the Trigger to single"
        
    def acquire(self):
        self.write(':INITIATE1:IMMEDIATE; *WAI')
        
    def set_sweep(self, Min_Freq, Max_Freq, numPoints):
        self.write('sense1:sweep:points '+str(numPoints))
        self.write('sense1:frequency:start '+str(Min_Freq))
        self.write('sense1:frequency:stop '+str(Max_Freq))
        
    def autoscale(self):
        self.write('DISP:WIND:TRAC:Y:AUTO ONCE')
        
    def collect_MagAndPhas(self):
        self.acquire()
        data = np.array(list(eval(self.query(':CALCULATE1:DATA:channel:all? FDATA'))))
        npoints = int(self.query('sense1:sweep:points?'))
        magData = data[0:npoints]
        phasData = data[npoints:]
        return magData, phasData
    
    def collect_ComplexData(self):
        "collect the data of the current trace and output the complex trace value."
        self.acquire()
        cstring = self.query('calculate:Data? Sdata')
        real, im = np.reshape(np.array(cstring.split(','),dtype=float),(-1,2)).T
        return real + 1j*im
    
    def getMin(self):
        self.write('calc:par:sel \'Trc1\'')
        self.write(':calculate1:marker1 on')
        minVal = self.query(':calculate1:marker1:function:execute min; res?')
        minVal = float(minVal[0:10])
        return minVal
    
    def set_power(self, powerVal):
        "Power value goes in dBm"
        self.write('source:power '+str(powerVal))
        
    def turn_off(self):
        self.write('output off')
        
    def turn_on(self):
        self.write('output on')
        
    def AutoDelayCorrection(self):
        self.write(':correction:edelay:auto once')
    
    def reset(self):
        self.write('*RST')
        
    def startup_measurement(self):
        self.write('*RST')
        self.write('calculate1:parameter:sdefine \'Trc2\', \'S21\'')
        self.write('calculate1:format phase')
        self.write('display:window2:state on')
        self.write('display:window2:trace2:feed \'Trc2\'')
        self.write('initiate:continuous:all off')











class FSW(object):
    """This python class is developed in order to have a fully operational
    script for the Vector Network Analyzer from Rodhe Schwartz.
    Written by Simone Frasca"""

    def __init__(self, visa_name):
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visa_name)
        self.pyvisa.timeout = 10000 # Set response timeout (in milliseconds)
    
    def read(self):
        return self.pyvisa.read()

    def write(self, string):
        self.pyvisa.write(string)

    def query(self, string):
        return self.pyvisa.query(string)
        
    def set_RBW(self, bandwidth):
        "Sets the proper RBW Bandwidth"
        self.write('sense:bandwidth '+str(bandwidth)) 
    
    def set_input_coupling(self, coupling_type):
       "Set Proper input coupling. The coupling type is either AC or DC"
       self.write('inp:coup '+coupling_type)   
       
    def set_input_impedance(self, impedance):
        "Set the input impeance typically 50 "
        self.write('inp:imp '+str(impedance))
        
    def set_VBW(self,bandwidth):
        "Sets the VBW bandwidth"
        self.write('bandwidth:video '+str(bandwidth))
        
    def set_trig(self, level):
        "This allows to select the trigger source (page 983). The source can either be : ext, ext2, ext3."
        "For triggering or IMM for free run. Only the port 1 is implemented. Minimum level is 0.5 V"
        self.write('trig:sour ext')
        self.write('trig:slop pos')
        self.write('trig:lev '+str(level))
    
    def set_continuous(self,continuous):
        "Sets the continuous mode either on or off"
        self.write('init:cont '+continuous)
        
        
    def set_display(self, dispVal):
        if dispVal:
            self.write('display:enable ON')
        else:
            self.write('display:enable OFF')
        
    def get_spectrum(self):
        startfreq = float(self.query('freq:start?'))
        stopfreq = float(self.query('freq:stop?'))
        sweepPoints = int(self.query('sweep:points?'))
        self.write('initiate:immediate; *WAI')
        self.write('trace:data? trace1')
        cstring = self.pyvisa.read_raw()
        cstring = str(cstring)[2:-3]
        values = np.reshape(np.array(cstring.split(','),dtype=float),(sweepPoints, 1))
        frequencies = np.linspace(startfreq, stopfreq, sweepPoints)
        return [frequencies, values]
        
    def set_sweep(self, Min_Freq, Max_Freq, numPoints):
        self.write('sweep:points '+str(numPoints))
        self.write('freq:start '+str(Min_Freq))
        self.write('freq:stop '+str(Max_Freq))
        
        
    def set_center_freq(self,center_freq):
        "Sets the center frequency"
        self.write("freq:cent "+str(center_freq))
        
    def set_center_freq_up_mode(self,Delta):
         "Sets the center frequency in a mode such that you can easily increase it by steps with the function set_center_freq_up"
         self.write("freq:cent:step "+str(Delta))
         
    def set_center_freq_up(self):
        "increase the center frequency by the step defined in the function set_center_freq_up_mode"
        self.write("freq:cent up") #increase the center frequency by the step defined in the function 
        
        
    def set_span(self,span):
        "sets the frequency span"
        self.write("freq:span "+str(span))
        
    def set_noise_correction(self,noise_correction):
        "activate the noise correction feature"
        if noise_correction:
            self.write("POW:NCOR ON")
        else :
            self.write("POW:NCOR OFF")
            
    def set_attenuation(self, attenuation):
        "sets the value of the electronic attenuation"
        self.write("inp:att:auto off")
        self.write("inp:att "+str(attenuation)+"dB")
        
    def set_range(self,range):
        self.write("disp:trac:y "+str(range)+"dB")
    
    
    def reset(self):
        self.write('*RST')
    
    def collect_spectrum(self):
        "This allows to collect the spectrum after the triger has been activated"
        
        startfreq = float(self.query('freq:start?'))
        stopfreq = float(self.query('freq:stop?'))
        sweepPoints = int(self.query('sweep:points?'))
        #Wait to be down acquire and then 
        self.write('*WAI; trace:data? trace1') #page 1066 - collect the trace 
        cstring = self.pyvisa.read_raw() # read the raw data for the collected trace 
        cstring = str(cstring)[2:-3]
        values = np.reshape(np.array(cstring.split(','),dtype=float),(sweepPoints, 1))
        frequencies = np.linspace(startfreq, stopfreq, sweepPoints)
        
        
        return [frequencies, values]
    












        
        
class SGS100(object):
    """This python class is developed in order to have a fully operational
    script for the I/Q Signal Generator from Rohde Schwartz.
    Written by Simone Frasca"""

    def __init__(self, visa_name):
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visa_name)
        self.pyvisa.timeout = 10000 # Set response timeout (in milliseconds)
    
    def read(self):
        return self.pyvisa.read()

    def write(self, string):
        self.pyvisa.write(string)

    def query(self, string):
        return self.pyvisa.query(string)

    def set_frequency(self, freq):
        "Frequency goes in Hz"
        self.write('source:frequency:cw '+str(freq))
    
    def set_power(self, powerVal):
        "Power value goes in dBm"
        self.write('source:power '+str(powerVal)+'dBm')
        
    def turn_off(self):
        self.write('output off')
        
    def turn_on(self):
        self.write('output on')
        
    def reset(self):
        self.write('*RST')
        

        
class HMC8012(object):
    """This python class is developed in order to have a fully operational
    script for the Voltmeter of Rodhe Schwartz.
    Written by Simone Frasca"""

    def __init__(self, visa_name):
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visa_name)
        self.pyvisa.timeout = 10000 # Set response timeout (in milliseconds)
    
    def read(self):
        return self.pyvisa.read()

    def write(self, string):
        self.pyvisa.write(string)

    def query(self, string):
        return self.pyvisa.query(string)
    
    def measure(self):
        value = self.query('READ?')
        return float(value)
    


