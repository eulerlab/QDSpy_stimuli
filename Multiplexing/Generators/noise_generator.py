import csv
import numpy as np
import os
import random

p = {
    'duration': 180,
    'framerate': 20,
    'domains' : 7,
    'nConds': 4,
    }
  

condition = []
for itx in range(p['duration']*p['framerate']):
    condition.append(np.random.randint(0,p['nConds'],size=p['domains']))


# os.chdir("C:\Users\eulerlab\Desktop")

f = open('coloured_noise_conditions.csv', 'w')
writer = csv.writer(f)
writer.writerows(condition)
f.close()


"""
# CSV Table Reader
import csv

tableName = 'sineTable.csv' 
f = open(tableName,'r')
reader = csv.reader(f)
condition = []
for row in reader:
    condition.append([float(row[0]),float(row[1]),float(row[2])])
"""
