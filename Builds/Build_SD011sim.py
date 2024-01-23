# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_11mm_straight(object, lead_number=0):
    object.sub_size_x = 13000
    object.sub_size_y = 1000
    
    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw CPW
    center_line, trench = object.CPW_line([-5500,5500], [0,0], 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=300, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()

def Build_Utype(object, lead_number=0):
    object.metal_thickness = 0
    object.sub_size_x = 7500
    object.sub_size_y = 7500

    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    # object.bond_pad_width = 300
    # object.bond_pad_gap = 140
    object.bond_pad_width = 17
    object.bond_pad_gap = 10
    object.taper_l = object.bond_pad_width * 2/3
    object.bond_pad_l = object.bond_pad_width
    
    object.toBeRemove = []
    object.toBeAdd = []

    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.build_region(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    
    # Draw CPW
    couple_l = 130
    spacing = 20
    feedline_l = 500
    # Draw feedline
    x1 = -1000
    y1 = 2000
    x2 = -1000
    y2 = -2000

    ''' Feedline Capacitively coupled'''
    start = [x1, y1 + (spacing + object.reson_width )* np.sign(y1)]
    stop = [x2, y2 + (spacing + object.reson_width )* np.sign(y2)]
    x_list, y_list = construct(start[0]-feedline_l + couple_l, start[1], f'x{feedline_l}')
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    x_list, y_list = construct(stop[0]-feedline_l + couple_l, stop[1], f'x{feedline_l}')
    feed_cen_2, feed_tren_2 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    tren_1 = object.line(start_x=x1 - object.reson_gap*2,
                             start_y=(y1+start[1])/2,
                             end_x=x1 + couple_l + object.reson_gap*2,
                             end_y=(y1+start[1])/2,
                             width=spacing)
    tren_2 = object.line(start_x=x2 - object.reson_gap*2,
                             start_y=(y2+stop[1])/2,
                             end_x=x2 + couple_l + object.reson_gap*2,
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
                    radius=30, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]

    # Draw mid dc lead
    mid_lead, mid_lead_tren = object.single_filter(x_list=[x1+2000,x1+3500,x1+3500],y_list=[0,0,-100])
    object.toBeAdd += [mid_lead]
    object.toBeRemove += [mid_lead_tren]

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()


