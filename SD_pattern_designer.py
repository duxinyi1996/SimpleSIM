#!/usr/bin/python
import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
	sys.path.append(folder_path)

from Compiler.dxf_compiler import *
from Compiler.HFSS_compiler import *

# from Builds.Build_SD009 import *
# folder_path = r'/Users/chellybone/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/wustl/HLab/Project_MLGM/Fab_files/SD_010'
# file_name = 'Test_009'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()
# # h = HFSS(project_name)
# # h.trap = False
# # Build_hBN_waveguide(h,)
# h = DXF(project_name)
# h.trap = True
# Build_009(h,8)
# print('time spent:', time.time()-start, 's')

from Builds.Build_SD011 import *
# folder_path = r'C:\Users\duxin\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Fab_files\SD_011'
folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Fab_files\SD_011'
file_name = 'SD011AddDCtext'
project_name = os.path.join(folder_path, file_name)
start = time.time()
# h = DXF(project_name)
h = DXF(project_name)
h.trap = 0
Build_011(h,lead_number=8)
print('time spent:', time.time()-start, 's')
