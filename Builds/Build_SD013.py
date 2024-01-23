# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_013(object, lead_number=0):
    object.metal_thickness = 0
    object.sub_size_x = 7500
    object.sub_size_y = 7500

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

    cen_x=1000
    cen_y=-1500

    # Draw Substrate
    object.substrate(cen_x=cen_x,cen_y=cen_y,dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.build_region(cen_x=cen_x,cen_y=cen_y,dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2 + cen_x, cen_y, object.sub_size_x / 2 + cen_x, cen_y, width=object.sub_size_y, name='Gnd')]
    
    # Draw CPW
    couple_l = 130
    spacing = 20
    feedline_l = 500
    # Draw feedline
    x1 = -1000 + cen_x
    y1 = 2000 + cen_y
    x2 = -1000 + cen_x
    y2 = -2000 + cen_y

    ''' Feedline Capacitively coupled'''
    start = [x1, y1 + (spacing + object.reson_width )* np.sign(y1)]
    stop = [x2, y2 + (spacing + object.reson_width )* np.sign(y2)]
    x_list, y_list = construct(start[0]-feedline_l + couple_l, start[1], f'x{feedline_l}')
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    x_list, y_list = construct(stop[0]-feedline_l + couple_l, stop[1], f'x{feedline_l}')
    feed_cen_2, feed_tren_2 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    tren_1 = object.line(start_x= x1 - object.reson_gap*object.openendTogap_ratio,
                             start_y=(y1+start[1])/2,
                             end_x=x1 + couple_l + object.reson_gap*object.openendTogap_ratio,
                             end_y=(y1+start[1])/2,
                             width=spacing)
    tren_2 = object.line(start_x= x2 - object.reson_gap*object.openendTogap_ratio,
                             start_y=(y2+stop[1])/2,
                             end_x=x2 + couple_l + object.reson_gap*object.openendTogap_ratio,
                             end_y=(y2+stop[1])/2,
                             width=spacing)
    object.toBeRemove += [feed_tren_1, feed_tren_2, tren_1, tren_2]
    object.feedline = [feed_cen_1, feed_cen_2]

    # Draw Reson
    x_list = [x1,
              x1 + 2000,
              x1 + 2000,
            #   x1 + 1500,
            #   x1 + 1500,
              x2]
    y_list = [y1,
              y1,
            #   0,
            #   0,
              y2,
              y2]
    center_line, trench = object.CPW_line(x_list, y_list, 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=300, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]

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
        object.filter_in_len = 7500

        object.DCcpw_width = 10
        object.DCcpw_gap = 6
        object.DCconnect_width = 15
        object.DCconnect_gap = 9
        object.DCconnect_radius = 30

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
            if i+1 in [2,4]:
                object.n_finger = 0
                object.filter_in_len = 0
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

    object = DC_lines(object, x=x1,
                    y=y1, 
                    dy=y1,
                   lead_number=lead_number)
    
    # Draw mid dc lead
    mid_lead, mid_lead_tren = object.single_filter(x_list=[x1+2000,x1+3500,x1+3500,x1+3500],y_list=[(y1+y2)/2,(y1+y2)/2,(y1+y2)/2-100,(y1+y2)/2-200])
    object.toBeAdd += [mid_lead]
    object.toBeRemove += [mid_lead_tren]

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()


