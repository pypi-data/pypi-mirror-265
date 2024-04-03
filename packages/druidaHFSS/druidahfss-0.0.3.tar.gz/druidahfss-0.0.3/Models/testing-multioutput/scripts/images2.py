# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 19:41:01  Dec 12, 2023
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("meta-atom_box_01_datageneration")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.ExportModelImageToFile("C:/Users/jorge/Documents/Projects Jorge C/DRUIDA PROJECT/POC/dbGeneration_v0/Models/testing-multioutput/scripts/image.png", 1156, 634, 
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
