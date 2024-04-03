# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 13:55:07  Dec 02, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "HFSSDesign1", "HFSS Modal Network", "")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oDesign.SetSolutionType("Eigenmode", 
	[
		"NAME:Options",
		"EnableAutoOpen:="	, False
	])
oDesign.SetSolutionType("HFSS Modal Network")
oDesign.SetSolutionType("Eigenmode", 
	[
		"NAME:Options",
		"EnableAutoOpen:="	, False
	])
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Insert3DComponent(
	[
		"NAME:InsertComponentData",
		"TargetCS:="		, "Global",
		"ComponentFile:="	, "C:/Users/jorge/Documents/Projects Jorge C/Glide_Symmetry/Designs/Models/GlideCell2.a3dcomp",
		"IsLocal:="		, False,
		"UniqueIdentifier:="	, "",
		[
			"NAME:InstanceParameters",
			"GeometryParameters:="	, "gap=\'2mm\' gWidth=\'1.75mm\' h1_factor=\'0.29999999999999999\' h2_factor=\'0.40000000000000002\' offset_factor=\'0.10000000000000001\' Period=\'8mm\' sep_factor=\'0.5\' SubsH=\'0.76200000000000001mm\' w1_factor=\'0.20000000000000001\' w2_factor=\'0.125\'",
			"MaterialParameters:="	, "",
			"DesignParameters:="	, ""
		]
	])
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Delete(
	[
		"NAME:Selections",
		"Selections:="		, "cell1"
	])
