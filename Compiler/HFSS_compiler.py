#!/usr/bin/python
import os, sys

folder_path = os.getcwd()
if folder_path not in sys.path:
    sys.path.append(
        folder_path)  # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import os
import time
from datetime import datetime
import pyaedt
import numpy as np
from Builds.Build_universal_functions import *

class HFSS:
    def __init__(self, project_name):
        self.compiler = 'hfss'
        self.project_name = project_name
        self.startup()

        self.gnd = []
        self.cpw = []
        self.DCleads = []
        self.DCleads_position = []
        # Tunable constant
        self.sub_size_x = 8000
        self.sub_size_y = 8000
        self.sub_thickness = 275
        self.sub_name = 'silicon'
        self.metal_thickness = 80E-3
        self.metal_name = 'perfect conductor'

        self.meander_xlen = 600
        self.meander_ylen = 120
        self.meander_radius = 60

        self.feedline_width = 15
        self.feedline_gap = 9
        self.feedline_radius = 100
        self.openendTogap_ratio = 10

        self.bond_pad_width = 300
        self.taper_l = self.bond_pad_width / 3 * 2
        self.bond_pad_l = self.bond_pad_width
        self.bond_pad_gap = self.bond_pad_width / self.feedline_width * self.feedline_gap

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
        self.n_finger = 12  # number of fingers
        self.w_finger = 4  # width of the fingers
        self.w_finger_tren = 2.5  # width of the finger trenches
        self.s_finger = 12  # spacing between the fingers
        self.h_finger = 140  # height of the fingers
        self.filter_in_len = 7500

        self.DCcpw_width = 3
        self.DCcpw_gap = 2.5
        self.DCconnect_width = 5
        self.DCconnect_gap = 3
        self.DCconnect_radius = 15

        self.DC_bond_x = 280
        self.DC_bond_y = 300
        self.direction = -1

        self.meshgrid = min(self.feedline_gap, self.reson_gap)

    def startup(self):
        self.non_graphical = False
        self.desktop = pyaedt.Desktop(non_graphical=self.non_graphical, new_desktop=False, close_on_exit=False,
                                      student_version=False)
        self.q = pyaedt.Hfss(projectname=self.project_name)
        self.modeler = self.q.modeler
        self.unit = 'um'
        self.modeler.model_units = self.unit
        self.desktop.disable_autosave()

    def substrate(self, cen_x=0, cen_y=0, dx=4000, dy=4000, up_z=0, name='Substrate'):
        up_z = -self.metal_thickness / 2
        position = [cen_x - dx, cen_y - dy, up_z]
        size = [2 * dx, 2 * dy, -self.sub_thickness]
        self.substrate = self.modeler.create_box(
            position=position, dimensions_list=size,
            name=f"{name}",
            matname=f"{self.sub_name}")

    # Basic_element: Change color
    def set_appearance(self, name, color, transparency):
        if isinstance(name, list):
            for each in name:
                obj = self.modeler[f"{each}"]
                obj.color = color
                obj.transparency = transparency
        else:
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
        mid_point = [cen_x + dx / np.sqrt(2), cen_y + dy / np.sqrt(2), bottom_z]
        line = self.modeler.create_polyline(
            [start_point, mid_point, end_point],
            segment_type='Arc',
            name=newname(name),
            matname=f"{self.metal_name}",
            xsection_type="Rectangle",
            xsection_width=f"{width}",
            xsection_height=f"{self.metal_thickness}",
        )
        return line

    # Basic_element: taper line
    def taper(self, start_x, start_y, end_x, end_y, start_width, end_width, direction='x', bottom_z=0, name=None):
        if direction == 'x':
            taper = self.modeler.create_polyline([[start_x, start_y - start_width / 2, bottom_z],
                                                  [start_x, start_y + start_width / 2, bottom_z],
                                                  [end_x, end_y + end_width / 2, bottom_z],
                                                  [end_x, end_y - end_width / 2, bottom_z],
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
                                      bottom_z=bottom_z, )]
        polyline = self.modeler.unite(segment)
        return polyline

    # Advance_element: CPW lines
    def CPW_line(self, x_list, y_list, width, gap, radius=0.0, name=None, end=[0,0]):
        center_line = self.Polyline(x_list, y_list, radius, width, name=name)
        x_list[0] = x_list[0] - gap*self.openendTogap_ratio*np.sign(x_list[1]-x_list[0])*end[0]
        y_list[0] = y_list[0] - gap*self.openendTogap_ratio*np.sign(y_list[1]-y_list[0])*end[0]
        x_list[-1] = x_list[-1] + gap*self.openendTogap_ratio*np.sign(x_list[-1]-x_list[-2])*end[1]
        y_list[-1] = y_list[-1] + gap*self.openendTogap_ratio*np.sign(y_list[-1]-y_list[-2])*end[1]
        trench = self.Polyline(x_list, y_list, radius, width + gap * 2, name=name + '_trench')
        return center_line, trench

    # Advance_element: taper CPW lines
    def CPW_taper(self, x_list, y_list, width_list, gap_list, direction='x', name='taper'):
        center_line = self.taper(x_list[0], y_list[0],
                                 x_list[1], y_list[1],
                                 width_list[0], width_list[1],
                                 direction=direction,
                                 name=name + 'taper')
        trench = self.taper(x_list[0], y_list[0],
                            x_list[1], y_list[1],
                            width_list[0] + 2 * gap_list[0], width_list[1] + 2 * gap_list[1],
                            direction=direction,
                            name=name + 'taper_trench')

        return center_line, trench

    # Advance_element: Bond pads for feedline
    def Bond_pad(self, x, y, direction='x'):
        new_gap = self.bond_pad_gap
        if direction == 'x':
            newx = x + self.taper_l * np.sign(x)
            newy = y
            self.port_end_x = newx + self.bond_pad_l * np.sign(x)
            self.port_start_x = self.port_end_x + new_gap * np.sign(x)
            self.port_end_y = y
            self.port_start_y = y
        else:
            newx = x
            newy = y + self.taper_l * np.sign(y)
            self.port_end_y = newy + self.bond_pad_l * np.sign(y)
            self.port_start_y = self.port_end_y + new_gap * np.sign(y)
            self.port_end_x = x
            self.port_start_x = x
        taper, taper_tren = self.CPW_taper(x_list=[x, newx],
                                           y_list=[y, newy],
                                           width_list=[self.feedline_width, self.bond_pad_width],
                                           gap_list=[self.feedline_gap, new_gap],
                                           direction=direction)
        bond, bond_tren = self.CPW_line(
            x_list=[self.port_end_x, newx],
            y_list=[self.port_end_y, newy],
            width=self.bond_pad_width,
            gap=new_gap,
            name='bond')
        bond_open = self.line(start_x=self.port_start_x, start_y=self.port_start_y,
                              end_x=self.port_end_x, end_y=self.port_end_y,
                              width=self.bond_pad_width + new_gap * 2)

        center_line = self.modeler.unite([taper, bond])
        trench = self.modeler.unite([taper_tren, bond_tren, bond_open])
        self.port()
        return center_line, trench

    def port(self):
        start = [self.port_start_x, self.port_start_y, 0]
        end = [self.port_end_x, self.port_end_y, 0]
        if self.port_start_x == self.port_start_y:
            dx = self.bond_pad_width / 2
            dy = 0
        else:
            dx = 0
            dy = self.bond_pad_width / 2
        p1 = [self.port_start_x - dx, self.port_start_y - dy, 0]
        p2 = [self.port_start_x + dx, self.port_start_y + dy, 0]
        p3 = [self.port_end_x + dx, self.port_end_y + dy, 0]
        p4 = [self.port_end_x - dx, self.port_end_y - dy, 0]
        name = newname('port')
        port = self.modeler.create_polyline([p1, p2, p3, p4, p1], name=name, cover_surface=True)
        self.q.create_lumped_port_to_sheet(name,
                                           axisdir=[start, end], impedance=50,
                                           portname='port')

    # Customized_element: build resonator
    def CPW_reson(self, x, y):
        start_x = -self.reson_l_couple / 2 + x
        start_y = (self.feedline_width / 2 + self.feedline_gap + self.reson_couple_d) + self.reson_gap + self.reson_width / 2 + self.reson_l_open
        start_y = start_y * self.direction + y

        if self.reson_l_couple - 300 < self.meander_xlen:
            xlen_list = [self.reson_l_couple - 300, self.meander_xlen]
        else:
            xlen_list = [self.meander_xlen, self.meander_xlen]

        if self.meander_ylen < 100:
            ylen_list = [self.direction * 100, self.direction * self.meander_ylen]
        else:
            ylen_list = [self.direction * self.meander_ylen, self.direction * self.meander_ylen]

        self.open_end_x = start_x
        self.open_end_y = start_y
        command = f'y{self.reson_l_open * (-self.direction)},'
        command += f'x{self.reson_l_couple},'
        command += meander(self.reson_l_short, xlen_list=xlen_list, ylen_list=ylen_list, radius = self.meander_radius)
        x_list, y_list = construct(start_x, start_y, shape=command[:-1])
        center_line, trench = self.CPW_line(x_list, y_list, width=self.reson_width, gap=self.reson_gap,
                                            radius=self.meander_radius, name='Reson')
        return center_line, trench

    # Customized_element: build feedline
    def Feedline(self, x_list, y_list, double_end_taper=True):
        center_line, trench = self.CPW_line(x_list, y_list,
                                            width=self.feedline_width,
                                            gap=self.feedline_gap,
                                            radius=self.feedline_radius,
                                            name='feedline')
        cen1, tren1 = self.Bond_pad(x_list[0], y_list[0])
        if double_end_taper:
            cen2, tren2 = self.Bond_pad(x_list[-1], y_list[-1])
            center_line = self.modeler.unite([center_line, cen1, cen2])
            trench = self.modeler.unite([trench, tren1, tren2])
        else:
            tren = self.Polyline(x_list=[x_list[-1],x_list[-1]+self.feedline_gap* self.openendTogap_ratio *np.sign(x_list[-1]-x_list[0])], 
                                 y_list=[y_list[-1],y_list[-1]+self.feedline_gap* self.openendTogap_ratio *np.sign(y_list[-1]-y_list[0])], 
                                 radius=self.feedline_radius, 
                                 width=self.feedline_width+self.feedline_gap*2)
            center_line = self.modeler.unite([center_line, cen1])
            trench = self.modeler.unite([trench, tren1, tren])
        return center_line, trench

    # Customized_element: build DC filter
    def DC_filter(self, x, y):
        cen_list = []
        tren_list = []
        for i in range(self.n_finger):
            dx = self.h_finger + self.DCcpw_width / 2
            cen = self.line(start_x=x - dx, start_y=y + i * self.s_finger * self.direction,
                            end_x=x + dx, end_y=y + i * self.s_finger * self.direction,
                            width=self.w_finger, name='finger_cap')
            tren = self.line(start_x=x - dx - self.w_finger_tren * 2, start_y=y + i * self.s_finger * self.direction,
                             end_x=x + dx + self.w_finger_tren * 2, end_y=y + i * self.s_finger * self.direction,
                             width=self.w_finger + self.w_finger_tren * 2,
                             name='finger_cap_trench')
            cen_list += [cen]
            tren_list += [tren]
        ym = y+ self.n_finger * self.s_finger * self.direction + 10
        cen, tren = self.CPW_line(x_list=[x,x], y_list=[y, ym],
                                  width=self.DCcpw_width,
                                  gap=self.DCcpw_gap,
                                  radius=self.DCconnect_radius,
                                  name='Finger_cap')
        cen_list += [cen]
        tren_list += [tren]
        y = ym
        # Inductor loop
        command, offset_x, offset_y, radius_list = inductor(self.DC_bond_x,
                                                            self.DC_bond_y,
                                                            total=self.filter_in_len,
                                                            spacing=self.DCcpw_width + self.DCcpw_gap,
                                                            direction=-self.direction)
        x_list, y_list = construct(x + offset_x, y + offset_y, command)
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
        self.DCleads_position += [[(x1 + x2) / 2, (y1 + y2) / 2]]
        spacing = self.DCcpw_width + self.DCcpw_gap
        cen = self.line(start_x=x1, start_y=y1, end_x=x2, end_y=y2,
                        width=self.DC_bond_x, name='Pads')
        tren = self.line(start_x=x1, start_y=y1 - spacing, end_x=x2, end_y=y2 + spacing,
                         width=self.DC_bond_x + spacing * 2, name='Pads_trench')
        cen_list += [cen]
        tren_list += [tren]

        center = self.modeler.unite(cen_list)
        trench = self.modeler.unite(tren_list)
        return center, trench
    
    def single_filter(self,x_list,y_list):
        cen_list = []
        tren_list = []
        connect, connect_tren = self.CPW_line(x_list=x_list[:-1],
                                                  y_list=y_list[:-1],
                                                  width=self.DCconnect_width,
                                                  gap=self.DCconnect_gap,
                                                  radius=self.DCconnect_radius,
                                                  name='connect'
                                                  )
        cen_list += [connect]
        tren_list += [connect_tren]

        if y_list[-2]==y_list[-1]:
            direction = 'x'
        else:
            direction = 'y'
        taper, taper_tren = self.CPW_taper(x_list=x_list[-2:],
                                            y_list=y_list[-2:],
                                            width_list=[self.DCconnect_width, self.DCcpw_width],
                                            gap_list=[self.DCconnect_gap, self.DCcpw_gap],
                                            direction=direction)
        cen_list += [taper]
        tren_list += [taper_tren]

        DC_lead, DC_lead_tren = self.DC_filter(x_list[-1], y_list[-1])
        cen_list += [DC_lead]
        tren_list += [DC_lead_tren]

        center = self.modeler.unite(cen_list)
        trench = self.modeler.unite(tren_list)
        return  center, trench
    
    def add_wirebonds(self, start, stop):
        self.modeler.create_bondwire(start_position=[start[0], start[1], self.sub_thickness/2],
                                         end_position=[stop[0], stop[1], self.sub_thickness/2],
                                         matname=self.metal_name)
        
    def FakeWirebonds(self):
        index = 0
        x0 = -self.sub_size_x / 2
        y0 = -self.sub_size_y / 2
        d = 500
        d1 = 200
        d2 = 300
        empty = []
        for position in self.DCleads_position:
            index += 1
            x = position[0]
            y = position[1]
            x_start = x0 + d * index
            y_start = y0 + d
            self.line(x_start - d1 / 2, y_start, x_start + d1 / 2, y_start, width=d1)
            empty += [self.line(x_start - d2 / 2, y_start, x_start + d2 / 2, y_start, width=d2)]
            self.modeler.create_polyline([[x_start - d1 / 2, y_start - d2 / 2, 0],
                                          [x_start - d1 / 2, y_start - d1 / 2, 0],
                                          [x_start + d1 / 2, y_start - d1 / 2, 0],
                                          [x_start + d1 / 2, y_start - d2 / 2, 0],
                                          [x_start - d1 / 2, y_start - d2 / 2, 0]],
                                         name=f'DC_{index}',
                                         cover_surface=True)
            self.add_wirebonds([x_start, y_start],[x,y])
            self.q.assign_voltage_source_to_sheet(sheet_name=f'DC_{index}',
                                                  axisdir=[[x_start, y_start - d2 / 2, 0],
                                                           [x_start, y_start - d1 / 2, 0]])
        self.modeler.subtract([self.modeler['Gnd_0']], empty, keep_originals=False)

    def build_region(self,dx,dy,cen_x=0,cen_y=0):
        '''Huge air box'''
        # self.modeler.create_air_region(x_pos=10, y_pos=10, z_pos=500, x_neg=10, y_neg=10, z_neg=10, is_percentage=True)
        '''Finite air box->vacuum'''
        # self.modeler.create_air_region(x_pos=0, y_pos=0, z_pos=500, x_neg=0, y_neg=0, z_neg=0, is_percentage=True)
        # region = self.modeler["Region"]
        # region.material_name = 'vacuum'
        '''Handmade vacuum box'''
        up_z = self.metal_thickness / 2 - 2*self.sub_thickness 
        position = [cen_x - dx, cen_y - dy, up_z]
        size = [2 * dx, 2 * dy, 5*self.sub_thickness]
        self.modeler.create_box(
            position=position, dimensions_list=size,
            name=f"Region",
            matname=f"vacuum")
        color = (128, 128, 128)
        transparency = 0.1
        self.set_appearance('Region', color, transparency)
    
    def thickness0(self):
        if self.metal_thickness == 0:
            list = []
            list += self.modeler.get_objects_w_string('gnd',case_sensitive=False)
            list += self.modeler.get_objects_w_string('feedline',case_sensitive=False)
            list += self.modeler.get_objects_w_string('reson',case_sensitive=False)
            list += self.modeler.get_objects_w_string('finger_cap',case_sensitive=False)
            list += self.modeler.get_objects_w_string('inductor',case_sensitive=False)
            self.q.assign_perfecte_to_sheets(list)

    def create_mesh(self):
        unit = self.meshgrid
        mesh = self.q.mesh.assign_length_mesh(self.modeler.get_objects_w_string('feedline',case_sensitive=False),
                                              isinside=False, maxlength=unit, maxel=None, meshop_name='feedline_mesh')
        mesh = self.q.mesh.assign_length_mesh(self.modeler.get_objects_w_string('reson',case_sensitive=False),
                                              isinside=False, maxlength=unit, maxel=None, meshop_name='reson_mesh')
        mesh = self.q.mesh.assign_length_mesh(self.modeler.get_objects_w_string('finger_cap',case_sensitive=False),
                                              isinside=False, maxlength=unit, maxel=None, meshop_name='finger_cap_mesh')
        mesh = self.q.mesh.assign_length_mesh(self.modeler.get_objects_w_string('inductor',case_sensitive=False),
                                              isinside=False, maxlength=unit, maxel=None, meshop_name='inductor_mesh')
    def beauty(self):
        region_list = self.modeler.get_objects_w_string('region',case_sensitive=False)
        self.set_appearance(name=region_list,color=(200,200,200),transparency=0.9)
        gnd_list = self.modeler.get_objects_w_string('gnd',case_sensitive=False)
        self.set_appearance(name=gnd_list,color=(0,127,255),transparency=0)
        feedline_list = self.modeler.get_objects_w_string('feedline',case_sensitive=False)
        self.set_appearance(name=feedline_list,color=(0,255,0),transparency=0)
        reson_list = self.modeler.get_objects_w_string('reson',case_sensitive=False)
        self.set_appearance(name=reson_list,color=(255,0,0),transparency=0)
        dc_list = self.modeler.get_objects_w_string('finger_cap',case_sensitive=False) 
        dc_list += self.modeler.get_objects_w_string('inductor',case_sensitive=False)
        self.set_appearance(name=dc_list,color=(128,0,128),transparency=0)

    def save(self):
        # self.FakeWirebonds()
        self.thickness0()
        self.create_mesh()
        self.beauty()
        self.q.save_project()
        self.desktop.enable_autosave()

    def tempsave(self):
        self.q.save_project()
    
    def add_label(self,*args):
        pass


global counter
counter = 0

def newname(name):
    global counter
    if name is None:
        name = ''
    name = name + f'_{counter}'
    counter += 1
    return name
