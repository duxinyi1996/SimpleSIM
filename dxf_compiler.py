import os,sys
import klayout.db as db

import numpy as np

class dxf:
	def __init__(self):
		self.ly = db.layout()
		self.ly.dbu = 1 # sets the database unit to 1 um

	def add_layer(self):
		top_cell = self.ly.create_cell("SAMPLE")
		layer1 = self.ly.layer(1, 0)