#!/usr/bin/python
import os,sys
folder_path = os.getcwd()
if folder_path not in sys.path:
  sys.path.append(folder_path) # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import os
import time
from datetime import datetime
import pyaedt
import numpy as np
from dxf_compiler import *

class HFSS:
    def __init__(self, project_name):
        self.project_name = project_name
        self.startup()
        
        self.gnd = []
        self.cpw = []
        self.DCleads = []
        # Tunable constant
        self.sub_size_x = 8000
        self.sub_size_y = 8000
        self.sub_thickness = 275
        self.sub_name = 'silicon'
        self.metal_thickness = 80E-3
        self.metal_name = 'gold'

        self.meander_xlen = 500
        self.meander_ylen = 50
        self.meander_radius = 20

        self.feedline_width = 15
        self.feedline_gap = 9
        self.feedline_radius = 100
        self.taper_l = 240
        self.bond_pad_size = 300

        self.reson_l_short = 3000
        self.reson_l_couple = 425
        self.reson_l_open = 1200
        self.reson_couple_d = 104
        self.reson_width = self.feedline_width
        self.reson_gap = self.feedline_gap

        self.open_end_x = None
        self.open_end_y = None
        self.open_end_size_x = 200
        self.open_end_size_y = 150

        # DC filters
        self.n_finger = 20  # number of fingers
        self.w_finger = 4  # width of the fingers
        self.w_finger_tren = 2.5  # width of the finger trenches
        self.s_finger = 12  # spacing between the fingers
        self.h_finger = 140  # height of the fingers

        self.DCcpw_width = 3
        self.DCcpw_gap = 2.5

        self.DC_bond_x = 280
        self.DC_bond_y = 300
        
    def startup(self):
        self.non_graphical = False
        self.desktop = pyaedt.Desktop(non_graphical=self.non_graphical, new_desktop_session=False, close_on_exit=False,
                       student_version=False)
        self.q = pyaedt.Hfss(projectname=self.project_name)
        self.modeler = self.q.modeler
        self.unit = 'um'
        self.modeler.model_units = self.unit
        self.desktop.disable_autosave()
        
    def substrate(self, cen_x=0, cen_y=0, dx=4000, dy=4000, up_z=0, name='Si'):
        up_z = -self.metal_thickness/2
        position = [cen_x - dx, cen_y - dy, up_z]
        size = [2 * dx, 2 * dy, -self.sub_thickness]
        self.substrate = self.modeler.create_box(
            position=position, dimensions_list=size,
            name=f"{name}",
            matname=f"{self.sub_name}")
        color = (128, 128, 128)
        transparency = 0.8
        self.set_appearance(name,color,transparency)
    
    # Basic_element: Change color
    def set_appearance(self,name,color,transparency):
        obj = self.modeler[f"{name}"]
        obj.color = color
        obj.transparency = transparency

    # Basic_element: line
    def line(self, start_x, start_y, end_x, end_y, width, bottom_z=0, name=None):
        line = self.modeler.create_polyline(
            [[start_x, start_y, bottom_z], [end_x, end_y, bottom_z]],
            name=newname(name),
            matname=f"{self.metal_name}",
            xsection_type="Rectangle",
            xsection_width=f"{width}",
            xsection_height=f"{self.metal_thickness}",
        )
        return line

    # Basic_element: arc
    def arc(self, start_x, start_y, end_x, end_y, turning_x, turning_y, width, bottom_z=0, name=None):
        start_point = [start_x, start_y, bottom_z]
        end_point = [end_x, end_y, bottom_z]
        cen_x = start_x + end_x - turning_x
        cen_y = start_y + end_y - turning_y
        center_point = [end_x, end_y, bottom_z]
        dx = turning_x - cen_x
        dy = turning_y - cen_y
        mid_point = [cen_x + dx/np.sqrt(2),cen_y + dy/np.sqrt(2), bottom_z]
        line = self.modeler.create_polyline(
            [start_point,mid_point,end_point],
            segment_type='Arc',
            name=newname(name),
            matname=f"{self.metal_name}",
            xsection_type="Rectangle",
            xsection_width=f"{width}",
            xsection_height=f"{self.metal_thickness}",
        )
        return line

    # Basic_element: taper line
    def taper(self,start_x, start_y,end_x,end_y,start_width,end_width,direction='x',bottom_z=0,name=None):
        if direction =='x':
            taper = self.modeler.create_polyline([[start_x, start_y - start_width / 2, bottom_z],
                                                  [start_x, start_y + start_width / 2, bottom_z],
                                                  [end_x, end_y + end_width /2, bottom_z],
                                                  [end_x, end_y - end_width/2, bottom_z],
                                                  [start_x, start_y - start_width / 2, bottom_z]],
                                                 cover_surface=True,
                                                 xsection_orient='X',
                                                 matname=f'{self.metal_name}',
                                                 name=newname(name))
        else:
            taper = self.modeler.create_polyline([[start_x - start_width / 2, start_y, bottom_z],
                                                  [start_x + start_width / 2, start_y, bottom_z],
                                                  [end_x + end_width / 2, end_y, bottom_z],
                                                  [end_x - end_width / 2, end_y, bottom_z],
                                                  [start_x - start_width / 2, start_y, bottom_z]],
                                                 cover_surface=True,
                                                 xsection_orient='Y',
                                                 matname=f'{self.metal_name}',
                                                 name=newname(name))
        taper = self.modeler.thicken_sheet(taper, thickness=self.metal_thickness, bBothSides=True)
        return taper

    # Advance_element: curved polyline
    def Polyline(self, x_list, y_list, radius, width, bottom_z=0, name=None):
        x_last = x_list[0]
        y_last = y_list[0]
        segment = []
        for index in range(1, len(x_list)):
            x = x_list[index]
            y = y_list[index]
            if index + 1 < len(x_list):
                x_next = x_list[index + 1]
                y_next = y_list[index + 1]
                if isinstance(radius, list):
                    r = radius[index]
                else:
                    r = radius
                x1 = x - r * np.sign(x - x_last)
                y1 = y - r * np.sign(y - y_last)
                x2 = x + r * np.sign(x_next - x)
                y2 = y + r * np.sign(y_next - y)
                segment += [self.line(x_last, y_last, x1, y1,
                                      name=name,
                                      width=width,
                                      bottom_z=bottom_z)]
                segment += [self.arc(x1, y1, x2, y2, x, y,
                                     name=name,
                                     width=width,
                                     bottom_z=bottom_z)]
                x_last = x2
                y_last = y2
            else:
                segment += [self.line(x_last, y_last, x, y,
                                      name=name,
                                      width=width,
                                      bottom_z=bottom_z,)]
        polyline = self.modeler.unite(segment)
        return polyline

    # Advance_element: CPW lines
    def CPW_line(self, x_list, y_list, width, gap, radius=0.0, name=None):
        center_line = self.Polyline(x_list, y_list, radius, width, name=name)
        trench = self.Polyline(x_list, y_list, radius, width + gap * 2, name=name+'_trench')
        return center_line,trench

    # Advance_element: taper CPW lines
    def CPW_taper(self, x_list, y_list, width_list, gap_list, direction='x', name='taper'):
        center_line = self.taper(x_list[0], y_list[0],
                                 x_list[1], y_list[1],
                                 width_list[0], width_list[1],
                                 direction=direction,
                                 name=name+'taper')
        trench = self.taper(x_list[0], y_list[0],
                                 x_list[1], y_list[1],
                                 width_list[0]+2*gap_list[0], width_list[1]+2*gap_list[1],
                                direction=direction,
                                 name=name + 'taper_trench')

        return center_line, trench

    # Advance_element: Bond pads for feedline
    def Bond_pad(self,x, y, direction='x'):
        new_gap = self.bond_pad_size / self.feedline_width * self.feedline_gap
        if direction == 'x':
            newx = x + self.taper_l * np.sign(x)
            newy = y
            self.port_end_x = newx + self.bond_pad_size * np.sign(x)
            self.port_start_x = self.port_end_x + self.bond_pad_size * np.sign(x)
            self.port_end_y = y
            self.port_start_y = y
        else:
            newx = x
            newy = y + self.taper_l * np.sign(y)
            self.port_end_y = newy + self.bond_pad_size * np.sign(y)
            self.port_start_y = self.port_end_y + self.bond_pad_size * np.sign(y)
            self.port_end_x = x
            self.port_start_x = x
        taper, taper_tren = self.CPW_taper(x_list=[x, newx],
                                             y_list=[y, newy],
                                             width_list=[self.feedline_width, self.bond_pad_size],
                                             gap_list=[self.feedline_gap, new_gap],
                                             direction=direction)
        bond, bond_tren = self.CPW_line(
            x_list=[self.port_end_x, newx],
            y_list=[self.port_end_y, newy],
            width=self.bond_pad_size,
            gap=new_gap,
            name='bond')
        bond_open = self.line(start_x=self.port_start_x, start_y=self.port_start_y,
                              end_x=self.port_end_x, end_y=self.port_end_y,
                              width=self.bond_pad_size + new_gap*2)

        center_line = self.modeler.unite([taper, bond])
        trench = self.modeler.unite([taper_tren, bond_tren, bond_open])
        self.port()
        return center_line,trench

    def port(self):
        start = [self.port_start_x, self.port_start_y, 0]
        end = [self.port_end_x, self.port_end_y, 0]
        if self.port_start_x == self.port_start_y:
            dx = self.bond_pad_size/2
            dy = 0
        else:
            dx = 0
            dy = self.bond_pad_size / 2
        p1 = [self.port_start_x - dx, self.port_start_y - dy, 0]
        p2 = [self.port_start_x + dx, self.port_start_y + dy, 0]
        p3 = [self.port_end_x + dx, self.port_end_y + dy, 0]
        p4 = [self.port_end_x - dx, self.port_end_y - dy, 0]
        name = newname('port')
        port = self.modeler.create_polyline([p1,p2,p3,p4,p1], name=name, cover_surface=True)
        self.q.create_lumped_port_to_sheet(name,
                                           axisdir=[start, end], impedance=50,
                                           portname='port')


    # Customized_element: build resonator
    def CPW_reson(self,x,y):
        start_x = -self.reson_l_couple / 2 + x
        start_y = (self.feedline_width / 2 + self.feedline_gap + self.reson_couple_d) + self.reson_gap + self.reson_width / 2 + self.reson_l_open
        ylen = self.meander_ylen
        start_y = - start_y * np.sign(y) + y
        ylen = - ylen * np.sign(y)

        if self.reson_l_couple-300 < self.meander_xlen:
            xlen_list = [self.reson_l_couple-300, self.meander_xlen]
        else:
            xlen_list = [self.meander_xlen]

        self.open_end_x = start_x
        self.open_end_y = start_y
        command = f'y{self.reson_l_open * np.sign(y)},'
        command += f'x{self.reson_l_couple},'
        command += meander(self.reson_l_short, xlen_list=xlen_list, ylen=ylen)
        x_list, y_list = construct(start_x, start_y, shape=command[:-1])
        center_line, trench = self.CPW_line(x_list, y_list, width=self.reson_width, gap=self.reson_gap, radius=self.meander_radius, name='Reson')
        return center_line, trench

    # Customized_element: build feedline
    def Feedline(self, x_list, y_list):
        center_line, trench = self.CPW_line(x_list, y_list,
                                            width=self.feedline_width,
                                            gap=self.feedline_gap,
                                            radius=self.feedline_radius,
                                            name='feedline')
        cen1, tren1 = self.Bond_pad(x_list[0], y_list[0])
        cen2, tren2 = self.Bond_pad(x_list[-1], y_list[-1])
        center_line = self.modeler.unite([center_line, cen1, cen2])
        trench = self.modeler.unite([trench, tren1, tren2])
        return center_line, trench

    # Customized_element: build DC filter
    def DC_filter(self, x, y):
        cen_list = []
        tren_list = []
        for i in range(self.n_finger):
            dx = self.h_finger + self.DCcpw_width / 2
            cen = self.line(start_x=x-dx, start_y=y-i*self.s_finger*np.sign(y),
                            end_x=x+dx, end_y=y-i*self.s_finger*np.sign(y),
                            width=self.w_finger, name='finger_cap')
            tren = self.line(start_x=x-dx-self.w_finger_tren * 2, start_y=y-i*self.s_finger*np.sign(y),
                            end_x=x+dx+self.w_finger_tren * 2, end_y=y-i*self.s_finger*np.sign(y),
                            width=self.w_finger + self.w_finger_tren*2,
                             name='finger_cap_trench')
            cen_list += [cen]
            tren_list += [tren]

        # Inductor loop
        command, offset_x, offset_y, radius_list = inductor(self.DC_bond_x,
                                               self.DC_bond_y,
                                               total=7500,
                                               spacing=self.DCcpw_width+self.DCcpw_gap,
                                               direction=np.sign(y))
        x_list, y_list = construct(x+offset_x, y+offset_y, command)
        cen, tren = self.CPW_line(x_list=x_list, y_list=y_list,
                                  width=self.DCcpw_width,
                                  gap=self.DCcpw_gap,
                                  radius=radius_list,
                                  name='Inductor')
        cen_list += [cen]
        tren_list += [tren]

        # bond_pad
        x1 = x + offset_x - self.DC_bond_x / 2
        y1 = y + offset_y
        x2 = x + offset_x - self.DC_bond_x / 2
        y2 = y + offset_y + self.DC_bond_y
        spacing = self.DCcpw_width + self.DCcpw_gap
        cen = self.line(start_x=x1, start_y=y1, end_x=x2, end_y=y2,
                        width=self.DC_bond_x, name='Pads')
        tren = self.line(start_x=x1, start_y= y1-spacing, end_x=x2, end_y=y2+spacing,
                        width=self.DC_bond_x + spacing * 2, name='Pads_trench')
        cen_list += [cen]
        tren_list += [tren]

        center = self.modeler.unite(cen_list)
        trench = self.modeler.unite(tren_list)
        return center, trench

    # Modeler_sum: build_chip design
    def Build_all(self,lead_number = 0):
        self.toBeRemove = []
        self.toBeAdd = []
        # Draw Substrate
        self.substrate(dx=self.sub_size_x/2, dy=self.sub_size_x/2)
        self.modeler.create_airbox(offset=10, offset_type="Relative")
        # Draw Gnd
        self.gnd = [self.line(-self.sub_size_x/2, 0, self.sub_size_x/2, 0, width=self.sub_size_y, name='Gnd')]
        # Draw feedline
        x_list, y_list = construct(-3000, 3000, 'x6000,y-6000,x-6000')
        feed_cen, feed_tren = self.Feedline(x_list=x_list, y_list=y_list)
        self.toBeRemove += [feed_tren]
        self.feedline = [feed_cen]
        # Draw resonator
        def draw_reson(lshort,x,y):
            self.reson_l_short = lshort
            cen, tren = self.CPW_reson(x=x, y=y)
            open_end_edge = self.open_end_y - self.open_end_size_y * np.sign(self.open_end_y)
            open_end = self.line(start_x=self.open_end_x,
                                 start_y=self.open_end_y,
                                 end_x=self.open_end_x,
                                 end_y=open_end_edge,
                                 width=self.open_end_size_x)
            self.toBeRemove += [tren, open_end]
            self.toBeAdd += [cen]
            for i in range(lead_number):
                x1 = self.open_end_x + (2*i-lead_number+1)/2*(self.open_end_size_x/lead_number)
                x2 = self.open_end_x + (2*i-lead_number+1)/2* 280
                y1 = open_end_edge
                if i % 2 == 0:
                    y2 = open_end_edge - np.sign(self.open_end_y)*200
                else:
                    y2 = open_end_edge - np.sign(self.open_end_y)*850
                ym = y1 - np.sign(self.open_end_y)*(lead_number/2 + 1 -abs(i-lead_number/2))*20
                ym1 = ym - np.sign(self.open_end_y) * 40
                connect, connect_tren = self.CPW_line(x_list=[x1,x1,x2,x2],
                                                     y_list=[y1,ym,ym,ym1],
                                                     width=5,
                                                     gap=3,
                                                     radius=15,
                                                     name='connect'
                                                )
                taper, taper_tren = self.CPW_taper(x_list=[x2,x2],
                                                  y_list=[ym1,y2],
                                                  width_list=[5, self.DCcpw_width],
                                                  gap_list=[3, self.DCcpw_gap],
                                                  direction='y')
                DC_lead, DC_lead_tren = self.DC_filter(x2,y2)
                DC_lead_sum = self.modeler.unite([DC_lead, taper, connect])
                self.toBeRemove += [taper_tren, DC_lead_tren, connect_tren]
                self.DCleads += [DC_lead_sum]
                self.tempsave()



        draw_reson(lshort=2750, x=-1500, y=3000)
        draw_reson(lshort=3000, x=1500, y=3000)
        draw_reson(lshort=3250, x=-1500, y=-3000)
        draw_reson(lshort=3500, x=1500, y=-3000)
        self.gnd = self.modeler.subtract(self.gnd, self.toBeRemove, keep_originals=False)
        self.cpw = self.modeler.unite(self.toBeAdd)
        self.save()

    def Build_part(self,lead_number = 0):
        self.sub_size_x = 4000
        self.sub_size_y = 4000
        self.toBeRemove = []
        self.toBeAdd = []
        # Draw Substrate
        self.substrate(dx=self.sub_size_x / 2, dy=self.sub_size_y / 2)
        self.modeler.create_airbox(offset=10, offset_type="Relative")
        print('substrate created')
        # Draw Gnd
        self.gnd = [self.line(-self.sub_size_x / 2, 0, self.sub_size_x / 2, 0, width=self.sub_size_y, name='Gnd')]
        print('ground created')
        # Draw feedline
        x_list, y_list = construct(-1000, 1500, 'x2000')
        feed_cen, feed_tren = self.Feedline(x_list=x_list, y_list=y_list)
        print('feedline created')
        self.toBeRemove += [feed_tren]
        self.feedline = [feed_cen]

        # Draw resonator
        def draw_reson(lshort, x, y):
            self.reson_l_short = lshort
            cen, tren = self.CPW_reson(x=x, y=y)
            open_end_edge = self.open_end_y - self.open_end_size_y * np.sign(self.open_end_y)
            open_end = self.line(start_x=self.open_end_x,
                                 start_y=self.open_end_y,
                                 end_x=self.open_end_x,
                                 end_y=open_end_edge,
                                 width=self.open_end_size_x)
            self.toBeRemove += [tren, open_end]
            self.toBeAdd += [cen]

            for i in range(lead_number):
                x1 = self.open_end_x + (2 * i - lead_number + 1) / 2 * (self.open_end_size_x / lead_number)
                x2 = self.open_end_x + (2 * i - lead_number + 1) / 2 * 280
                y1 = open_end_edge
                if i % 2 == 0:
                    y2 = open_end_edge - np.sign(self.open_end_y) * 200
                else:
                    y2 = open_end_edge - np.sign(self.open_end_y) * 850
                ym = y1 - np.sign(self.open_end_y) * (lead_number / 2 + 1 - abs(i - lead_number / 2)) * 20
                ym1 = ym - np.sign(self.open_end_y) * 40
                connect, connect_tren = self.CPW_line(x_list=[x1, x1, x2, x2],
                                                      y_list=[y1, ym, ym, ym1],
                                                      width=5,
                                                      gap=3,
                                                      radius=15,
                                                      name='connect'
                                                      )
                taper, taper_tren = self.CPW_taper(x_list=[x2, x2],
                                                   y_list=[ym1, y2],
                                                   width_list=[5, self.DCcpw_width],
                                                   gap_list=[3, self.DCcpw_gap],
                                                   direction='y')
                DC_lead, DC_lead_tren = self.DC_filter(x2, y2)
                DC_lead_sum = self.modeler.unite([DC_lead, taper, connect])
                self.toBeRemove += [taper_tren, DC_lead_tren, connect_tren]
                self.DCleads += [DC_lead_sum]
                self.tempsave()

        draw_reson(lshort=3250, x=0, y=1500)
        self.gnd = self.modeler.subtract(self.gnd, self.toBeRemove, keep_originals=False)
        self.cpw = self.modeler.unite(self.toBeAdd)
        self.save()

    def save(self):
        self.q.save_project()
        self.desktop.enable_autosave()

    def tempsave(self):
        self.q.save_project()


def construct(start_x, start_y, shape=''):
    command = shape.split(',')
    x_list = [start_x]
    y_list = [start_y]
    for each in command:
        select = each[0]
        len = float(each[1:])
        if select == 'x':
            start_x += len
        if select == 'y':
            start_y += len
        x_list += [start_x]
        y_list += [start_y]
    return x_list, y_list

def meander(total,xlen_list,ylen):
    command = ''
    remain = total
    flag = True
    def draw(flag,remain,command,tag,sign):
        if tag =='x':
            delta = xlen
        else:
            delta = ylen
        if flag:
            remain -= delta
            if remain > 0:
                command += f'{tag}{delta*sign},'
            else:
                command += f'{tag}{(remain+delta)*sign},'
                flag = False
        return flag,remain,command
    if len(xlen_list)>1:
        xlen = xlen_list[0]
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=-1)
        xlen = xlen_list[1]
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=1)
    else:
        xlen = xlen_list[0]
    while flag:
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=-1)
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=1)
    return command

def inductor(xpad,ypad,spacing,total,direction=1):
    global dx, dy, flag, remain, command, radius
    d = {}
    d.update({'x': 0})
    d.update({'y': 0})
    d.update({'r': []})
    radius = 0
    d['r'] += [radius]
    command = ''
    remain = total
    flag = True
    def draw(xpad , ypad, tag, sign):
        global dx, dy, flag, remain, command, radius
        if flag:
            if tag == 'x':
                xpad = xpad + spacing
                delta = xpad
            else:
                ypad = ypad + spacing
                delta = ypad
            remain -= delta
            if tag == 'y' and sign == 1:
                radius += spacing
            if remain < 500 and tag =='x' and sign == -direction:
                command += f'{tag}{(delta/2) * sign},'
                d[tag] += (delta/2) * sign
                d['r'] += [spacing]
                flag = False
            else:
                command += f'{tag}{delta * sign},'
                d[tag] += delta * sign
                d['r'] += [radius]

        return xpad, ypad
    while flag:
        xpad, ypad = draw(xpad, ypad, tag='y', sign=1)
        xpad, ypad = draw(xpad, ypad, tag='x', sign=-1)
        xpad, ypad = draw(xpad, ypad, tag='y', sign=-1)
        xpad, ypad = draw(xpad, ypad, tag='x', sign=1)
    command += f'y{direction*250}'
    d['y'] += direction * 250
    return command, -d['x'], -d['y'], d['r']

global counter
counter = 0
def newname(name):
    global counter
    if name is None:
        name =''
    name = name+f'_{counter}'
    counter += 1
    return name




