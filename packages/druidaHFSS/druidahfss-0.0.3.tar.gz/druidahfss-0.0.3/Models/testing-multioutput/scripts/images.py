# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 14:27:30  Dec 12, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("meta-atom_box_01_datageneration")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
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
					"NAME:Color",
					"R:="			, 255,
					"G:="			, 0,
					"B:="			, 0
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"Box1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Color",
					"R:="			, 0,
					"G:="			, 0,
					"B:="			, 255
				]
			]
		]
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"Rectangle1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Color",
					"R:="			, 255,
					"G:="			, 0,
					"B:="			, 0
				]
			]
		]
	])
oEditor.ExportModelImageToFile("C:/Users/jorge/Documents/Projects Jorge C/DRUIDA PROJECT/POC/dbGeneration_v0/Images/nombreArchivoImagen.jpg", 640, 480, 
	[
		"NAME:SaveImageParams",
		"ShowAxis:="		, "False",
		"ShowGrid:="		, "False",
		"ShowRuler:="		, "False",
		"ShowRegion:="		, "Default",
		"Selections:="		, "",
		"FieldPlotSelections:="	, "",
		"Orientation:="		, ""
	])
