# Modeler_sum: build_chip design SD009
from Builds.Build_universal_functions import *

def Build_011(object, lead_number=0):
    object.sub_size_x = 7500
    object.sub_size_y = 7500
    # object.feedline_width = 25
    object.feedline_width = 17
    object.feedline_gap = 10
    object.reson_width = object.feedline_width
    object.reson_gap = object.feedline_gap

    object.bond_pad_width = 300
    object.taper_l = object.bond_pad_width / 3 * 2
    object.bond_pad_l = object.bond_pad_width
    # object.bond_pad_gap = 127
    object.bond_pad_gap = 90

    object.toBeRemove = []
    object.toBeAdd = []
    # Draw Substrate
    object.substrate(dx=object.sub_size_x / 2, dy=object.sub_size_x / 2)
    object.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
    # Draw Gnd
    object.gnd = [object.line(-object.sub_size_x / 2, 0, object.sub_size_x / 2, 0, width=object.sub_size_y, name='Gnd')]
    # Draw feedline
    x_list, y_list = construct(-1300, 2500, 'x300')
    feed_cen_1, feed_tren_1 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    x_list, y_list = construct(-1300, -2500, 'x300')
    feed_cen_2, feed_tren_2 = object.Feedline(x_list=x_list, y_list=y_list, double_end_taper=False)
    object.toBeRemove += [feed_tren_1, feed_tren_2]
    object.feedline = [feed_cen_1, feed_cen_2]

    # Draw resonator
    couple_l = 200
    spacing = 20
    radius = 150
    start = [-1000,2500]
    stop = [1000,-2500]
    # total_l = 11000 # for test 011, test 011_1 to test 011_6
    total_l = 11000 # for SD_011, SD_011_withDC
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
    # print(all_command)
    x_list, y_list = construct(start_x=x1, start_y=y1, shape=all_command)
    center_line, trench = object.CPW_line(x_list, y_list, 
                    width=object.reson_width, gap=object.reson_gap, 
                    radius=radius, name='reson',
                    end=[1,1])
    object.toBeRemove += [trench]
    object.toBeAdd += [center_line]

    # Draw DC lines:
    object.DCcpw_width = 10
    object.DCcpw_gap = 2
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
        open_end = object.line(start_x=x,
                             start_y=y+object.direction*dy,
                             end_x=x,
                             end_y=y+object.direction*(dy+175),
                             width=250)
        object.toBeRemove += [tren,open_end]
        object.toBeAdd += [cen]
        for i in range(lead_number):
            print('processing lead:',i )
            x1 = x + (2 * i - lead_number + 1) / 2 * (object.open_end_size_x / lead_number)
            x2 = x + (2 * i - lead_number + 1) / 2 * 280
            y1 = y+object.direction*(dy+175)
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
            DC_lead, DC_lead_tren = object.DC_filter(x2, y2)
            DC_lead_sum = object.modeler.unite([DC_lead, taper, connect])
            object.toBeRemove += [taper_tren, DC_lead_tren, connect_tren]
            object.DCleads += [DC_lead_sum]
        return object
    # object = DC_lines(object, x= start[0]-couple_l,
    #                 y=start[1]- (spacing + object.reson_width)* np.sign(start[1]), 
    #                 dy=400, 
    #                 lead_number=lead_number)
    object.gnd = object.modeler.subtract(object.gnd, object.toBeRemove, keep_originals=False)
    object.cpw = object.modeler.unite(object.toBeAdd)
    object.add_label(2600,3000)
    object.save()


