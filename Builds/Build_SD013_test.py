# Modeler_sum: build_chip design SD013, has a stack
from Builds.Build_universal_functions import *

def Build_013_test(object, lead_number=0):
    object.sub_size_x = 7500
    object.sub_size_y = 7500
    
    object.feedline_width = 20
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
    feedline_l = 250
    couple_l = 130
    spacing = 25
    radius = 30
    x1 = 0
    y1 = 2500
    x2 = 0
    y2 = -2500

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
    # Draw resonator
    total_l = 8500 # for SD_013
    def meander_1(x1,y1,x2,y2,total_l,radius,x_turns1,x_turns2):
        remain = total_l - abs(x_turns1-x1) - abs(x_turns1-x2) - abs(y1-y2)
        turns = remain//(2*abs(x_turns1 - x_turns2))
        shift = remain%(2*abs(x_turns1 - x_turns2))
        print(remain,turns,shift)
        x = x1
        y = y1
        command = []
        command += [f'x{x_turns1-x1},']
        direction = np.sign(x_turns1-x1)
        for i in range(turns):
           command += [f'y{2*radius*np.sign(y2-y1)},']
           y -= 2*radius
           direction = -direction
        #    print(direction)
           command += [f'x{(x_turns1-x_turns2)*direction},']
        command += [f'y{2*radius*np.sign(y2-y1)},']
        y -= 2*radius
        command += [f'x{(int(shift/2))*(-direction)},']
        mid_command = f'y{-2*y},'
        back_command = []
        for c in reversed(command):
            if "x" in c:
                num = -int(c[1:-1])
                c = 'x' + f'{num},'
            back_command += [c]    
        all_command = ''
        for x in command:
            all_command += str(x)
        all_command += mid_command
        for x in  back_command:
            all_command += str(x)
        return x1,y1,all_command
    x1,y1,all_command = meander_1(x1,y1,x2,y2,total_l,radius=150,x_turns1=1500,x_turns2=1000)
    x_list, y_list = construct(start_x=x1, start_y=y1, shape=all_command)
    center_line, trench = object.CPW_line(x_list, y_list, 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=radius, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]
    
    # Construct all
    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()

