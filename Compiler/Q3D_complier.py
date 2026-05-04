import os, sys

folder_path = os.getcwd()
if folder_path not in sys.path:
    sys.path.append(
        folder_path)  # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import os
import time
from datetime import datetime
import ansys.aedt.core as pyaedt
import numpy as np

from Compiler.HFSS_compiler import *

class Q3D(HFSS):
    """
    Inherits all geometry methods from HFSS, but runs them in the Q3D Extractor
    for low-frequency / DC inductance and capacitance matrix extraction.
    """
    
    def startup(self):
        """
        OVERRIDES the parent HFSS startup method.
        When Q3D('ProjectName') is called, it will use this method to launch Q3D.
        """
        self.non_graphical = False
        self.desktop = pyaedt.Desktop(non_graphical=self.non_graphical, 
                                      new_desktop=False, 
                                      close_on_exit=False,
                                      student_version=False, 
                                      version='2025.2')
        
        self.q = pyaedt.Q3d(project=self.project_name)
        self.modeler = self.q.modeler
        self.unit = 'um'
        self.modeler.model_units = self.unit
        self.desktop.disable_autosave()

    def assign_q3d_inductance_ports(self, combined_name):
        """
        Automates Q3D Source/Sink assignment for a UNITED resonator/ground object.
        """
        # If the unite method returns a list, grab the string name
        if isinstance(combined_name, list):
            combined_name = combined_name[0]
            
        open_x = self.open_end_x
        open_y = self.open_end_y
        tolerance = 1e-3

        all_edges = self.modeler.get_object_edges(combined_name)

        source_edge = None
        sink_edges = []

        # Find the edges exactly on our sliced flat plane
        for edge in all_edges:
            mid_x, mid_y, mid_z = self.modeler.get_edge_midpoint(edge)
            
            if abs(mid_y - open_y) < tolerance:
                # If the midpoint X aligns with the center, it's the center trace!
                if abs(mid_x - open_x) < tolerance:
                    source_edge = edge
                # If it's on the chopped plane but NOT the center trace, it must be the ground Sinks!
                else:
                    sink_edges.append(edge)

        # Assign Source
        if source_edge:
            self.q.assign_source_to_object_edge(combined_name, source_edge, source_name="Res_Source")
            print(f"[Info] Assigned Source to Center Trace.")
        else:
            print(f"[Error] Could not find Source edge near {open_x}, {open_y}")

        # Assign Sinks
        if sink_edges:
            for i, edge in enumerate(sink_edges):
                self.q.assign_sink_to_object_edge(combined_name, edge, sink_name=f"Res_Sink_{i}")
            print(f"[Info] Assigned {len(sink_edges)} Sinks to the Ground Plane.")
        else:
            print("[Error] Could not find Ground Sink edges.")