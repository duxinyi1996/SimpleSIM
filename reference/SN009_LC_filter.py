# ----------------------------------------------
# Written by KZ to write meander lines efficiently for HFSS
#
# ----------------------------------------------
import math
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()



#
#All user defined parameters down below
#


#Define project name
oProject = oDesktop.SetActiveProject("Project14")
#Define HFSS design name
oDesign = oProject.SetActiveDesign("HFSSDesign1")
#Define modeler name
oEditor = oDesign.SetActiveEditor("3D Modeler")

#Center locations of x and y
x_center = 0
y_center = 0
#Define orientation -- which direction does the connection point to
orientation = "x"


#chip size in um
chip_x = 1000
chip_y = 1000

#number of fingers
n_f = 20
#width of the fingers in um
w_f = 4
#width of the finger trenches in um
w_ft = 2.5
#spacing between the fingers in um
s_f = 12
#height of the fingers
h_f = 283
#length of the center pin in um
l_cpw = 285.35
#width of the cpw in um
w_cpw = 3
#trench for the cpw in um
t_cpw = 2.5
#feed length in um
feed = 50
#pad trench dimensions
x_t_pad = 460
x_pad = 400
y_t_pad = 410
y_pad = 350
dx_pad = (x_t_pad - x_pad)/2






#drawing functions
def drawRec(x, y, width, height, name):
	oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, str(x) + "um",
			"YStart:="		, str(y) + "um",
			"ZStart:="		, "0mm",
			"Width:="		, str(width) + "um",
			"Height:="		, str(height) + "um",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, name,
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		]
	)
def drawCircle(x, y, r, name):
	oEditor.CreateCircle(
		[
			"NAME:CircleParameters",
			"IsCovered:="		, True,
			"XCenter:="		, str(x) + "um",
			"YCenter:="		, str(y) + "um",
			"ZCenter:="		, "0mm",
			"Radius:="		, str(r) + "um",
			"WhichAxis:="		, "Z",
			"NumSegments:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, name,
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])


def drawCurvedCPW(w, g, x, y, r_min, deg_start, deg_end, name):
	rad_start = deg_start/180*math.pi
	rad_end = deg_end/180*math.pi
	x0 = x - r_min*math.cos(rad_start)
	y0 = y - r_min*math.sin(rad_start)
	
	#unit parameters, depending on whether r_min = 0, we might have 3 or 4 names for trenchUnite
	trenchUnite =  name + "trenchStart," + name + "outerTrenchArc," + name + "trenchEnd"
	cpwUnite = name + "pinStart," + name + "innerPinArc," + name + "outerPinArc," + name + "pinEnd"
	
	#inner trench arc
	if r_min != 0:
		oEditor.CreateEquationCurve(
			[
				"NAME:EquationBasedCurveParameters",
				"XtFunction:="		, str(x0/1e6) + "+" + str(r_min/1e6) + "*cos(_t)",
				"YtFunction:="		, str(y0/1e6) + "+" + str(r_min/1e6)+ "*sin(_t)",
				"ZtFunction:="		, "0",
				"tStart:="		, str(rad_start),
				"tEnd:="		, str(rad_end),
				"NumOfPointsOnCurve:="	, "100",
				"Version:="		, 1,
				[
					"NAME:PolylineXSection",
					"XSectionType:="	, "None",
					"XSectionOrient:="	, "Auto",
					"XSectionWidth:="	, "0",
					"XSectionTopWidth:="	, "0",
					"XSectionHeight:="	, "0",
					"XSectionNumSegments:="	, "0",
					"XSectionBendType:="	, "Corner"
				]
			], 
			[
				"NAME:Attributes",
				"Name:="		, name + "innerTrenchArc",
				"Flags:="		, "",
				"Color:="		, "(143 175 143)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, "\"vacuum\"",
				"SurfaceMaterialValue:=", "\"\"",
				"SolveInside:="		, True,
				"ShellElement:="	, False,
				"ShellElementThickness:=", "0mm",
				"IsMaterialEditable:="	, True,
				"UseMaterialAppearance:=", False,
				"IsLightweight:="	, False
			])
		trenchUnite += "," + name + "innerTrenchArc"
	#outer trench arch
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x0/1e6) + "+" + str((r_min + w + 2*g)/1e6) + "*cos(_t)",
			"YtFunction:="		, str(y0/1e6) + "+" + str((r_min + w + 2*g)/1e6)+ "*sin(_t)",
			"ZtFunction:="		, "0",
			"tStart:="		, str(rad_start),
			"tEnd:="		, str(rad_end),
			"NumOfPointsOnCurve:="	, "100",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "outerTrenchArc",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	#trenchStart
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x/1e6) +"+_t*cos(" +str(rad_start) + ")",
			"YtFunction:="		, str(y/1e6) +"+_t*sin(" +str(rad_start) + ")",
			"ZtFunction:="		, "0",
			"tStart:="		, str(0),
			"tEnd:="		, str((w + 2*g)/1e6),
			"NumOfPointsOnCurve:="	, "2",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "trenchStart",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	#trenchEnd
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str((x0 + r_min*math.cos(rad_end)) /1e6) +"+_t*cos(" +str(rad_end) + ")",
			"YtFunction:="		, str((y0 + r_min*math.sin(rad_end)) /1e6) +"+_t*sin(" +str(rad_end) + ")",
			"ZtFunction:="		, "0",
			"tStart:="		, str(0),
			"tEnd:="		, str((w + 2*g)/1e6),
			"NumOfPointsOnCurve:="	, "2",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "trenchEnd",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, trenchUnite
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False
		])
	oEditor.CoverLines(
		[
			"NAME:Selections",
			"Selections:="		, name + "trenchStart",
			"NewPartsModelFlag:="	, "Model"
		])
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "gnd",
			"Tool Parts:="		, name + "trenchStart"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])
	#inner pin arc	
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x0/1e6) + "+" + str((r_min + g)/1e6) + "*cos(_t)",
			"YtFunction:="		, str(y0/1e6) + "+" + str((r_min + g)/1e6)+ "*sin(_t)",
			"ZtFunction:="		, "0",
			"tStart:="		, str(rad_start),
			"tEnd:="		, str(rad_end),
			"NumOfPointsOnCurve:="	, "100",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "innerPinArc",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	#inner trench arch
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x0/1e6) + "+" + str((r_min + w + g)/1e6) + "*cos(_t)",
			"YtFunction:="		, str(y0/1e6) + "+" + str((r_min + w + g)/1e6)+ "*sin(_t)",
			"ZtFunction:="		, "0",
			"tStart:="		, str(rad_start),
			"tEnd:="		, str(rad_end),
			"NumOfPointsOnCurve:="	, "100",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "outerPinArc",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	#trenchStart
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x/1e6) +"+_t*cos(" +str(rad_start) + ")",
			"YtFunction:="		, str(y/1e6) +"+_t*sin(" +str(rad_start) + ")",
			"ZtFunction:="		, "0",
			"tStart:="		, str(g/1e6),
			"tEnd:="		, str((w + g)/1e6),
			"NumOfPointsOnCurve:="	, "2",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "pinStart",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	#trenchEnd
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str((x0 + r_min*math.cos(rad_end)) /1e6) +"+_t*cos(" +str(rad_end) + ")",
			"YtFunction:="		, str((y0 + r_min*math.sin(rad_end)) /1e6) +"+_t*sin(" +str(rad_end) + ")",
			"ZtFunction:="		, "0",
			"tStart:="		, str(g/1e6),
			"tEnd:="		, str((w + g)/1e6),
			"NumOfPointsOnCurve:="	, "2",
			"Version:="		, 1,
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0",
				"XSectionTopWidth:="	, "0",
				"XSectionHeight:="	, "0",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, name + "pinEnd",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, cpwUnite
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False
		])
	oEditor.CoverLines(
		[
			"NAME:Selections",
			"Selections:="		, name + "pinStart",
			"NewPartsModelFlag:="	, "Model"
		])
def drawCPW(x, y, w, g, l, orientation, name):
	if orientation == "x":
		xp = x
		yp = y + g
		width_trench = l
		width_pin = l
		height_trench = w + 2*g
		height_pin = w
	elif orientation == "y":
		xp = x + g
		yp = y
		width_trench = w + 2*g
		width_pin = w
		height_trench = l
		height_pin = l
	drawRec(x, y, width_trench, height_trench, name + "_trench")
	drawRec(xp, yp, width_pin, height_pin, name + "_pin")
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "gnd",
			"Tool Parts:="		, name + "_trench"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])
#substrate
#Ground
drawRec(-chip_x/2, -chip_y/2, chip_x, chip_y, "gnd")



#trench and fins for the fingers
finger_x = []
finger_y = []
subtract_list = "capTrench1"
unite_list = "filter"


for i in range(n_f):
    finger_x.append(i*s_f)
    finger_y.append(-h_f/2)

for i in range(n_f - 1):
	subtract_list += ",capTrench" + str(i + 2)
	
 
for i in range(n_f):
	drawRec(finger_x[i] - chip_x/2 + feed, finger_y[i], w_f + 2*w_ft, h_f + 2*w_ft, "capTrench" + str(i+1))
	drawRec(finger_x[i] - chip_x/2 + feed + w_ft, finger_y[i], w_f, h_f, "capFin" + str(i+1))
	unite_list += ",capFin" + str(i + 1)

#cpw trench and cpw
drawRec(-chip_x/2, -w_cpw/2 - t_cpw, feed + l_cpw, w_cpw + 2*t_cpw, "cpwTrench")
drawRec(-chip_x/2, -w_cpw/2, feed + l_cpw, w_cpw, "filter")
subtract_list += ",cpwTrench"


#pad trenches
drawRec(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw, -y_pad/2, x_t_pad, y_pad, "padTrenchX")
drawRec(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw + dx_pad, -y_t_pad/2, x_pad, y_t_pad, "padTrenchY")
drawCircle(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw + dx_pad, -y_pad/2, dx_pad, "pT_circle1")
drawCircle(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw + dx_pad, +y_pad/2, dx_pad, "pT_circle2")
drawCircle(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw + dx_pad + x_pad, -y_pad/2, dx_pad, "pT_circle3")
drawCircle(-chip_x/2 + feed + l_cpw + w_cpw + t_cpw + dx_pad +x_pad, y_pad/2, dx_pad, "pT_circle4")

subtract_list += ",padTrenchX,padTrenchY,pT_circle1,pT_circle2,pT_circle3,pT_circle4"


#drawing the inductor
drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw, w_cpw/2 + t_cpw, 0, 270, 360, "cpw_t1_")
unite_list += ",cpw_t1_pinStart"
drawCPW(-chip_x/2 + feed + l_cpw, w_cpw/2 + t_cpw, w_cpw, t_cpw, y_pad/2 - w_cpw/2*3 - t_cpw*2, "y", "cpw_1")
unite_list += ",cpw_1_pin"
drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw + dx_pad + t_cpw + w_cpw, y_t_pad/2 - w_cpw - 2*t_cpw, dx_pad - t_cpw, 90, 180, "cpw_t2_")

unite_list += ",cpw_t2_pinStart"


for i in range(5):
	drawCPW(-chip_x/2 + feed + l_cpw + dx_pad + w_cpw + t_cpw, y_t_pad/2 - w_cpw - 2*t_cpw - i*w_cpw - i*t_cpw, w_cpw, t_cpw, x_pad, "x", "cpw_" + str(2 + 4*i))
	unite_list += ",cpw_" + str (2 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw + x_t_pad - dx_pad + w_cpw + t_cpw, y_t_pad/2 - w_cpw - 2*t_cpw - i*w_cpw - i*t_cpw, dx_pad - w_cpw - 2*t_cpw - i*w_cpw - i*t_cpw, 90, 0, "cpw_t" + str(4*i + 3) + "_")
	unite_list += ",cpw_t" + str(4*i + 3) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw + x_t_pad - t_cpw - i*w_cpw - i*t_cpw, -y_pad/2, w_cpw, t_cpw, y_pad, "y", "cpw_" + str(3 + 4*i))
	unite_list += ",cpw_" + str (3 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw + x_t_pad - dx_pad + w_cpw + t_cpw, -y_t_pad/2 + w_cpw + 2*t_cpw + i*w_cpw + i*t_cpw, dx_pad - w_cpw - 2*t_cpw - i*w_cpw - i*t_cpw, -90, 0, "cpw_t" + str(4*i + 4) + "_")
	unite_list += ",cpw_t" + str(4*i + 4) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw + dx_pad + w_cpw + t_cpw, -y_t_pad/2 + i*w_cpw + i*t_cpw, w_cpw, t_cpw, x_pad, "x", "cpw_" + str(4 + 4*i))
	unite_list += ",cpw_" + str (4 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw + dx_pad + t_cpw + w_cpw, -y_t_pad/2 + w_cpw + 2*t_cpw + i*w_cpw + i*t_cpw, dx_pad - w_cpw - 2*t_cpw - i*w_cpw - i*t_cpw, -90, -180, "cpw_t" + str(4*i + 5) + "_")
	unite_list += ",cpw_t" + str(4*i + 5) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw + t_cpw + w_cpw + i*w_cpw + i*t_cpw, -y_pad/2, w_cpw, t_cpw, y_pad - w_cpw - t_cpw, "y", "cpw_" + str(5 + 4*i))
	unite_list += ",cpw_" + str (5 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw, t_cpw, -chip_x/2 + feed + l_cpw + dx_pad + t_cpw + w_cpw, y_t_pad/2 - 2*w_cpw - 3*t_cpw - i*w_cpw -i*t_cpw, dx_pad - 2*t_cpw - w_cpw -i*w_cpw - i*t_cpw, 90, 180, "cpw_t" + str(6 + 4*i) + "_")
	unite_list += ",cpw_t" + str(4*i + 6) + "_pinStart"



#the wire bounding pad
drawRec(-chip_x/2 + l_cpw + dx_pad + feed + w_cpw + t_cpw, -y_pad/2, x_pad, y_pad, "pad")
unite_list += ",pad"


oEditor.Subtract(
	[
		"NAME:Selections",
		"Blank Parts:="		, "gnd",
		"Tool Parts:="		, subtract_list
	], 
	[
		"NAME:SubtractParameters",
		"KeepOriginals:="	, False
	])

oEditor.Unite(
	[
		"NAME:Selections",
		"Selections:="		, unite_list
	], 
	[
		"NAME:UniteParameters",
		"KeepOriginals:="	, False
	])

