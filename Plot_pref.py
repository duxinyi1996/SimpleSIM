#!/usr/bin/python

import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
	sys.path.append(folder_path) # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy import signal
from qutip import *

# Font
font = {'family': "Arial",
	"weight": 'bold',
	"size":12}
mpl.rc("font",**font)
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.bf'] = 'sans:italic:bold'

# Linewidth
linewidth = 1
mpl.rcParams['axes.linewidth'] = linewidth
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['lines.linewidth'] = linewidth
mpl.rcParams['xtick.major.width'] = linewidth
mpl.rcParams['xtick.major.size'] = 2
mpl.rcParams['ytick.major.width'] = linewidth
mpl.rcParams['ytick.major.size'] = 2
mpl.rcParams['legend.fontsize'] = 9

# layout
fig_size = np.asarray([8.5,8.5])
fig_size = fig_size / 2.54