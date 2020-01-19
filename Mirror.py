from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
def cellmirror(model):
    modelpath = 'C:/Users/duhju/Desktop/abaqus/modelos/' + model +'.cae'
    executeOnCaeStartup()
    a = mdb.models['Model-1'].rootAssembly
    mdb.ModelFromInputFile(name='Cell', inputFileName='C:/Temp/Cell.inp')
    a = mdb.models['Cell'].rootAssembly
    a = mdb.models['Model-1'].rootAssembly
    del mdb.models['Model-1']
    a = mdb.models['Cell'].rootAssembly
    p1 = mdb.models['Cell'].parts['PART-3']
    p = mdb.models['Cell'].Part(name='PART-1', 
        objectToCopy=mdb.models['Cell'].parts['PART-3'], compressFeatureList=ON, 
        mirrorPlane=XYPLANE)
    p1 = mdb.models['Cell'].parts['PART-3']
    p = mdb.models['Cell'].Part(name='PART-2', 
        objectToCopy=mdb.models['Cell'].parts['PART-3'], compressFeatureList=ON, 
        mirrorPlane=YZPLANE)
    p1 = mdb.models['Cell'].parts['PART-2']
    p = mdb.models['Cell'].Part(name='PART-4', 
        objectToCopy=mdb.models['Cell'].parts['PART-2'], compressFeatureList=ON, 
        mirrorPlane=XYPLANE)
    p1 = mdb.models['Cell'].parts['PART-3']
    p = mdb.models['Cell'].Part(name='PART-5', 
        objectToCopy=mdb.models['Cell'].parts['PART-3'], compressFeatureList=ON, 
        mirrorPlane=XZPLANE)
    p1 = mdb.models['Cell'].parts['PART-5']
    p = mdb.models['Cell'].Part(name='PART-6', 
        objectToCopy=mdb.models['Cell'].parts['PART-5'], compressFeatureList=ON, 
        mirrorPlane=XYPLANE)
    p1 = mdb.models['Cell'].parts['PART-5']
    p = mdb.models['Cell'].Part(name='PART-7', 
        objectToCopy=mdb.models['Cell'].parts['PART-5'], compressFeatureList=ON, 
        mirrorPlane=YZPLANE)
    p1 = mdb.models['Cell'].parts['PART-7']
    p = mdb.models['Cell'].Part(name='PART-8', 
        objectToCopy=mdb.models['Cell'].parts['PART-7'], compressFeatureList=ON, 
        mirrorPlane=XYPLANE)
    a = mdb.models['Cell'].rootAssembly
    a = mdb.models['Cell'].rootAssembly
    p = mdb.models['Cell'].parts['PART-2']
    a.Instance(name='PART-2-1', part=p, dependent=ON)
    p = mdb.models['Cell'].parts['PART-4']
    a.Instance(name='PART-4-1', part=p, dependent=ON)
    p = mdb.models['Cell'].parts['PART-5']
    a.Instance(name='PART-5-1', part=p, dependent=ON)
    p = mdb.models['Cell'].parts['PART-6']
    a.Instance(name='PART-6-1', part=p, dependent=ON)
    p = mdb.models['Cell'].parts['PART-7']
    a.Instance(name='PART-7-1', part=p, dependent=ON)
    p = mdb.models['Cell'].parts['PART-8']
    a.Instance(name='PART-8-1', part=p, dependent=ON)
    a = mdb.models['Cell'].rootAssembly
    a1 = mdb.models['Cell'].rootAssembly
    p = mdb.models['Cell'].parts['PART-1']
    a1.Instance(name='PART-1-1', part=p, dependent=ON)
    a1 = mdb.models['Cell'].rootAssembly
    a1.InstanceFromBooleanMerge(name='Cell', instances=(a1.instances['PART-3-1'], 
        a1.instances['PART-2-1'], a1.instances['PART-4-1'], 
        a1.instances['PART-5-1'], a1.instances['PART-6-1'], 
        a1.instances['PART-7-1'], a1.instances['PART-8-1'], 
        a1.instances['PART-1-1'], ), mergeNodes=BOUNDARY_ONLY, 
        nodeMergingTolerance=1e-06, domain=MESH, originalInstances=SUPPRESS)
    mdb.models['Cell'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.saveAs(pathName=modelpath)
    #: The model database has been saved.
