# -*- coding: utf-8 -*-
"""
@author: Jorge Cardenas
"""

def createProject():
    
    import ScriptEnv
    oDesktop.RestoreWindow()
    oProject = oDesktop.NewProject()
    

def hffsDesing(oProject, name):
    
    oProject.InsertDesign("HFSS", name, "HFSS Modal Network", "")

def solutionType(oProject, name, solution_type):
    #solution_type =Eigenmode
	#"HFSS Modal Network"

    oDesign = oProject.SetActiveDesign(name)
    oDesign.SetSolutionType(solution_type, [
		"NAME:Options",
		"EnableAutoOpen:="	, False
	])

def load3DObject(oDesign, componentFilePath):
    #component file path
	#  "C:/Users/jorge/Documents/Projects Jorge C/Glide_Symmetry/Designs/Models/GlideCell2.a3dcomp""C:/Users/jorge/Documents/Projects Jorge C/Glide_Symmetry/Designs/Models/GlideCell2.a3dcomp"
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.Insert3DComponent(
	[
		"NAME:InsertComponentData",
		"TargetCS:="		, "Global",
		"ComponentFile:="	, componentFilePath,
		"IsLocal:="		, False,
		"UniqueIdentifier:="	, "",
		[
			"NAME:InstanceParameters",
			"GeometryParameters:="	, "gap=\'2mm\' gWidth=\'1.75mm\' h1_factor=\'0.29999999999999999\' h2_factor=\'0.40000000000000002\' offset_factor=\'0.10000000000000001\' Period=\'8mm\' sep_factor=\'0.5\' SubsH=\'0.76200000000000001mm\' w1_factor=\'0.20000000000000001\' w2_factor=\'0.125\'",
			"MaterialParameters:="	, "",
			"DesignParameters:="	, ""
		]
	])
    
def setVariable(proj,name,value, design):
    oDesign = proj.SetActiveDesign(design)
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
    					"NAME:"+ name,
    					"Value:="		, value
    				]
    			]
    		]
    	])

    
def exportImage(proj,imagesPath,imageName):
	
	oDesign = proj.SetActiveDesign("HFSSDesign1")
	oEditor = oDesign.SetActiveEditor("3D Modeler")
	oEditor.ExportModelImageToFile(imagesPath+"/"+imageName+".png", 1156, 634, 
	[
		"NAME:SaveImageParams",
		"ShowAxis:="		, "False",
		"ShowGrid:="		, "False",
		"ShowRuler:="		, "False",
		"ShowRegion:="		, "Default",
		"Selections:="		, "",
		"FieldPlotSelections:="	, "",
		"Orientation:="		, "Top"
	])


def createResult(proj,path,name,design,simID, resultName):

    oDesign = proj.SetActiveDesign(design)
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(resultName, "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    	], 
    	[
    		"X Component:="		, "Freq",
    		"Y Component:="		, [resultName]
    	], [])

    oModule.ExportToFile(resultName, path+"/output/"+str(simID)+"/files/"+str(resultName)+str(name)+".csv")


#("Eigen Modes Plot 1",
def createEigenReport(proj,path,name,design,simID, resultName):
    oDesign = proj.SetActiveDesign(design)
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(resultName, "Eigenmode Parameters", "Rectangular Plot", "Setup1 : LastAdaptive", [], 
	[
		"px:="			, ["All"],
		"gWidth:="		, ["Nominal"],
		"Period:="		, ["Nominal"],
		"Segments:="		, ["Nominal"],
		"gap:="			, ["Nominal"],
		"h1_factor:="		, ["Nominal"],
		"w1_factor:="		, ["Nominal"],
		"offset_factor:="	, ["Nominal"],
		"h2_factor:="		, ["Nominal"],
		"sep_factor:="		, ["Nominal"],
		"w2_factor:="		, ["Nominal"],
		"SweepPML:="		, ["Nominal"],
		"SubsH:="		, ["Nominal"],
		"py:="			, ["0deg"]
	], 
	[
		"X Component:="		, "px",
		"Y Component:="		, ["re(Mode(1))","re(Mode(2))","re(Mode(3))"]
	])
    oModule.ExportToFile(resultName, path+"/output/"+str(simID)+"/files/"+str(resultName)+str(name)+".csv")
