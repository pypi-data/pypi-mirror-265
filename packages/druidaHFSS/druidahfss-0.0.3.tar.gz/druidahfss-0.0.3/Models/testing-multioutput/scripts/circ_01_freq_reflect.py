# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 7:44:34  Oct 17, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "HFSSDesign1", "HFSS Modal Network", "")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "0mm",
		"YStart:="		, "0mm",
		"ZStart:="		, "0mm",
		"Width:="		, "2mm",
		"Height:="		, "1.6mm",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Rectangle1",
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
				"NAME:NewProps",
				[
					"NAME:Xsize",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "5mm"
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
				"Rectangle1:CreateRectangle:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:XSize",
					"Value:="		, "Xsize"
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
				"NAME:NewProps",
				[
					"NAME:Ysize",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "6mm"
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
    				"NAME:NewProps",
    				[
    					"NAME:" +"parameters",
    					"PropType:="		, "VariableProp",
    					"UserDef:="		, True,
    					"Value:="		, "[0.2]mm"
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
				"Rectangle1:CreateRectangle:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:YSize",
					"Value:="		, "Ysize"
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
					"NAME:Ysize",
					"Value:="		, "5mm"
				]
			]
		]
	])
oEditor.CreateBox(
	[
		"NAME:BoxParameters",
		"XPosition:="		, "0mm",
		"YPosition:="		, "0mm",
		"ZPosition:="		, "0mm",
		"XSize:="		, "5mm",
		"YSize:="		, "5mm",
		"ZSize:="		, "1.4mm"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Box1",
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
				"Box1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Material",
					"Value:="		, "\"Rogers RT/duroid 5880 (tm)\""
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
				"Box1:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:XSize",
					"Value:="		, "Xsize"
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
				"Box1:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:YSize",
					"Value:="		, "Ysize"
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
				"NAME:NewProps",
				[
					"NAME:H",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "0.5mm"
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
				"Box1:CreateBox:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:ZSize",
					"Value:="		, "H"
				]
			]
		]
	])
oEditor.CreateCylinder(
	[
		"NAME:CylinderParameters",
		"XCenter:="		, "1.6mm",
		"YCenter:="		, "2mm",
		"ZCenter:="		, "0mm",
		"Radius:="		, "0.848528137423857mm",
		"Height:="		, "0.4mm",
		"WhichAxis:="		, "Z",
		"NumSides:="		, "0"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Cylinder1",
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
				"Cylinder1"
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
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignPerfectE(
	[
		"NAME:PerfE1",
		"Objects:="		, ["Rectangle1"],
		"InfGroundPlane:="	, False
	])
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"Cylinder1:CreateCylinder:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Center Position",
					"X:="			, "1.6mm",
					"Y:="			, "2mm",
					"Z:="			, "H"
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
				"Cylinder1:CreateCylinder:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Center Position",
					"X:="			, "Xsize/2",
					"Y:="			, "Ysize/2",
					"Z:="			, "H"
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
				"NAME:NewProps",
				[
					"NAME:margin",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "1mm"
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
				"Cylinder1:CreateCylinder:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Radius",
					"Value:="		, "parameters[0]"
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
					"NAME:margin",
					"Value:="		, "1mm"
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
				"Cylinder1:CreateCylinder:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Radius",
					"Value:="		, "Xsize/2"
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
				"Cylinder1:CreateCylinder:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Radius",
					"Value:="		, "parameters[0]"
				]
			]
		]
	])
oEditor.CreateRegion(
	[
		"NAME:RegionParameters",
		"+XPaddingType:="	, "Absolute Offset",
		"+XPadding:="		, "0mm",
		"-XPaddingType:="	, "Absolute Offset",
		"-XPadding:="		, "0mm",
		"+YPaddingType:="	, "Absolute Offset",
		"+YPadding:="		, "0mm",
		"-YPaddingType:="	, "Absolute Offset",
		"-YPadding:="		, "0mm",
		"+ZPaddingType:="	, "Absolute Offset",
		"+ZPadding:="		, "10mm",
		"-ZPaddingType:="	, "Absolute Offset",
		"-ZPadding:="		, "10mm"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Region",
		"Flags:="		, "Wireframe#",
		"Color:="		, "(143 175 143)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "nan ",
		"IsMaterialEditable:="	, True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])
oModule.AssignPrimary(
	[
		"NAME:Primary1",
		"Faces:="		, [61],
		[
			"NAME:CoordSysVector",
			"Coordinate System:="	, "Global",
			"Origin:="		, ["5mm","0mm","10.9mm"],
			"UPos:="		, ["5mm","5mm","10.9mm"]
		],
		"ReverseV:="		, False
	])
oModule.AssignPrimary(
	[
		"NAME:Primary2",
		"Faces:="		, [60],
		[
			"NAME:CoordSysVector",
			"Coordinate System:="	, "Global",
			"Origin:="		, ["5mm","5mm","10.9mm"],
			"UPos:="		, ["0mm","5mm","10.9mm"]
		],
		"ReverseV:="		, False
	])
oModule.AssignSecondary(
	[
		"NAME:Secondary1",
		"Faces:="		, [58],
		[
			"NAME:CoordSysVector",
			"Coordinate System:="	, "Global",
			"Origin:="		, ["5mm","0mm","10.9mm"],
			"UPos:="		, ["0mm","0mm","10.9mm"]
		],
		"ReverseV:="		, True,
		"Primary:="		, "Primary2",
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg"
	])
oModule.AssignSecondary(
	[
		"NAME:Secondary2",
		"Faces:="		, [59],
		[
			"NAME:CoordSysVector",
			"Coordinate System:="	, "Global",
			"Origin:="		, ["0mm","0mm","10.9mm"],
			"UPos:="		, ["0mm","5mm","10.9mm"]
		],
		"ReverseV:="		, True,
		"Primary:="		, "Primary1",
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg"
	])
oModule.AssignFloquetPort(
	[
		"NAME:FloquetPort1",
		"Faces:="		, [56],
		"NumModes:="		, 2,
		"DoDeembed:="		, True,
		"DeembedDist:="		, "10mm",
		"RenormalizeAllTerminals:=", True,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			],
			[
				"NAME:Mode2",
				"ModeNum:="		, 2,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [False,False],
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg",
		[
			"NAME:LatticeAVector",
			"Coordinate System:="	, "Global",
			"Start:="		, ["5mm","0mm","10.9mm"],
			"End:="			, ["5mm","5mm","10.9mm"]
		],
		[
			"NAME:LatticeBVector",
			"Coordinate System:="	, "Global",
			"Start:="		, ["5mm","0mm","10.9mm"],
			"End:="			, ["0mm","0mm","10.9mm"]
		],
		[
			"NAME:ModesList",
			[
				"NAME:Mode",
				"ModeNumber:="		, 1,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TE",
				"AffectsRefinement:="	, True
			],
			[
				"NAME:Mode",
				"ModeNumber:="		, 2,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TM",
				"AffectsRefinement:="	, True
			]
		]
	])
oModule.AssignFloquetPort(
	[
		"NAME:FloquetPort2",
		"Faces:="		, [57],
		"NumModes:="		, 2,
		"DoDeembed:="		, True,
		"DeembedDist:="		, "10mm",
		"RenormalizeAllTerminals:=", True,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			],
			[
				"NAME:Mode2",
				"ModeNum:="		, 2,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [False,False],
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg",
		[
			"NAME:LatticeAVector",
			"Coordinate System:="	, "Global",
			"Start:="		, ["5mm","0mm","-10mm"],
			"End:="			, ["5mm","5mm","-10mm"]
		],
		[
			"NAME:LatticeBVector",
			"Coordinate System:="	, "Global",
			"Start:="		, ["5mm","0mm","-10mm"],
			"End:="			, ["0mm","0mm","-10mm"]
		],
		[
			"NAME:ModesList",
			[
				"NAME:Mode",
				"ModeNumber:="		, 1,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TE",
				"AffectsRefinement:="	, True
			],
			[
				"NAME:Mode",
				"ModeNumber:="		, 2,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TM",
				"AffectsRefinement:="	, True
			]
		]
	])
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssDriven", 
	[
		"NAME:Setup1",
		"SolveType:="		, "Single",
		"Frequency:="		, "60GHz",
		"MaxDeltaS:="		, 0.02,
		"UseMatrixConv:="	, False,
		"MaximumPasses:="	, 10,
		"MinimumPasses:="	, 1,
		"MinimumConvergedPasses:=", 1,
		"PercentRefinement:="	, 30,
		"IsEnabled:="		, True,
		[
			"NAME:MeshLink",
			"ImportMesh:="		, False
		],
		"BasisOrder:="		, 1,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.3333,
		"UseMaxTetIncrease:="	, False,
		"PortAccuracy:="	, 2,
		"UseABCOnPort:="	, False,
		"SetPortMinMaxTri:="	, False,
		"UseDomains:="		, False,
		"UseIterativeSolver:="	, False,
		"EnhancedLowFreqAccuracy:=", False,
		"SaveRadFieldsOnly:="	, False,
		"SaveAnyFields:="	, True,
		"IESolverType:="	, "Auto",
		"LambdaTargetForIESolver:=", 0.15,
		"UseDefaultLambdaTgtForIESolver:=", True,
		"IE Solver Accuracy:="	, "Balanced",
		"InfiniteSphereSetup:="	, ""
	])
oModule.InsertFrequencySweep("Setup1", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearStep",
		"RangeStart:="		, "30GHz",
		"RangeEnd:="		, "90GHz",
		"RangeStep:="		, "0.1GHz",
		"Type:="		, "Interpolating",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"InterpTolerance:="	, 0.5,
		"InterpMaxSolns:="	, 250,
		"InterpMinSolns:="	, 0,
		"InterpMinSubranges:="	, 1,
		"InterpUseS:="		, True,
		"InterpUsePortImped:="	, False,
		"InterpUsePropConst:="	, True,
		"UseDerivativeConvergence:=", False,
		"InterpDerivTolerance:=", 0.2,
		"UseFullBasis:="	, True,
		"EnforcePassivity:="	, True,
		"PassivityErrorTolerance:=", 0.0001,
		"SMatrixOnlySolveMode:=", "Auto"
	])
oProject.SaveAs("C:\\Users\\jorge\\Documents\\Projects Jorge C\\DRUIDA PROJECT\\POC\\dbGeneration_v0\\Models\\testing-multioutput\\meta-atom_circ_01_datageneration.aedt", True)
oDesktop.CloseProject("meta-atom_05_datageneration")