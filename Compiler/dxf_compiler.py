#!/usr/bin/python
import os, sys
from datetime import datetime as dt

folder_path = os.getcwd()
if folder_path not in sys.path:
    sys.path.append(
        folder_path)  # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import os, sys
import pya as db
from Compiler.HFSS_compiler import *
import numpy as np


class DXF(HFSS):
    def startup(self):
        self.trap = True
        self.label = True
        self.q = db.Layout()
        self.unit = 1E-6    # data were in 1um unit
        self.q.dbu = 1E-9/self.unit     # sets the database precision 1nm,
        self.dxf_unit = 1E-3    # dxf ratio
        self.modeler = Myklayout()
        self.main = self.q.create_cell("Main")
        self.t = db.DCplxTrans(1/self.q.dbu)
        self.t_dxf = db.DCplxTrans(self.dxf_unit / self.unit)
        self.texts = []
        self.compiler = 'dxf'
        self.feedline = None
        self.DCleads = None

    def set_appearance(self, name, color, transparency):
        pass

    def line(self, start_x, start_y, end_x, end_y, width, **para):
        dx = end_x - start_x
        dy = start_y - end_y
        theta = np.arctan2(dy, dx)
        newdx = width / 2 * np.sin(theta)
        newdy = width / 2 * np.cos(theta)
        p1 = [start_x - newdx, start_y + newdy]
        p2 = [start_x + newdx, start_y - newdy]
        p3 = [end_x + newdx, end_y - newdy]
        p4 = [end_x - newdx, end_y + newdy]
        line = self.modeler.create_polyline([p1, p2, p3, p4])
        # print('line')
        return line.transformed_cplx(self.t)

    def arc(self, start_x, start_y, end_x, end_y, turning_x, turning_y, width, **para):
        point_number = 90
        start_point = np.array([start_x, start_y])
        end_point = np.array([end_x, end_y])
        cen_x = start_x + end_x - turning_x
        cen_y = start_y + end_y - turning_y
        center_point = np.array([cen_x, cen_y])
        d_start = start_point - center_point
        d_end = end_point - center_point
        r_start = np.sqrt(np.sum(d_start ** 2))
        r_end = np.sqrt(np.sum(d_end ** 2))
        rad_start = np.arctan2(d_start[1], d_start[0])
        rad_end = np.arctan2(d_end[1], d_end[0])
        if abs(rad_start - rad_end) > np.pi:
            temp = [rad_start, rad_end]
            temp.sort()
            temp[0] += 2 * np.pi
            if rad_start in temp:
                rad_end = temp[0]
            else:
                rad_start = temp[0]
        rad_list = np.linspace(rad_start, rad_end, point_number)
        r_list = np.linspace(abs(r_start), abs(r_end), point_number)
        x1 = center_point[0] + (r_list - width / 2) * np.cos(rad_list)
        y1 = center_point[1] + (r_list - width / 2) * np.sin(rad_list)
        x2 = center_point[0] + (r_list + width / 2) * np.cos(rad_list)
        y2 = center_point[1] + (r_list + width / 2) * np.sin(rad_list)
        points = np.concatenate((np.column_stack([x1, y1]),
                                 np.column_stack([np.flip(x2), np.flip(y2)])),
                                axis=0)
        arc = self.modeler.create_polyline(points)
        # print('arc')
        return arc.transformed_cplx(self.t)

    def taper(self, start_x, start_y, end_x, end_y, start_width, end_width, direction='x', bottom_z=0, name=None):
        if direction == 'x':
            taper = self.modeler.create_polyline([[start_x, start_y - start_width / 2, bottom_z],
                                                  [start_x, start_y + start_width / 2, bottom_z],
                                                  [end_x, end_y + end_width / 2, bottom_z],
                                                  [end_x, end_y - end_width / 2, bottom_z]])
        else:
            taper = self.modeler.create_polyline([[start_x - start_width / 2, start_y, bottom_z],
                                                  [start_x + start_width / 2, start_y, bottom_z],
                                                  [end_x + end_width / 2, end_y, bottom_z],
                                                  [end_x - end_width / 2, end_y, bottom_z]])
        # print('taper')
        return taper.transformed_cplx(self.t)

    def port(self):
        pass

    def add_trap(self,x=0,y=0):
        def create_trap(d,s):
            region = db.Region()
            for i in range(int(-self.sub_size_x/2/d),int(self.sub_size_x/2/d)):
                for j in range(int(-self.sub_size_y / 2 / d), int(self.sub_size_y / 2 / d)):
                    square = self.modeler.create_polyline([[-s/2, -s/2],
                                                           [-s/2, s/2],
                                                           [s/2, s/2],
                                                           [s/2, -s/2]]).moved(i*d+x, j*d+y)
                    region += db.Region(square.transformed_cplx(self.t))
            return region
        safe = 150
        d = 10
        s = 3
        if self.trap:
            print('Adding trap')
            region1 = self.gnd[0].sized(-safe/self.q.dbu)
            region2 = (self.gnd[1].snapped(d/self.q.dbu, d/self.q.dbu)).sized(safe/self.q.dbu)
            region = (region1 - region2).merge()
            real = create_trap(d, s) & region
            self.mylist += [real]
            self.taglist += ['Trap']

    # Customized_element: Create labels
    def add_label(self,x,y):
        today = dt.now().strftime("%Y%m%d")
        name = (self.project_name).split("\\")[-1].split("/")[-1]
        label = f'{today}' + '_' + name
        # text =  db.Text(label, x, y)
        gen_text = db.TextGenerator().default_generator()
        region = db.Region()
        region += gen_text.text(label, self.q.dbu, 100.0)
        # print('text', region)
        self.texts += [region.moved(x/self.q.dbu,y/self.q.dbu)]

    def save(self):
        def draw(tag, items):
            layer = self.q.layer(tag)
            for item in items:
                self.main.shapes(layer).insert(item)
                print('Drawing layer:',tag)
        self.outter_gnd = self.gnd[0]
        self.inner_gnd = (self.gnd[1]-self.cpw).merge()
        self.mylist = [self.outter_gnd,
                  self.feedline,
                  self.inner_gnd,
                  self.DCleads,
                  self.texts]
        self.taglist = ['GND', 'Feedline', 'Reson', 'DCleads','Labels']
        self.add_trap()
        for i in range(0, len(self.mylist)):
            if self.mylist[i] is not None:
                draw(self.taglist[i], self.mylist[i])
        if '.dxf' not in self.project_name:
            self.project_name += '.dxf'
        self.q.write(self.project_name)

    def add_wirebonds(self, start, stop):
        pass

    def tempsave(self):
        pass


class Myklayout:
    def create_box(self, **para):
        pass

    def create_polyline(self, position_list, **para):
        point_list = []
        for position in position_list:
            point = db.DPoint(float(position[0]), float(position[1]))
            point_list += [point]
        polygon = db.DPolygon(point_list)
        return polygon

    def create_airbox(self, **para):
        pass
    def create_air_region(self, **para):
        pass
    def thicken_sheet(self, **para):
        pass

    def unite(self, items, **para):
        region = get_region(items)
        return region.merge()

    def subtract(self, originals, toBeRemove, **para):
        region1 = get_region(originals)
        region2 = get_region(toBeRemove)
        return region1.merge(), region2.merge()


def get_region(items):
    region = db.Region()
    for item in items:
        # print(item)
        if isinstance(item, db.Region):
            region += item
        else:
            region += db.Region(item)
    return region
