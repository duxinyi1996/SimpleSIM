# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_009(object, lead_number=0):
    object.sub_size_x = 7500
    object.sub_size_y = 7500
    object.reson_l_couple = 700
    object.reson_l_open = 1000

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw feedline
    x_list, y_list = construct(-2500, 2750, 'x5500,y-5500,x-5500')
    feed_cen, feed_tren = object.Feedline(x_list=x_list, y_list=y_list)
    object.toBeRemove += [feed_tren]
    object.feedline = [feed_cen]

    # Draw resonator
    object.reson_couple_d = 10
    object.draw_reson(lshort=5200, x=-1500, y=2750, lead_number=lead_number)
    object.reson_couple_d = 11
    object.draw_reson(lshort=4900, x=1500, y=2750, lead_number=lead_number)
    object.reson_couple_d = 11
    object.draw_reson(lshort=4600, x=-1500, y=-2750, lead_number=lead_number)
    object.reson_couple_d = 13
    object.draw_reson(lshort=4300, x=1500, y=-2750, lead_number=lead_number)

    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.save()