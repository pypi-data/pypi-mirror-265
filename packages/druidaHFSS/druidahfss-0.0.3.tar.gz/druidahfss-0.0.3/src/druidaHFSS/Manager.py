
# -*- coding: utf-8 -*-

"""dataManagement.py
   Author: Jorge Cardenas

   1. Simulation data logging in CSV Files
   2. Simulation data Retrieval

   Future developments:
   1. Local or remote data storage
"""

import csv
import os
import pandas as pd
import os.path as path

import subprocess

class Builder:

    def __init__(self, ansysPath,modelName,projectName, designName, modelPath,scriptPath,exportPath, imagesPath):
        self.ansysPath = ansysPath
        self.modelName = modelName
        self.modelPath = modelPath
        self.exportPath = exportPath
        self.projectName = projectName
        self.designName = designName
        self.imagesPath = imagesPath
        self.scriptPath = scriptPath

        isExist = os.path.exists(self.exportPath)
        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(self.exportPath)
            print("The new Exports directory is created!")

        isExist = os.path.exists(self.imagesPath)
        
        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(self.imagesPath)
            print("The new Images directory is created!")

    def create(self):
        pathString=self.scriptPath + self.modelName+".py"
        subprocess.run([self.ansysPath,"-RunScriptandExit",pathString])

    def simulate(self, filepath):
        subprocess.run([self.ansysPath,"-RunScriptandExit",filepath])

    def sim_file(self, parameters, batch, iteration, filePath, **kwargs):
    
        reports=kwargs['reports']
        simulationID=kwargs['simulation_id']
        variableName=kwargs['variable_name']
        value=kwargs['value']
        units=kwargs['units']
        simFileName=kwargs['sim_file_name']


        tag = "_"+str(batch)+"-"+str(iteration)

        os.chdir( os.path.normpath(filePath))
        drawing = '"' + self.modelPath + self.projectName + '.aedt"'
        print(drawing)

        isExist = os.path.exists(self.exportPath +"/output/"+str(simulationID)+"/files/")


        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(self.exportPath +"/output/"+str(simulationID)+"/files/")
            print("The new directory is created!")

        isExist2 = os.path.exists(self.imagesPath +"/"+str(simulationID)+"/")


        if not isExist2:

            # Create a new directory because it does not exist
            os.makedirs(self.imagesPath +"/"+str(simulationID)+"/")
            print("The new directory is created!")


        f = open(simFileName, "w")  

        #f.write("\n")
 
        f.write("import ScriptEnv\n")
        f.write("import sys\n")
        f.write("import os\n")
        f.write("sys.path.insert(0, './src/')\n")
        f.write("from druidaHFSS.modules import hfss \n")


        f.write("oDesktop.RestoreWindow()\n")
        f.write("oDesktop.OpenProject(" + drawing + ")\n")
        f.write("oProject = oDesktop.SetActiveProject(" + '"'+self.projectName+'"' + ")\n")
        f.write('hfss.setVariable(oProject,"' + variableName + ' ","' + value + units + '","' +self.designName +'")\n')
        
        f.write('oDesign = oProject.SetActiveDesign("' +self.designName  + '")\n')
        f.write("oDesign.AnalyzeAll()")
        f.write("\n")
        f.write('oModule = oDesign.GetModule("OutputVariable")\n')

        for key, val in reports.items():
            f.write('oModule.CreateOutputVariable("' + str(key) + '","'+str(val)+'", "Setup1 : Sweep", "Modal Solution Data", [])\n')

        
        for key, val in reports.items():

            f.write('hfss.createResult(oProject,"' + self.exportPath +'","'+ tag +'","'+ self.designName  +'","'+ simulationID  +'","'+str(key)+'")\n')
        

        
        fileName= str(self.modelName+"_"+ simulationID+tag ) 
        f.write('hfss.exportImage(oProject,"' + self.imagesPath+"/"+str(simulationID) +'","'+fileName+'")\n')


        

        f.close()

    def sim_file_eigen(self, parameters, batch, iteration, filePath, **kwargs):
    
        reports=kwargs['reports']
        simulationID=kwargs['simulation_id']
        variableName=kwargs['variable_name']
        value=kwargs['value']
        units=kwargs['units']
        simfile=kwargs['simfile']

        tag = "_"+str(batch)+"_"+str(iteration)

        os.chdir( os.path.normpath(filePath))
        drawing = '"' + self.modelPath + self.projectName + '.aedt"'
        print(drawing)

        isExist = os.path.exists(self.exportPath +"/output/"+str(simulationID)+"/files/")


        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(self.exportPath +"/output/"+str(simulationID)+"/files/")
            print("The new directory is created!")

        f = open(simfile, "w")  

        #f.write("\n")

        f.write("import ScriptEnv\n")
        f.write("import sys\n")
        f.write("import os\n")
        f.write("sys.path.insert(0, './src/')\n")
        f.write("from druidaHFSS.modules import hfss \n")


        f.write("oDesktop.RestoreWindow()\n")
        f.write("oDesktop.OpenProject(" + drawing + ")\n")
        f.write("oProject = oDesktop.SetActiveProject(" + '"'+self.projectName+'"' + ")\n")

        for idx,item in enumerate(value): 
            f.write('hfss.setVariable(oProject,"' + variableName[idx] + ' ","' + item + units + '","' +self.designName +'")\n')
        
        f.write('oDesign = oProject.SetActiveDesign("' +self.designName  + '")\n')
        f.write("oDesign.AnalyzeAll()")
        f.write("\n")

        
        #for key, val in reports.items():
        #    f.write('oModule.CreateOutputVariable("' + str(key) + '","'+str(val)+'", "Setup1 : Sweep", "Modal Solution Data", [])\n')

        
        for key, val in reports.items():

            f.write('hfss.createEigenReport(oProject,"' + self.exportPath +'","'+ tag +'","'+ self.designName  +'","'+ simulationID  +'","'+str(key)+'")\n')
        

        f.close()



class DataExplorer:

    def __init__(self):
        pass
    
    def load_df():
        pass

    def load_all_df():
        pass

    def load_data():
        pass

    def load_all_batch_data():
        pass

    def merge_all_batch_data():
        pass

    def merge_all_data():
        pass

    
    pass


   
class DBManager:

   file=None
   df = None
   def __init__(self, ansysPath,modelName,projectName, designName, modelPath,dbPath,dbName ):
        self.ansysPath = ansysPath
        self.modelName = modelName
        self.modelPath = modelPath
        self.dbPath = dbPath
        self.projectName = projectName
        self.designName = designName 
        self.dbName = dbName 

        isExist = os.path.exists(self.dbPath)
        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(self.dbPath)
            print("The new DB directory is created!")

        
   def load_df(self, columns):

      if path.exists(self.dbPath+self.dbName):
         self.df = pd.read_csv(self.dbPath+self.dbName, header=0)
      else:
            
        column_names = columns
        self.df = pd.DataFrame(columns = column_names.keys())

        for  (key, value) in columns.items():
            self.df[key]=self.df[key].astype( value)
 
   def insert_row(self,data_struct):
   
      self.df = pd.concat([self.df, pd.DataFrame([data_struct])])
      
      self.df.to_csv(self.dbPath+self.dbName, index=False,sep=',')
      
  
      
     


