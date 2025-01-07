# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_SingleFilter(object, lead_number=0):
    object.metal_thickness = 0
    object.sub_size_x = 1200*2
    object.sub_size_y = 4000

    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    if object.compiler == 'hfss':
        object.bond_pad_width = 17
        object.bond_pad_gap = 10
    else:
        object.bond_pad_width = 300
        object.bond_pad_gap = 140
    
    object.taper_l = object.bond_pad_width * 2/3
    object.bond_pad_l = object.bond_pad_width
    
    object.toBeRemove = []
    object.toBeAdd = []

    # Draw Substrate
    cen_y = -1500
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2, cen_y = cen_y)
    object.build_region(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2, cen_y = cen_y)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, cen_y, object.sub_size_x / 2, cen_y, width=object.sub_size_y, name='Gnd')]
    
    # Draw DC lines:
    def DC_lines(object, x, y, dy, lead_number):
        open_x = 450
        open_y = 400
        extend = 10
        dy = dy - open_y / 2
        object.n_finger = 12  # number of fingers
        object.w_finger = 4 * 3  # width of the fingers
        object.w_finger_tren = 2.5 * 3  # width of the finger trenches
        object.s_finger = 12 * 3  # spacing between the fingers
        object.h_finger = 140  # height of the fingers
        object.filter_in_len = 10000

        object.DCcpw_width = 10
        object.DCcpw_gap = 10
        object.DCconnect_width = 15
        object.DCconnect_gap = 15
        object.DCconnect_radius = 50

        object.direction = - np.sign(y)
        tren = object.line(start_x=x,
                             start_y=y,
                             end_x=x,
                             end_y=y+object.direction*dy,
                             width=2*object.DCcpw_gap+object.DCcpw_width)
        cen = object.line(start_x=x,
                             start_y=y,
                             end_x=x,
                             end_y=y+object.direction*(dy+extend),
                             width=object.DCcpw_width)
        end_y = y + object.direction*(dy+open_y)
        open_end = object.line(start_x=x,
                             start_y=y + object.direction*dy,
                             end_x=x,
                             end_y=end_y,
                             width=open_x)
        object.toBeRemove += [tren,open_end]
        object.toBeAdd += [cen]
        n = lead_number
        if lead_number % 2 == 1:
            n += 1
        for i in range(lead_number):
            print('processing lead:',i )
            x1 = x + (2 * i - n + 1) / 2 * (open_x / n)
            x2 = x + (2 * i - n + 1) / 2 * 450
            y1 = end_y
            if i % 2 == 0:
                y2 = y1 + object.direction * 700
            else:
                y2 = y1 + object.direction * 1600
            if i+1 in [1,5]:
                object.n_finger = 0
                object.filter_in_len = 10000
                y2 += 12 * object.s_finger * object.direction
            else:
                object.n_finger = 12
                object.filter_in_len = 7500
            ym = y1 + object.direction * (n / 2 + 1 - abs(i - n / 2)) * 40 * 3
            ym1 = ym + object.direction * 40 *3
            lead, lead_tren = object.single_filter(x_list=[x1, x1, x2, x2, x2],
                                y_list=[y1-object.direction*extend, ym, ym, ym1, y2])
            object.DCleads += [lead]
            object.toBeAdd += [lead]
            object.toBeRemove += [lead_tren]
        return object

    object = DC_lines(object, x=0,
                    y=10, 
                    dy=500,
                   lead_number=lead_number)

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(0,0)
    object.save()


