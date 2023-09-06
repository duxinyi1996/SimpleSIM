from Builds.Build_universal_functions import *

def Build_partReson(object, lead_number=0):
    object.sub_size_x = 4000
    object.sub_size_y = 4000
    object.bond_pad_width = object.feedline_width
    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_y / 2)
    object.modeler.create_air_region(x_pos=0.1, y_pos=0.1, z_pos=400, x_neg=0.1, y_neg=0.1, z_neg=10,
                                    is_percentage=True)
    print('substrate created')
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    print('ground created')
    # Draw feedline
    x_list, y_list = construct(-1000, 1500, 'x2000')
    feed_cen, feed_tren = object.Feedline(x_list=x_list, y_list=y_list)
    print('feedline created')
    object.toBeRemove += [feed_tren]
    object.feedline = [feed_cen]

    object.draw_reson(lshort=3250, x=0, y=1500, lead_number=lead_number)
    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)

    object.save()