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
oProject = oDesktop.SetActiveProject("SN010_qubit_design")
#Define HFSS design name
oDesign = oProject.SetActiveDesign("test")
#Define modeler name
oEditor = oDesign.SetActiveEditor("3D Modeler")

#Center locations of x and y
x_center = 0
y_center = 0
#Define orientation -- which direction does the connection point to
orientation = "x"


#chip size in um
chip_x = 5000
chip_y = 2000
chip_z = 280

#coupled pins
start = 100
w_cp = 0.9
g_c_cp = 0.7
g_g_cp = 0.5
l_cp = 500
t_cp = 2*w_cp + 2*g_g_cp + g_c_cp
r_turn = 30
d_finger = 60
l_finger = 400
l_cp2 = 50

w_cpw = 1.8
l_transition = 3
l_cpw = 1500 - 20
l_filter_transition = 20
arm_x = 920
arm_w = 3.6
arm_t = 1.1
arm_l = 400

#drawing functions
def unite(u_list):
	oEditor.Unite(
	[
		"NAME:Selections",
		"Selections:="		, u_list
	], 
	[
		"NAME:UniteParameters",
		"KeepOriginals:="	, False
	])
def cover(line):
	oEditor.CoverLines(
	[
			"NAME:Selections",
			"Selections:="		, line,
			"NewPartsModelFlag:="	, "Model"
	])
def subtract(a, b):
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, a,
			"Tool Parts:="		, b
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])
def drawGenCurve(x_fun, y_fun, t_start, t_end, name):
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, x_fun,
			"YtFunction:="		, y_fun,
			"ZtFunction:="		, "0",
			"tStart:="		, t_start,
			"tEnd:="		, t_end,
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
def drawCurve(x_start, y_start, rad_start, rad_end, r, name):
	oEditor.CreateEquationCurve(
		[
			"NAME:EquationBasedCurveParameters",
			"XtFunction:="		, str(x_start/1e6) + "+" + str(r/1e6) + "*cos(_t)",
			"YtFunction:="		, str(y_start/1e6) + "+" + str(r/1e6)+ "*sin(_t)",
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
def drawCoupledCPW(x, y, w, g_c, g_g, l, orientation, name):
	if orientation == "x":
		xp = x
		yp = y + g_g
		xpg = x
		ypg = y + g_g + w
		width_trench = l
		width_pin = l
		width_pin_gap = l
		height_trench = 2*w + 2*g_g + g_c
		height_pin = 2*w + g_c
		height_pin_gap = g_c

	elif orientation == "y":
		xp = x + g_g
		yp = y
		xpg = x + g_g + w
		ypg = y
		width_trench = 2*w + 2*g_g + g_c
		width_pin = 2*w + g_c
		width_pin_gap = g_c
		height_trench = l
		height_pin = l
		height_pin_gap = l
	drawRec(x, y, width_trench, height_trench, name + "_trench")
	drawRec(xp, yp, width_pin, height_pin, name + "_pin")
	drawRec(xpg, ypg, width_pin_gap, height_pin_gap, name + "_pin_gap")
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
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, name + "_pin",
			"Tool Parts:="		, name + "_pin_gap"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])
def drawCurvedCoupledCPW(x, y, w, g_c, g_g, r_min, deg_start, deg_end, name):
	rad_start = deg_start/180*math.pi
	rad_end = deg_end/180*math.pi
	x0 = x - r_min*math.cos(rad_start)
	y0 = y - r_min*math.sin(rad_start)
	#trench
	drawCurve(x0, y0, rad_start, rad_end, r_min, name + "_innerTrenchArc")
	drawCurve(x0, y0, rad_start, rad_end, r_min + t_cp, name + "_outerTrenchArc")
	drawGenCurve(str(x/1e6) +"+_t*cos(" +str(rad_start) + ")", str(y/1e6) +"+_t*sin(" +str(rad_start) + ")", '0', str(t_cp/1e6), name + '_lineStart')
	drawGenCurve(str((x0 + math.cos(rad_end)*r_min)/1e6) +"+_t*cos(" +str(rad_end) + ")", str((y0 + math.sin(rad_end)*r_min)/1e6) +"+_t*sin(" +str(rad_end) + ")", '0', str(t_cp/1e6), name + '_lineEnd')
	unite(name + '_innerTrenchArc,' + name + '_outerTrenchArc,' + name + '_lineStart,' + name + '_lineEnd') 
	cover(name + "_innerTrenchArc")
	subtract('gnd', name + '_innerTrenchArc')
	#pin
	drawCurve(x0, y0, rad_start, rad_end, r_min + g_g, name + '_innerPinArc')
	drawCurve(x0, y0, rad_start, rad_end, r_min + t_cp - g_g, name + '_outerPinArc')
	drawGenCurve(str((x + math.cos(rad_start)*g_g)/1e6) +"+_t*cos(" +str(rad_start) + ")", str((y + math.sin(rad_start)*g_g)/1e6) +"+_t*sin(" +str(rad_start) + ")", '0', str((t_cp - 2*g_g)/1e6), name + '_pinStart')
	drawGenCurve(str((x0 + math.cos(rad_end)*(r_min + g_g))/1e6) +"+_t*cos(" +str(rad_end) + ")", str((y0 + math.sin(rad_end)*(r_min + g_g))/1e6) +"+_t*sin(" +str(rad_end) + ")", '0', str((t_cp - 2*g_g)/1e6), name + '_pinEnd')
	unite(name + '_innerPinArc,' + name + '_outerPinArc,' + name + '_pinStart,' + name + '_pinEnd') 
	cover(name + "_innerPinArc")
	#pin gap
	drawCurve(x0, y0, rad_start, rad_end, r_min + g_g + w, name + '_innerPinGapArc')
	drawCurve(x0, y0, rad_start, rad_end, r_min + t_cp - g_g - w, name + '_outerPinGapArc')
	drawGenCurve(str((x + math.cos(rad_start)*(g_g + w))/1e6) +"+_t*cos(" +str(rad_start) + ")", str((y + math.sin(rad_start)*(g_g + w))/1e6) +"+_t*sin(" +str(rad_start) + ")", '0', str((g_c)/1e6), name + '_pinGapStart')
	drawGenCurve(str((x0 + math.cos(rad_end)*(r_min + g_g + w))/1e6) +"+_t*cos(" +str(rad_end) + ")", str((y0 + math.sin(rad_end)*(r_min + g_g + w))/1e6) +"+_t*sin(" +str(rad_end) + ")", '0', str((g_c)/1e6), name + '_pinGapEnd')
	unite(name + '_innerPinGapArc,' + name + '_outerPinGapArc,' + name + '_pinGapStart,' + name + '_pinGapEnd') 
	cover(name + "_innerPinGapArc")
	subtract(name + '_innerPinArc', name + '_innerPinGapArc')
def drawBox(x, y, z, dx, dy, dz, material, name):
	oEditor.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, str(x) + "um",
			"YPosition:="		, str(y) + "um",
			"ZPosition:="		, str(z) + "um",
			"XSize:="		, str(dx) + 'um',
			"YSize:="		, str(dy) + 'um',
			"ZSize:="		, str(dz) + 'um'
		], 
		[
			"NAME:Attributes",
			"Name:="		, name,
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, material,
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
#substrate
drawBox(-chip_x/2, -chip_y/2, 0, chip_x, chip_y, -chip_z, "\"silicon\"", "substrate")
#Ground
drawRec(-chip_x/2, -chip_y/2, chip_x, chip_y, "gnd")

#coupled pins
drawRec(-chip_x/2 + start, -t_cp/2, -2, t_cp, 'trap_trench')
subtract('gnd', 'trap_trench')
drawCoupledCPW(-chip_x/2 + start, -t_cp/2, w_cp, g_c_cp, g_g_cp, l_cp, 'x', 'coupled')

drawCurvedCoupledCPW(-chip_x/2 + start + l_cp, t_cp/2, w_cp, g_c_cp, g_g_cp, r_turn, -90, 0, 't1')

drawCoupledCPW(-chip_x/2 + start + l_cp + r_turn, t_cp/2 + r_turn, w_cp, g_c_cp, g_g_cp, l_finger/2 - t_cp/2 - r_turn, 'y', 'finger0')

unite_list = "coupled_pin,t1_innerPinArc,finger0_pin"

for i in range(4):
	drawCoupledCPW(-chip_x/2 + start + l_cp + r_turn + d_finger*(i + 1), -l_finger/2, w_cp, g_c_cp, g_g_cp, l_finger, 'y', 'finger' + str(i + 1))
	unite_list += ",finger" + str(i + 1) + "_pin"
for i in range(2):
	drawCurvedCoupledCPW(-chip_x/2 + start + l_cp + r_turn + t_cp + d_finger + d_finger*2*i, - l_finger/2, w_cp, g_c_cp, g_g_cp, (r_turn -  t_cp/2), 180, 360, 'left_t' + str(i + 1))
	unite_list += ',left_t' + str(i + 1) + "_innerPinArc"
for i in range(3):
	drawCurvedCoupledCPW(-chip_x/2 + start + l_cp + r_turn + t_cp + d_finger*2*i, l_finger/2, w_cp, g_c_cp, g_g_cp, (r_turn -  t_cp/2), 180, 0, 'right_t' + str(i + 1))
	unite_list += ',right_t' + str(i + 1) + "_innerPinArc"


drawCoupledCPW(-chip_x/2 + start + l_cp + r_turn + 5*d_finger,  t_cp/2 + r_turn, w_cp, g_c_cp, g_g_cp,  l_finger/2 - t_cp/2 - r_turn, 'y', 'finger6')
unite_list += ",finger6_pin"

drawCurvedCoupledCPW(-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp, r_turn + t_cp/2, w_cp, g_c_cp, g_g_cp, r_turn, 180, 270, 't2')
unite_list += ",t2_innerPinArc"

drawCoupledCPW(-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn, -t_cp/2, w_cp, g_c_cp, g_g_cp, l_cp2, 'x', 'coupled2')
unite_list += ",coupled2_pin"

#the trensition region
drawRec(-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2, -t_cp/2, l_transition, t_cp, 'transition_trench')
subtract('gnd', 'transition_trench')
drawGenCurve(str((-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2)/1e6), str((-w_cp - g_c_cp/2)/1e6) + "+_t", '0', str((2*w_cp + g_c_cp)/1e6), 'transition_long')
drawGenCurve(str((-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2 + l_transition)/1e6), str((-w_cpw/2)/1e6) + "+_t", '0', str((w_cpw)/1e6), 'transition_short')
drawGenCurve(str((-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2)/1e6) + "+3e-6*_t", str((-w_cp - g_c_cp/2)/1e6) + "+0.35e-6*_t", '0', '1', 'transition_left')
drawGenCurve(str((-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2)/1e6) + "+3e-6*_t", str((w_cp + g_c_cp/2)/1e6) + "-0.35e-6*_t", '0', '1', 'transition_right')
unite('transition_long,transition_short,transition_left,transition_right')
cover('transition_long')
unite_list += ",transition_long"


drawCPW(-chip_x/2 + start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2 + l_transition, -t_cp/2, w_cpw, (t_cp - w_cpw)/2, l_cpw, 'x', 'tail')
unite_list += ",tail_pin"

drawCPW(-chip_x/2 + start + arm_x, g_c_cp/2, arm_w, arm_t, arm_l, 'y', 'arm')
unite_list += ',arm_pin'





#the filter part
feed = start + l_cp + r_turn + 5*d_finger + t_cp + r_turn + l_cp2 + l_transition + l_cpw + l_filter_transition
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
l_cpw_filter = 285.35
#width of the cpw in um
w_cpw_filter = 3
#trench for the cpw in um
t_cpw_filter = 2.5


#the main bone of the filter
w_filter_main = 4
t_filter_main = 4

#pad trench dimensions
x_t_pad = 260+200
x_pad = 200+200
y_t_pad = 260+200
y_pad = 200+200
dx_pad = (x_t_pad - x_pad)/2


drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6), str((-t_cp/2)/1e6) + "+_t", '0', str((t_cp)/1e6), 'tft_short')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition + l_filter_transition)/1e6), str((-(w_cpw_filter + 2*t_cpw_filter)/2)/1e6) + "+_t", '0', str((w_cpw_filter + 2* t_cpw_filter)/1e6), 'tft_long')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6) + "+20e-6*_t", str((-t_cp/2)/1e6) + "-2.25e-6*_t", '0', '1', 'tft_left')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6) + "+20e-6*_t", str((t_cp/2)/1e6) + "+2.25e-6*_t", '0', '1', 'tft_right')
unite('tft_short,tft_long,tft_left,tft_right')
cover('tft_short')
subtract('gnd', 'tft_short')

drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6), str((-w_cpw/2)/1e6) + "+_t", '0', str((w_cpw)/1e6), 'tfp_short')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition + l_filter_transition)/1e6), str((-(w_cpw_filter)/2)/1e6) + "+_t", '0', str((w_cpw_filter)/1e6), 'tfp_long')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6) + "+20e-6*_t", str((-w_cpw/2)/1e6) + "-0.6e-6*_t", '0', '1', 'tfp_left')
drawGenCurve(str((-chip_x/2 + feed - l_filter_transition)/1e6) + "+20e-6*_t", str((w_cpw/2)/1e6) + "+0.6e-6*_t", '0', '1', 'tfp_right')
unite('tfp_short,tfp_long,tfp_left,tfp_right')
cover('tfp_short') 
unite_list += ',tfp_short'



#cpw for filter
drawCPW(-chip_x/2 + feed, -(w_cpw_filter + 2*t_cpw_filter)/2, w_cpw_filter, t_cpw_filter, l_cpw_filter, 'x', 'filter')
unite_list += ',filter_pin'
#trench and fins for the fingers
finger_x = []
finger_y = []
subtract_list = "capTrench1"



for i in range(n_f):
    finger_x.append(i*s_f)
    finger_y.append(-h_f/2)

for i in range(n_f - 1):
	subtract_list += ",capTrench" + str(i + 2)
	
 
for i in range(n_f):
	drawRec(finger_x[i] - chip_x/2 + feed, finger_y[i], w_f + 2*w_ft, h_f + 2*w_ft, "capTrench" + str(i+1))
	drawRec(finger_x[i] - chip_x/2 + feed + w_ft, finger_y[i], w_f, h_f, "capFin" + str(i+1))
	unite_list += ",capFin" + str(i + 1)




#pad trenches
drawRec(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter, -y_pad/2, x_t_pad, y_pad, "padTrenchX")
drawRec(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter + dx_pad, -y_t_pad/2, x_pad, y_t_pad, "padTrenchY")
drawCircle(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter + dx_pad, -y_pad/2, dx_pad, "pT_circle1")
drawCircle(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter + dx_pad, +y_pad/2, dx_pad, "pT_circle2")
drawCircle(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter + dx_pad + x_pad, -y_pad/2, dx_pad, "pT_circle3")
drawCircle(-chip_x/2 + feed + l_cpw_filter + w_cpw_filter + t_cpw_filter + dx_pad +x_pad, y_pad/2, dx_pad, "pT_circle4")

subtract_list += ",padTrenchX,padTrenchY,pT_circle1,pT_circle2,pT_circle3,pT_circle4"


#drawing the inductor
drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter, w_cpw_filter/2 + t_cpw_filter, 0, 270, 360, "cpw_t1_")
unite_list += ",cpw_t1_pinStart"
drawCPW(-chip_x/2 + feed + l_cpw_filter, w_cpw_filter/2 + t_cpw_filter, w_cpw_filter, t_cpw_filter, y_pad/2 - w_cpw_filter/2*3 - t_cpw_filter*2, "y", "cpw_1")
unite_list += ",cpw_1_pin"
drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter + dx_pad + t_cpw_filter + w_cpw_filter, y_t_pad/2 - w_cpw_filter - 2*t_cpw_filter, dx_pad - t_cpw_filter, 90, 180, "cpw_t2_")

unite_list += ",cpw_t2_pinStart"


for i in range(5):
	drawCPW(-chip_x/2 + feed + l_cpw_filter + dx_pad + w_cpw_filter + t_cpw_filter, y_t_pad/2 - w_cpw_filter - 2*t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, w_cpw_filter, t_cpw_filter, x_pad, "x", "cpw_" + str(2 + 4*i))
	unite_list += ",cpw_" + str (2 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter + x_t_pad - dx_pad + w_cpw_filter + t_cpw_filter, y_t_pad/2 - w_cpw_filter - 2*t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, dx_pad - w_cpw_filter - 2*t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, 90, 0, "cpw_t" + str(4*i + 3) + "_")
	unite_list += ",cpw_t" + str(4*i + 3) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw_filter + x_t_pad - t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, -y_pad/2, w_cpw_filter, t_cpw_filter, y_pad, "y", "cpw_" + str(3 + 4*i))
	unite_list += ",cpw_" + str (3 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter + x_t_pad - dx_pad + w_cpw_filter + t_cpw_filter, -y_t_pad/2 + w_cpw_filter + 2*t_cpw_filter + i*w_cpw_filter + i*t_cpw_filter, dx_pad - w_cpw_filter - 2*t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, -90, 0, "cpw_t" + str(4*i + 4) + "_")
	unite_list += ",cpw_t" + str(4*i + 4) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw_filter + dx_pad + w_cpw_filter + t_cpw_filter, -y_t_pad/2 + i*w_cpw_filter + i*t_cpw_filter, w_cpw_filter, t_cpw_filter, x_pad, "x", "cpw_" + str(4 + 4*i))
	unite_list += ",cpw_" + str (4 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter + dx_pad + t_cpw_filter + w_cpw_filter, -y_t_pad/2 + w_cpw_filter + 2*t_cpw_filter + i*w_cpw_filter + i*t_cpw_filter, dx_pad - w_cpw_filter - 2*t_cpw_filter - i*w_cpw_filter - i*t_cpw_filter, -90, -180, "cpw_t" + str(4*i + 5) + "_")
	unite_list += ",cpw_t" + str(4*i + 5) + "_pinStart"
	drawCPW(-chip_x/2 + feed + l_cpw_filter + t_cpw_filter + w_cpw_filter + i*w_cpw_filter + i*t_cpw_filter, -y_pad/2, w_cpw_filter, t_cpw_filter, y_pad - w_cpw_filter - t_cpw_filter, "y", "cpw_" + str(5 + 4*i))
	unite_list += ",cpw_" + str (5 + 4*i) + "_pin"
	drawCurvedCPW(w_cpw_filter, t_cpw_filter, -chip_x/2 + feed + l_cpw_filter + dx_pad + t_cpw_filter + w_cpw_filter, y_t_pad/2 - 2*w_cpw_filter - 3*t_cpw_filter - i*w_cpw_filter -i*t_cpw_filter, dx_pad - 2*t_cpw_filter - w_cpw_filter -i*w_cpw_filter - i*t_cpw_filter, 90, 180, "cpw_t" + str(6 + 4*i) + "_")
	unite_list += ",cpw_t" + str(4*i + 6) + "_pinStart"



#the wire bounding pad
drawRec(-chip_x/2 + l_cpw_filter + dx_pad + feed + w_cpw_filter + t_cpw_filter, -y_pad/2, x_pad, y_pad, "pad")
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



#oEditor.Subtract(
#	[
#		"NAME:Selections",
#		"Blank Parts:="		, "gnd",
#		"Tool Parts:="		, subtract_list
#	], 
#	[
#		"NAME:SubtractParameters",
#		"KeepOriginals:="	, False
#	])
