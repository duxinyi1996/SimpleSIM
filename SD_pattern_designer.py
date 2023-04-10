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


folder_path = r'C:\Users\xingrui\Desktop\Shilling\OneDrive_1_4-5-2023\hfss\tune_geo'

file_name = 'test_reson'
project_name = os.path.join(folder_path, file_name)
start = time.time()

h = HFSS(project_name)
h.trap = False
h.Build_part()
# h.Build_all(8)
print('time spent:', time.time()-start, 's')


