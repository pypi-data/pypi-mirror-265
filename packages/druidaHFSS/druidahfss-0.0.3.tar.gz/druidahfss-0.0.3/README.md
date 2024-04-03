# druidaHFSS 
# Ansys HFSS Interface
## _Simulate, data generation, optimization_

This development is intended to provide an interface to access HFSS, in order to automate simulation, Data generation and optimization processes.

## Features

- Automate the re-creation of models in aedt files.
- Create intermediate files to run simulations.
- Run simulations and gather specific metrics from the simulator.

## Usage
```
from dbuilder import Manager as MG
```


```
Builder=MG.Builder(ansysPath=ansysPath,modelName=_,projectName=_, designName=_,modelPath=_, exportPath=_)
```

```
Builder.create()
```

```
Builder.sim_file('', batch, iteration, simfile_path, **kwargs)
```


```    
Builder.simulate(simfile_path+simfileName)
```

```
dbManager=MG.DBManager(ansysPath=ansysPath,
                       modelName=modelName,
                       projectName=project_name,
                       designName=designName,
                       modelPath=modelPath, 
                       dbPath=dBPath,
                      dbName=dbName)
```

```
dbManager.load_df(columns=columnNames)


"""This object can be treated as a pandas dataframe"""
dbManager.df 

```

```
dbManager.insert_row(data_to_store)
```

```
image_rgb=tools.cropImage( file,image_path=path,
                              image_name=fileName_absolute,
                              output_path=imagesPath, 
                             resize_dim=(512,512))
```