# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_taper(object, lead_number=0):
    object.sub_size_x = 1000
    object.sub_size_y = 1000
    
    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    object.bond_pad_width = 300
    object.bond_pad_gap = 130
    object.taper_l = object.bond_pad_width * 2 / 3
    object.bond_pad_l = object.bond_pad_width

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2)
    object.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw Feedline
    x_list=[-200,200]
    y_list=[0,0]
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=True)
    object.toBeRemove += [feed_tren_1]
    object.feedline = [feed_cen_1]

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.add_label(2600,3000)
    object.save()