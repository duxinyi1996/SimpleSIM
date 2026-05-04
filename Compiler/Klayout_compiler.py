#!/usr/bin/python
import os, sys
from datetime import datetime as dt

folder_path = os.getcwd()
if folder_path not in sys.path:
    sys.path.append(
        folder_path)  # easier to open driver files as long as Simple_DAQ.py is in the same folder with drivers
import os, sys
import klayout.db as db
from Compiler.HFSS_compiler import *
import numpy as np


class KLAYOUT(HFSS):
    def startup(self):
        self.trap = False
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
        self.extention = '.dxf'
        self.feedline = None
        self.DCleads = None

    def set_appearance(self, name, color, transparency):
        pass

    def line(self, start_x, start_y, end_x, end_y, width, **para):
        dx = end_x - start_x
        dy = end_y - start_y
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
        if self.trap and self.gnd is not None:
            print('Adding trap')
            bbox = self.gnd.bbox()
            safe_dbu = int(safe / self.q.dbu)
            safe_region = db.Region(bbox).sized(-safe_dbu)
            real = create_trap(d, s) & safe_region & self.gnd
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

    def fillet_corners(self, item, radius):
        """
        Rounds the corners of a specified KLayout db.Region.
        
        Parameters:
        - item (db.Region or list): The KLayout region(s) to fillet.
        - radius (float): The radius of the curve in um.
        """
        # Handle lists of objects
        if isinstance(item, list):
            for obj in item:
                self.fillet_corners(obj, radius)
            return
        # Ensure the item is a KLayout Region
        if isinstance(item, db.Region):
            # 1. Convert the radius from um to Database Units (dbu)
            # self.q.dbu is 0.001 (1nm), so 5um becomes 5000 dbu
            radius_dbu = int(radius / self.q.dbu)
            # Number of points to approximate a full circle
            n_points = 64 
            # 2. Apply the rounding. 
            rounded_region = item.round_corners(radius_dbu, radius_dbu, n_points)
            # 3. OVERWRITE IN-PLACE:
            item.assign(rounded_region)
            print(f"[Info] KLAYOUT: Successfully filleted Region with radius {radius}um ({radius_dbu} dbu).")
        else:
            print(f"[Warning] KLAYOUT: Object is not a db.Region. Cannot fillet. Type: {type(item)}")

    def save(self):
        def draw(tag, items):
            layer = self.q.layer(tag)
            for item in items:
                if item is not None and not item.is_empty():
                    self.main.shapes(layer).insert(item)
            print('Drawing layer:', tag)
        self.mylist = [self.gnd,
                  self.cpw,
                  self.DCleads,
                  self.texts]
        self.taglist = ['GND', 'CPW', 'DCleads', 'Labels']
        if self.trap:
            self.add_trap()
        for i in range(0, len(self.mylist)):
            if self.mylist[i] is not None:
                draw(self.taglist[i], self.mylist[i])
        if '.' not in self.project_name:
            self.project_name += self.extention
        self.q.write(self.project_name)

    def add_wirebonds(self, start, stop):
        pass

    def tempsave(self):
        self.save()


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

    def subtract(self, originals, toBeRemove, keep_originals=False, **para):
        region1 = get_region(originals)
        region2 = get_region(toBeRemove)
        result_region = (region1 - region2).merge()
        if isinstance(originals, db.Region):
            originals.assign(result_region)
        elif isinstance(originals, list) and len(originals) > 0 and isinstance(originals[0], db.Region):
            originals[0].assign(result_region)
        if not keep_originals:
            if isinstance(toBeRemove, db.Region):
                toBeRemove.clear()
            elif isinstance(toBeRemove, list):
                for item in toBeRemove:
                    if isinstance(item, db.Region):
                        item.clear()
        return result_region


def get_region(items):
    region = db.Region()
    for item in items:
        # print(item)
        if isinstance(item, db.Region):
            region += item
        else:
            region += db.Region(item)
    return region
