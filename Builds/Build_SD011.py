# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_011(object, lead_number=0):
    object.sub_size_x = 7500
    object.sub_size_y = 7500
    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    object.bond_pad_width = 300
    object.taper_l = object.bond_pad_width / 3 * 2
    object.bond_pad_l = object.bond_pad_width
    object.bond_pad_gap = 90

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw feedline
    x_list, y_list = construct(-1500, 2000, 'x500')
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    x_list, y_list = construct(-1500, -2000, 'x500')
    feed_cen_2, feed_tren_2 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    object.toBeRemove += [feed_tren_1, feed_tren_2]
    object.feedline = [feed_cen_1, feed_cen_2]

    # Draw resonator
    couple_l = 200
    spacing = 20
    radius = 150
    start = [-1000,2000]
    stop = [1000,-2000]
    total_l = 11000
    def meander_1(start,stop,couple_l,spacing,total_l,radius,x_turns1,x_turns2):
        x1 = start[0] - couple_l
        y1 = start[1]- (spacing + object.reson_width )* np.sign(start[1])
        x2 = stop[0] - couple_l
        y2 = stop[1]- (spacing + object.reson_width )* np.sign(stop[1])
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
           print(direction)
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
    
    def meander_2(start,stop,couple_l,spacing,total_l,radius,x_turns1,*args):
        x1 = start[0] - couple_l
        y1 = start[1]- (spacing + object.reson_width )* np.sign(start[1])
        x2 = stop[0] + couple_l
        y2 = stop[1]- (spacing + object.reson_width )* np.sign(stop[1])
        remain = total_l - abs(x1-x2) - abs(y1-y2) - 2*abs(x_turns1)
        turns = remain//(2*2*abs(x_turns1))
        shift = remain%(2*2*abs(x_turns1))
        print(remain,turns,shift)
        x = x1
        y = y1
        command = []
        command += [f'x{(x_turns1-x1)},']
        x += (x_turns1-x1)
        direction = np.sign(x_turns1-x1)
        for i in range(turns):
           command += [f'y{2*radius*np.sign(y2-y1)},']
           y -= 2*radius
           direction = -direction
           command += [f'x{(2*x_turns1)*direction},']
           x += (2*x_turns1)*direction
        command += [f'y{2*radius*np.sign(y2-y1)},']
        y -= 2*radius
        command += [f'x{(int(shift/2))*(-direction)},']
        x += (int(shift/2))*(-direction)
        mid_command = f'y{-y},x{-2*x},y{-y},'
        all_command = ''
        for x in command:
            all_command += str(x)
        all_command += mid_command
        for x in reversed(command):
            all_command += str(x)
        return x1,y1,all_command
    
    
    x1,y1,all_command = meander_1(start,stop,couple_l,spacing,total_l,radius,x_turns1=1500,x_turns2=1000)
    # x1,y1,all_command = meander_2(start,stop,couple_l,spacing,total_l,radius,x_turns1=500)
    print(all_command)
    x_list, y_list = construct(start_x=x1, start_y=y1, shape=all_command)
    center_line, trench = object.CPW_line(x_list, y_list, 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=radius, name='reson',
                    end=[1,1])
    
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]
    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.save()


