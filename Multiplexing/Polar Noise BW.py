# -*- coding: utf-8 -*-
"""
Created on April 19th 2016 @author: Luke Edward Rogerson, AG Euler
"""
import collections
import csv
from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import QDS 
import seaborn as sns 

p = {'_sName'          : "Polar_flicker_0",
     '_sDescr'         : "Noise flicker distributed over a polar grid",
     'frameRate'       : 20,
     'duration'        : 180,
     'radius_max'      : 180,
     'radius_itx'      : 2,
     'radius_centre'   : 25,
     'azimuth_max'     : 2*np.pi, 
     'azimuth_itx'     : 3,  
     'iFull'           : 255,
     "nFrPerMarker"    : 1,
     "MarkPer_s"       : 1.0,         # number of markers per second
}

def buildStimulus(p):
    radius = [p['radius_centre'],p['radius_centre']+50,p['radius_centre']+100]
    azimuth = [0,120,240,360]

    domain = []
    for a in range(p['radius_itx']): 
        for b in range(p['azimuth_itx']):
            domain.append((radius[a],
                           radius[a+1],
                           azimuth[b],
                           azimuth[b+1] -azimuth[b]))
    
    p['domain'] = domain
    QDS.DefObj_Ellipse(0, p["radius_centre"]*2, p["radius_centre"]*2)
    for itx in range(len(domain)):
        QDS.DefObj_Sector(itx+1,domain[itx][1],domain[itx][0],domain[itx][2],domain[itx][3],5)
         
def iterateStimulus(p):
    folderStr = "C:\\Users\\AGEuler\\Documents\\QDSpy\\Stimuli\\Multiplexing\\"
    tableStr = 'grayscale_noise_conditions.csv' 
    f = open(folderStr+tableStr,'r')
    reader = csv.reader(f)
    condition = []
    for itx,row in enumerate(reader):
        if itx%2 == 0:
            condition.append([float(state) for state in row])

    states = [
        (0,0,0),
        (p['iFull'],p['iFull'],p['iFull']),
        (0,0,p['iFull']),
        (0,p['iFull'],0),
    ]

    for t_pnt in range(p['frameRate']*p['duration']):
        # Add marker    
        if (t_pnt%(p['MarkPer_s']*p['frameRate']) < p['nFrPerMarker']): # <- Will this work for longer duration?
            showMarker = 1
        else:
            showMarker = 0

        IND,RGB,POS,MAG,ANG,ALP = [],[],[],[],[],[]
        # Add stimulus marker
        for itx in range(7):
            IND.append(itx,)     
            RGB.append(states[int(condition[t_pnt][itx])])
            POS.append((0,0),)
            MAG.append((1,1),)
            ANG.append(0,)
        
        QDS.SetObjColor(7,IND,RGB)
        QDS.Scene_RenderEx(1/p["frameRate"],IND,POS,MAG,ANG,showMarker)

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