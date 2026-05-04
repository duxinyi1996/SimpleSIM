# Modeler_sum: build_chip design Boulder chip, resonator 1
from Builds.Build_universal_functions import *

def Build_Boulder(object):
    object.metal_thickness = 0
    object.sub_size_x = 1000
    object.sub_size_y = 1800
    object.sub_thickness = -525
     # Draw Substrate: Si
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2)
    object.build_region(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2, dz=4000)

    object.reson_width = 6
    object.reson_gap = 3
    
    object.toBeRemove = []
    object.toBeAdd = []

    # Draw Gnd
    object.gnd = [object.line(start_x=-object.sub_size_x / 2, start_y=0, end_x=object.sub_size_x / 2, end_y=0, width=object.sub_size_y, name='Gnd')]
    # Draw Reson
    object.openendTogap_ratio = 5/3
    x_list, y_list = construct(start_x=object.sub_size_x / 2-200, start_y=-object.sub_size_y / 2+200, shape='x76.5,y1409,x-300,y-1030.3,x-300,y1065.5')
    center_line, trench = object.CPW_line(x_list.copy(), y_list.copy(), 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=75, name='reson',
                    end=[0,1])
    
    object.modeler.subtract(trench, [center_line], keep_originals=True)
    object.fillet_corners(trench, 2.5)
    object.fillet_corners(center_line, 2.5)
    object.gnd = object.modeler.subtract(object.gnd, [trench,center_line], keep_originals=False)

    center_line_1, trench_1 = object.CPW_line(x_list.copy(), y_list.copy(), 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=75, name='reson',
                    end=[0,1])
    object.fillet_corners(center_line_1, 3)
    object.gnd = object.modeler.unite([object.gnd,center_line_1])
    # object.cpw = object.modeler.unite([center_line_1])

    '''Assign port'''
    # 1. Define the true open end coordinates from the x/y lists
    object.open_end_x = x_list[-1]
    # 2. Chop 2um off the tip to remove the fillet and gap extension
    chop_amount = 2.0
    object.open_end_y = y_list[-1] - chop_amount 
    # Draw a 100um wide rectangle that cuts the tip off the center trace and grounds
    chop_rect = object.line(start_x=object.open_end_x, start_y=object.open_end_y + 10,
                            end_x=object.open_end_x, end_y=object.open_end_y,
                            width=100, name='Chop_Rect')                 
    object.gnd = object.modeler.subtract(object.gnd, [chop_rect], keep_originals=False)

    # 3. Assign the Q3D Ports to the newly flattened edges
    object.assign_q3d_inductance_ports(combined_name=object.gnd)
    # ==========================================
    # object.add_label(2600,3000)
    object.tempsave()


