#!/usr/bin/python3
'''live_adc_graph.py'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import data_adc as dataDevice

PADDING = 5
CHANNEL = 0
SCALE = 1
INTERVAL = 1000
my_data = dataDevice.Device()
dispdata = []
timeplot = 0
fig, ax = plt.subplots()
line, = ax.plot(dispdata)
time_text = ax.text(0.02, 0.95,
                    dataDevice.DATANAME[CHANNEL],
                    transform=ax.transAxes)

def update(data):
    '''Update figure'''
    global dispdata, timeplot
    timeplot += 1
    dispdata.append(data)
    ax.set_xlim(0, timeplot)
    ymin = min(dispdata) - PADDING
    ymax = max(dispdata) + PADDING
    ax.set_ylim(ymin, ymax)
    line.set_data(range(timeplot), dispdata)
    return line

def data_gen():
    '''Data generator'''
    while True:
        yield my_data.get_new()[CHANNEL]/SCALE

ani = animation.FuncAnimation(fig, update,
                              data_gen, interval=INTERVAL)
plt.show()
#End
