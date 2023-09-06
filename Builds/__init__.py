#!/usr/bin/python
import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
	sys.path.append(folder_path) # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers