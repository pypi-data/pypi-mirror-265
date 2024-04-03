# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 15:38:18  Jan 25, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("meta-atom_cross_01_datageneration")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
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
					"Value:="		, "[0.2, 0.5, 0.5, 0.5, 6] mm"
				]
			]
		]
	])
