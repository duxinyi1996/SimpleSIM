from Builds.Build_universal_functions import *

def Build_hBN_waveguide(object):
    object.sub_name = 'alumina_96pct'
    object.sub_thickness = 400
    object.sub_size_x = 60000
    object.sub_size_y = 6000
    object.metal_name = 'gold'
    object.metal_thickness = 160E-3
    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2, name='Sapphire')
    object.modeler.create_air_region(x_pos=0.1, y_pos=0.1, z_pos=400, x_neg=0.1, y_neg=0.1, z_neg=10,
                                    is_percentage=True)
    print('substrate created')
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    print('ground created')

    # Draw feedline
    object.bond_pad_width = 1600
    object.bond_pad_gap = 320
    object.bond_pad_l = 20000
    object.taper_l = object.bond_pad_width / 3 * 2
    object.feedline_gap = 20
    object.feedline_width = 50
    x_list, y_list = construct(-75, 50, 'x150')
    feed_cen, feed_tren = object.Feedline(x_list=x_list, y_list=y_list)
    print('feedline created')
    object.toBeRemove += [feed_tren]
    object.feedline = [feed_cen]

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.save()