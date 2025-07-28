#!/usr/bin/python
import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
	sys.path.append(folder_path)

from Compiler.Klayout_compiler import *
from Compiler.HFSS_compiler import *

from Builds.Build_SD013_test import *
folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Designs\SD013test'
file_name = 'SD013test_bareline_2025'
project_name = os.path.join(folder_path, file_name)
start = time.time()
h = HFSS(file_name)
h.trap = 0
Build_013_test(h,lead_number=0)
print('time spent:', time.time()-start, 's')

# from Builds.Build_SD009 import *
# folder_path = r'/Users/chellybone/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/wustl/HLab/Project_MLGM/Fab_files/SD_010'
# file_name = 'Test_009'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()
# # h = HFSS(project_name)
# # h.trap = False
# # Build_hBN_waveguide(h,)
# h = KLAYOUT(project_name)
# h.trap = True
# Build_009(h,8)
# print('time spent:', time.time()-start, 's')

# from Builds.Build_SD011_debug import *
# from Builds.Build_SD014 import *
# # folder_path = r'C:\Users\duxin\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Fab_files\SD_011'
# folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Designs\SD014'
# file_name = 'temp_sim'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()
# # h = KLAYOUT(project_name)
# h = HFSS(project_name)
# h.trap = 0
# Build_Utype(h,lead_number=3)
# print('time spent:', time.time()-start, 's')

# from Builds.Build_SD012 import *
# folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Fab_files\SD_012'
# file_name = 'SD012_removePad'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()
# # h = KLAYOUT(project_name)
# h = HFSS(project_name)
# h.trap = 0
# Build_012(h,lead_number=2)
# print('time spent:', time.time()-start, 's')

# from Builds.Build_SD013 import *
# folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Designs\SD013'
# file_name = 'temp_sim'

# # folder_path = r'C:\Users\xingrui\OneDrive - Washington University in St. Louis\wustl\HLab\Project_MLGM\Fab_files\SD_013'
# # file_name = 'SD013_121123'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()

# h.trap = 0
# Build_013(h,lead_number=2)
# print('time spent:', time.time()-start, 's')

# from Builds.Build_100nH import *
# # folder_path = r'D:\OneDrive - Washington University in St. Louis\wustl\HLab\Project_gPhotonDetector\Design'
# file_name = '100nH_generated'
# project_name = os.path.join(folder_path, file_name)
# start = time.time()
# # h = DXF(project_name)
# h = HFSS(file_name)
# # h.trap = 0
# Build_SingleFilter(h,lead_number=1)
# print('time spent:', time.time()-start, 's')

from Builds.Build_100nH import *
folder_path = r'D:\OneDrive - Washington University in St. Louis\wustl\HLab\Project_gPhotonDetector\Design'
file_name = '100nH_generated'
project_name = os.path.join(folder_path, file_name)
start = time.time()
h = KLAYOUT(project_name)
# h = HFSS(project_name)
h.trap = 0
Build_SingleFilter(h,lead_number=1)
print('time spent:', time.time()-start, 's')

