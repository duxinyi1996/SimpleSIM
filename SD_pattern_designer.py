#!/usr/bin/python
import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
	sys.path.append(folder_path) # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from Plot_pref import *
from dxf_compiler import *
from HFSS_compiler import *


folder_path = r'C:\Users\duxin\OneDrive - Washington University in St. Louis\wustl\2023 Spring\hfss\test'
# folder_path = r'/Users/chellybone/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/wustl/2023 Spring/hfss/test'
file_name = 'total_short'
project_name = os.path.join(folder_path, file_name)
start = time.time()

h = DXF(project_name)
# h.Build_part()
h.Build_all(8)
print('time spent:', time.time()-start, 's')


