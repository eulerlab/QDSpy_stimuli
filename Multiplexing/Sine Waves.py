# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:32:23 2016

@author: Luke
"""
import collections
import csv
from functools import partial
import QDS
import math
import numpy as np
import random

# Define global stimulus parameters
p = {'_sName'          : "Ripple_0",
     '_sDescr'         : "Sine wave ripple",
     'seed'            : 1,
     "nTrials"         : 1, 
     "iHalf"           : 127,
     "iFull"           : 254,
     "dxStim_um"       : 100,   # Stimulus size
     "durFr_s"         : 1/60.0, # Frame duration
     'durRipple'       : 1,
     "tSteadyMID_s"    : 2,    # Light at 50% for steps
     'MarkPer_s'       : 1,
     'nFrPerMarker'    : 2,
     }
     
def buildStimulus(p):
    # Define stimulus objects
    QDS.DefObj_Ellipse(1, 50, 50)
    QDS.DefObj_Sector(2,125,25,0,360,5)
    
def iterateStimulus(p):    
    folderStr = "C:\\Users\\AGEuler\\Documents\\QDSpy\\Stimuli\\Multiplexing\\"
    tableStr = 'sine_conditions.csv' 
    f = open(folderStr+tableStr,'r')
    reader = csv.reader(f)
    conditions = []
    for itx,row in enumerate(reader):
        if itx%2 == 0:
            conditions.append([float(state) for state in row])

    bkg_clr = (0,0,0)

    pause_counter = 0
    for (condition,frequency,contrast) in conditions:
        if pause_counter == 0:
            QDS.Scene_Clear(0.05, 1)
            QDS.Scene_Clear(0.95, 0)
            pause_counter = 16
        
        pause_counter -=1
        for itx in range(int(p['durRipple']/p['durFr_s'])):
            t_pnt = itx*p['durFr_s']

            # Add marker    
            if (itx%(p['MarkPer_s']/p['durFr_s']) < p['nFrPerMarker']):
                showMarker = 1
            else:
                showMarker = 0
            
            # Calculate stimulus intensity
            Intensity = math.sin(2*math.pi*frequency*t_pnt)*contrast/100*p["iHalf"]+p["iHalf"]
            RGB = (int(Intensity),int(Intensity),int(Intensity))
            
            # Set object intensity
            obj_colour = {
                0: [RGB,bkg_clr,], # Centre only  
                1: [bkg_clr,RGB,], # Annulus only  
                2: [RGB,RGB,],     # Centre and Annulus
            }

            QDS.SetObjColor(2, [1,2], obj_colour[condition-1])
            QDS.Scene_Render(p["durFr_s"], 2, [1,2], [(0,0),(0,0)], showMarker)    

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize,p['_sName'],p['_sDescr'])),
    ('log', partial(QDS.LogUserParameters,p)),
    ('build', partial(buildStimulus,p)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear,1.0, 0)),
    ('iter', partial(iterateStimulus,p)),
    ('clear2', partial(QDS.Scene_Clear,1.0, 0)),
    ('stop', QDS.EndScript)]                               
)

[dispatcher[process]() for process in list(dispatcher.keys())]