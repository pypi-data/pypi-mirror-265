# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 8:41:23  Nov 06, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("meta-atom_circ_01_datageneration")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Delete(
	[
		"NAME:Selections",
		"Selections:="		, "Cylinder1"
	])
oDesign.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:LocalVariableTab",
			[
				"NAME:PropServers", 
				"LocalVariables"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:parameters",
					"Value:="		, "[0.2, 0.5, 0.5, 0.5] mm"
				]
			]
		]
	])
oDesign.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:LocalVariableTab",
			[
				"NAME:PropServers", 
				"LocalVariables"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:H",
					"Value:="		, "parameters[3]"
				]
			]
		]
	])
oEditor.CreateBox(
	[
		"NAME:BoxParameters",
		"XPosition:="		, "1mm",
		"YPosition:="		, "2mm",
		"ZPosition:="		, "0mm",
		"XSize:="		, "1mm",
		"YSize:="		, "1mm",
		"ZSize:="		, "1mm"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Box2",
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
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"Box2"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Material",
					"Value:="		, "\"pec\""
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Box2:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:XSize",
					"Value:="		, "parameters[0]"
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Box2:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:YSize",
					"Value:="		, "parameters[1]"
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Box2:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:ZSize",
					"Value:="		, "parameters[2]"
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Box2:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Position",
					"X:="			, "1mm",
					"Y:="			, "2mm",
					"Z:="			, "parameters[3]"
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Box2:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Position",
					"X:="			, "Xsize/2 - parameters[0] /2",
					"Y:="			, "Ysize/2 - parameters[1]/2",
					"Z:="			, "parameters[3]"
				]
			]
		]
	])
oProject.Save()
