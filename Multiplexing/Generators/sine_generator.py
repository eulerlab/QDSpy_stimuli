import csv
import numpy as np
import os
import random

p = {
    'nTrials': 10,
    'condition_modes': 3,
    'contrast_values' :[25,50.0,100.0],
    'frequency_values':[2,4,8],
    }
  
contfreq_pairs = [(x,y) for x in p['frequency_values'] for y in p['contrast_values']]
condition = []
shape_conditions = np.linspace(1,p['condition_modes'],p['condition_modes'],dtype='int32')
for itx in range(p['nTrials']):
    random.shuffle(contfreq_pairs)
    random.shuffle(shape_conditions)
    shape = random.randint(0,p['condition_modes']-1)
    for shape in shape_conditions:
        for contrast,frequency in contfreq_pairs:
            condition.append([shape,contrast,frequency])

# os.chdir("C:\Users\eulerlab\Desktop")

f = open('sine_conditions.csv', 'w')
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
