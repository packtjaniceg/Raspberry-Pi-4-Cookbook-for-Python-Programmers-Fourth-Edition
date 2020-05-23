#!/usr/bin/python3

''' log_graph.py '''
import numpy as np
import matplotlib.pyplot as plt

def add_plot(figure, idx):
    ''' Create a new subplot '''
    layout = DATA_COL*100+11+idx     #numrows, numcols, fignum
    sp = figure.add_subplot(layout)  #411, 412 etc
    sp.plot(DATA['ID'], DATA[HEADER[OFFSET+idx]], COLS[idx],
            label=HEADER[OFFSET+idx])
    sp.set_xlabel('Samples')
    sp.set_ylabel('Reading')
    sp.legend()

DATA_LOG = "data.log"
OFFSET = 2 #Non Data Columns
COLS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
with open(DATA_LOG) as f:
    HEADER = f.readline().split('\t')
    HEADER = [x.strip() for x in HEADER]
DATA_COL = len(HEADER)-OFFSET

DATA = np.genfromtxt(DATA_LOG, delimiter='\t',
                     skip_header=1, names=HEADER)
fig = plt.figure(1)
plt.suptitle("Data Samples")

for i in range(DATA_COL):
    add_plot(fig, i)

plt.tight_layout(pad=1.1)
plt.show()
#End
