import os,time
import numpy as np
import phidl
from phidl import Device
from phidl import quickplot as qp
import phidl.geometry as pg
current_path = os.path.abspath(os.path.dirname(__file__))

phidl.set_quickplot_options(show_ports=None, show_subports=None, label_aliases=None, new_window=None, blocking=True, zoom_factor=None, interactive_zoom=None)

class PHIDL():
    def __init__(self, project_name):
        self.project_name = project_name
        self.startup()
        self.modeler = MyPHIDL()
        self.die_spacing = 10e3
        self.die_size = 9e3
        self.wafer_dia = 100e3
        self.layer = 1
    def startup(self):
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
        # print(p1, p2, p3, p4)
        return line
    
    def GCAKey(self, displace = [0,0]):
        a = 16
        b = 62
        c = 21
        d = 63.5
        Square_center = self.line(-2,0,2,0,4)
        hline = self.line(a,0,b,0,2)
        hline_1 = self.line(-a,0,-b,0,2)
        hline_2 = self.line(0,a,0,b,2)
        hline_3 = self.line(0,-a,0,-b,2)
        starline = self.line(c,c,d,d,2)
        starline_1 = self.line(c,-c,d,-d,2)
        starline_2 = self.line(-c,c,-d,d,2)
        starline_3 = self.line(-c,-c,-d,-d,2)
        D = self.modeler.unite([Square_center,
                                hline,
                                hline_1,
                                hline_2,
                                hline_3, 
                                starline,
                                starline_1,
                                starline_2,
                                starline_3,
                                ])
        return D.move(displace)
    
    def Cross(self, displace = [0,0], L=500, W=3):
        hline = self.line(-L,0,L,0,W)
        vline = self.line(0,-L,0,L,W)
        D = self.modeler.unite([vline,
                                hline,
                                ])
        return D.move(displace)
    
    def Four_point_Probe(self, displace=[0,0]):
        A = Device()
        Square = pg.rectangle([300,300]).move([-150,-150])
        Square_0 = A << Square
        Square_1 = A << Square
        Square_2 = A << Square
        Square_3 = A << Square
        Square_0.move([200,200])
        Square_1.move([-200,200])
        Square_2.move([-200,-200])
        Square_3.move([200,-200])
        Square_c = self.line(-100,0,100,0,200)
        return self.modeler.unite([Square_c,Square_1,Square_2,Square_3,Square_0]).move(displace)
    
    def Four_point_Probe_JJ(self, displace=[0,0]):
        Slot = self.line(0,-300,0,300,20)
        return self.modeler.subtract(self.Four_point_Probe(),Slot).move(displace)
    
    def Contact_groove(self,displace=[0,0],rotation=0):
        # Default pointing right, (0,0) being the center at shorter edge
        small = self.line(0,0,1,0,3)
        large = self.line(1,0,2,0,5)
        D = self.modeler.unite([small,large]).rotate(rotation)
        return D.move(displace)
    
    def Manhattan_JJ(self, displace=[0,0]):
        A = Device()
        Square_0 = self.line(0,0,150,0,150).move([55/2,0])
        Square_1 = self.line(0,0,-150,0,150).move([-55/2,0])
        Bridge_0 = self.line(-75,0,75,0,40)
        Cut_0 = self.line(0,-10,0,20,25)
        Cut_1 = self.line(0,-10,0,-20,7.5).move([7.5/2-55/2+15,0])
        A = self.modeler.subtract([Square_0,Square_1,Bridge_0],
                                  [Cut_0,Cut_1,
                                   self.Contact_groove([25/2,-5/2],0),
                                   self.Contact_groove([-25/2,-5/2],180),
                                   self.Contact_groove([0,-10],270),
                                   ])
        return A.move(displace)

    def Die(self,displace = [0,0]):
        Die = pg.basic_die(
              size = (self.die_size, self.die_size), # Size of die
              street_width = 300,   # Width of corner marks for die-sawing
              street_length = 3000, # Length of corner marks for die-sawing
              die_name = 'Witness',
              text_size = 500,
              text_location = 'NW',
              layer = 1,
              draw_bbox = False,
              bbox_layer = 99,
              )
        Dose_1 = pg.litho_steps(
            line_widths=[0.25,0.5,1,2,4,8,16,32,64],
            line_spacing= 50,
            height= 1000,
            layer= 1,
        ).move([3e3,3e3])
        A = Device()
        Dose_2 = A<<Dose_1
        Dose_2.move([-6e3,-5e3])
        GCA_1 = A<<self.GCAKey([-3250,0])
        GCA_2 = A<<self.GCAKey([3250,0])
        Mark_1 = A<<self.Cross([-3250,1000])
        Mark_2 = A<<self.Cross([3250,1000])
        D = [Die,Dose_1,Dose_2,GCA_1,GCA_2,Mark_1,Mark_2]

        FourPP = self.Four_point_Probe()
        MJJ = self.Manhattan_JJ()
        for y in np.linspace(-2e3,2e3,5):
            new_FourPP = A<<FourPP
            D += [new_FourPP.move([2e3,y])]
            # D += [A<<self.Four_point_Probe([2e3,y])] #SLOW
        for x in np.linspace(-2e3,1e3,7):
            for y in np.linspace(-2e3,2e3,11):
                new_MJJ = A<<MJJ
                D += [new_MJJ.move([x,y])]
                # D += [A<<self.Manhattan_JJ([x,y])] #SLOW
        spacing =100
        width = 4e3
        ruler = pg.litho_ruler(
            height = 500,
            width = 50,
            spacing = spacing,
            scale = [2,1,1,1,1,1.5,1,1,1,1],
            num_marks= int(width/spacing)+1,
            layer = 1,
        ).move([-width/2,0])
        D += [A<<ruler.move([0,2.5e3])]
        D = self.modeler.unite(D)
        return D.move(displace)
    
    def Chip_No(self, displace = [0,0]):
        D = pg.text(f"({displace[0]/1e3/5:0.0f},{displace[1]/1e3/5:0.0f})",layer=1,size=300).move([2.5e3,-2e3])
        return D.move(displace)
    
    def Die_array(self):
        A = Device()
        Die_array = []
        a = self.wafer_dia/2-self.die_spacing/2
        die = self.Die()
        for x in np.linspace(-a,a,10):
            for y in np.linspace(-a,a,10):
                if x**2+y**2<(self.wafer_dia/2)**2:
                    new_die = A<<die
                    Die_array += [new_die.move([x,y])]
                    Die_array += [A<<self.Chip_No([x,y])]
        Die_array = self.modeler.unite(Die_array)
        ### CellArray: fast but not sure how to output
        # A = Device()
        # Die_array = A.add_array(self.Die(),columns=10,rows=10,spacing=[self.die_spacing,self.die_spacing])
        # Die_array = Die_array.move([-self.die_spacing/2*10,-self.die_spacing/2*10])
        return Die_array
    
    def Uniformity(self):
        spacing = 100
        ruler_h = pg.litho_ruler(
            height = 100,
            width = 20,
            spacing = spacing,
            scale = [20,1,1,1,1,10,1,1,1,1],
            num_marks= int(self.wafer_dia/spacing+1),
            layer = 1,
        ).move([-self.wafer_dia/2,0])
        ruler_v = pg.litho_ruler(
            height = 100,
            width = 20,
            spacing = spacing,
            scale = [3,1,1,1,1,2,1,1,1,1],
            num_marks= int(self.wafer_dia/spacing+1),
            layer = 1,
        ).move([-self.wafer_dia/2,0])
        ruler_v.rotate(90)
        D = [ruler_h, ruler_v]
        A = Device()
        for x in np.linspace(-self.wafer_dia/2,self.wafer_dia/2,51):
            D += [pg.text(f"{x/1e3:0.0f} mm",layer=1,size=100).move([x,2000])]
            D += [pg.text(f"{x/1e3:0.0f} mm",layer=1,size=100).move([x,-200])]
            D += [A<<pg.rectangle([300,800]).move([x,1000])]
        for y in np.linspace(-self.wafer_dia/2,self.wafer_dia/2,51):
            D += [pg.text(f"{y/1e3:0.0f}",layer=1,size=100).move([-400,y-120])]
        return self.modeler.unite(D)
    
    def EdgeWindow(self):
        window = pg.rectangle([40e3,1.75e3]).move([-20e3,-1.75e3/2])
        y = -47.3e3 #np.sqrt(50**2-(37.5/2)**2)
        left = pg.text("FLAT->",layer=1,size=2000,justify = 'right').move([-20e3,-2000/2])
        right = pg.text("<-FLAT",layer=1,size=2000,justify = 'left').move([20e3,-2000/2])
        return self.modeler.unite([window,left,right]).move([0,y])


class MyPHIDL:
    def create_box(self, **para):
        pass

    def create_polyline(self, position_list, **para):
        D = Device()
        xpts = []
        ypts = []
        for position in position_list:
            xpts += [position[0]]
            ypts += [position[1]]
        D = D.add_polygon([xpts,ypts], layer=1)
        return D

    def create_airbox(self, **para):
        pass
    def create_air_region(self, **para):
        pass
    def thicken_sheet(self, **para):
        pass

    def unite(self, items, **para):
        
        if isinstance(items, list):
            D = items[0]
            if len(items)>1:
                for i in range(1,len(items)):
                    D = pg.boolean(A=D,B=items[i], operation= 'or', layer = 1)
            else:
                pass
        else:
            D = items
        return D

    def subtract(self, originals, toBeRemove, **para):
        region1 = self.unite(originals)
        region2 = self.unite(toBeRemove)
        D =  pg.boolean(A=region1,B=region2, operation= 'not', layer = 1)
        return D

    
# GCA_key = pg.import_gds(filename=os.path.join(current_path,'GDS_Lib','GCA_KEY.GDS'), cellname=None, flatten= True)
h = PHIDL('test')
now= time.time()
# qp([h.Die_array(),h.Uniformity()])
# D  = h.modeler.unite([h.Die_array(),h.Uniformity()])
D = h.modeler.subtract(h.Die_array(),
                       pg.rectangle([h.wafer_dia,2.1e3]).move([-h.wafer_dia/2,0])) # Remove the overlap regions
D = h.modeler.unite([D,
                     h.Uniformity(),
                     h.EdgeWindow(),
                     pg.text("CNF Witness 5in Mask",layer=1,size=5000,justify = 'center').move([0,51e3]),
                     h.Cross([40e3,10e3]),
                     h.Cross([-40e3,10e3]),
                     ])
D.write_gds(os.path.join(current_path,"07102025XD255L1.gds"))
print(time.time()-now)
