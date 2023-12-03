# Modeler_sum: build_chip design SD012, has a stack
from Builds.Build_universal_functions import *

def Build_012(object, lead_number=0):
    object.sub_size_x = 50000
    object.sub_size_y = 50000
    
    object.feedline_width = 18
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    object.bond_pad_width = 300
    object.taper_l = object.bond_pad_width / 3 * 2
    object.bond_pad_l = object.bond_pad_width
    object.bond_pad_gap = 130

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw feedline
    couple_l = 130
    spacing = 20
    radius = 30
    x1 = 0
    y1 = 651
    x2 = 0
    y2 = -3548
    start = [0, y1 + (spacing + object.reson_width )* np.sign(y1)]
    stop = [0, y2 + (spacing + object.reson_width )* np.sign(y2)]
    x_list, y_list = construct(-250 + couple_l, start[1], 'x250')
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    x_list, y_list = construct(-250 + couple_l, stop[1], 'x250')
    feed_cen_2, feed_tren_2 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    object.toBeRemove += [feed_tren_1, feed_tren_2]
    object.feedline = [feed_cen_1, feed_cen_2]
    # Draw resonator
    x_list = [x1]
    y_list = [y1]
    turnings = [[1230,651],
                [1230,131],
                [2104,131],
                [2104,-611],
                [1669,-611],
                [1669,-938],
                [1269,-938],
                [1269,-1364],
                [1509,-1364],
                [1509,-1553],
                [1143,-1553],
                [1143,-1979],
                [1088,-1979],
                [1088,-3174],
                [557,-3174],
                [557,-3544]
                ]
    for turns in turnings:
        x_list += [turns[0]]
        y_list += [turns[1]]
    y_list[-1] = y2
    y_list[1] = y1
    x_list += [x2]
    y_list += [y2]

    center_line, trench = object.CPW_line(x_list, y_list, 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=radius, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]

    # Draw DC lines:
    def DC_lines(object, x, y, dy, lead_number):
        extend = 10
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
        end_y = y+object.direction*(dy+250)
        open_end = object.line(start_x=x,
                             start_y=y+object.direction*dy,
                             end_x=x,
                             end_y=end_y,
                             width=250)
        object.toBeRemove += [tren,open_end]
        object.toBeAdd += [cen]
        for i in range(lead_number):
            print('processing lead:',i )
            x1 = x + (2 * i - lead_number + 1) / 2 * (object.open_end_size_x / lead_number)
            x2 = x + (2 * i - lead_number + 1) / 2 * 280
            y1 = end_y
            if i % 2 == 0:
                y2 = y1 + object.direction * 300
            else:
                y2 = y1 + object.direction * 1000
            ym = y1 + object.direction * (lead_number / 2 + 1 - abs(i - lead_number / 2)) * 20
            ym1 = ym + object.direction * 40
            connect, connect_tren = object.CPW_line(x_list=[x1, x1, x2, x2],
                                                  y_list=[y1-object.direction*extend, ym, ym, ym1],
                                                  width=5,
                                                  gap=3,
                                                  radius=15,
                                                  name='connect'
                                                  )
            taper, taper_tren = object.CPW_taper(x_list=[x2, x2],
                                               y_list=[ym1, y2],
                                               width_list=[5, object.DCcpw_width],
                                               gap_list=[3, object.DCcpw_gap],
                                               direction='y')
            if i>1:
                object.n_finger = 12
                object.filter_in_len = 7500
            else:
                object.n_finger = 0
                object.filter_in_len = 0
            DC_lead, DC_lead_tren = object.DC_filter(x2, y2)
            DC_lead_sum = object.modeler.unite([DC_lead, taper, connect])
            object.toBeRemove += [taper_tren, DC_lead_tren, connect_tren]
            object.DCleads += [DC_lead_sum]
        return object
    object = DC_lines(object, x=x1,
                    y=y1, 
                    dy=y1-300+250/2, 
                    lead_number=lead_number)
    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()


