from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
###################################################################################################
######In case of using this code snippet directly, pay attention to the temperature field, as it might
###### be applied to a set of nodes of different size than the actual model
def analise(arq, matrix, resf):
    
    executeOnCaeStartup()
    #matrix = 'G1'
    #arq = 'CFC-30'
    #resf = 595
    #carga = 'xx'

    if matrix == 'G1':
        aque = 595
    elif matrix == 'G2':
        aque = 605
    elif matrix == 'G3':
        aque= 470
        
    
    path = 'C:/Users/duhju/Desktop/abaqus/modelos/' + arq + '.cae'
    openMdb(pathName=path)
    #: The model database "C:\Users\duhju\Desktop\abaqus\modelos\CFC-30.cae" has been opened.
    p = mdb.models['Cell'].parts['Cell']
    a = mdb.models['Cell'].rootAssembly
    a.regenerate()
    a = mdb.models['Cell'].rootAssembly

    mdb.models['Cell'].StaticStep(name='Step-2', previous='Step-1')
    mdb.models['Cell'].StaticStep(name='Step-3', previous='Step-2')

    a = mdb.models['Cell'].rootAssembly
    n1 = a.instances['Cell-1'].nodes
    region = a.Set(nodes=n1, name='Set-3')

##    if arq == 'CCC-15':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:1840 #1 ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == "CCC-30":
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:1078 #1fff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == 'CCC-45':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:782 #7ff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == 'CFC-15':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == "CFC-30":
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:1736 #7ff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == 'CFC-45':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:1736 #7ff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == 'C-15':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:1066 #7fff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == "C-30":
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:623 #1ffffff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')
##    elif arq == 'C-45':
##        a = mdb.models['Cell'].rootAssembly
##        n1 = a.instances['Cell-1'].nodes
##        nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:515 #7fffff ]', ), )
##        region = a.Set(nodes=nodes1, name='Set-3')

    ###Campo de aquecimento do modelo
    mdb.models['Cell'].Temperature(name='Predefined Field-1', 
        createStepName='Initial', region=region, distributionType=UNIFORM, 
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(0.0, ))
    mdb.models['Cell'].predefinedFields['Predefined Field-1'].setValuesInStep(
        stepName='Step-1', magnitudes=(float(aque), ))
    ###Campo de resfriamento do modelo
    a = mdb.models['Cell'].rootAssembly
    region = a.sets['Set-3']
    mdb.models['Cell'].Temperature(name='Predefined Field-2', 
        createStepName='Step-1', region=region, distributionType=UNIFORM, 
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(float(aque), ))
    mdb.models['Cell'].predefinedFields['Predefined Field-2'].setValuesInStep(
        stepName='Step-2', magnitudes=(float(resf), ))
    ###Condicao de deformacao do modelo

    if resf == aque:
        mdb.models['Cell'].predefinedFields['Predefined Field-2'].suppress()
        
    epso = 1.0e-4
    cargas = ['xx', 'yy', 'zz', 'xy', 'xz', 'yz']
    for carga in cargas:

        if carga=='xx':
            mdb.models['Cell'].boundaryConditions['BC-rp1'].setValuesInStep(
                stepName='Step-3', u1=epso, u2=0.000, u3=0.000)
        elif carga=='yy':
            mdb.models['Cell'].boundaryConditions['BC-rp1'].setValuesInStep(
                stepName='Step-3', u1=0.000, u2=epso, u3=0.000)
        elif carga=='zz':
            mdb.models['Cell'].boundaryConditions['BC-rp1'].setValuesInStep(
                stepName='Step-3', u1=0.000, u2=0.000, u3=epso)
        elif carga=='xy':
            mdb.models['Cell'].boundaryConditions['BC-rp1'].setValuesInStep(
                stepName='Step-3', u1=0.000, u2=0.000, u3=0.000)
            mdb.models['Cell'].boundaryConditions['BC-rp2'].setValuesInStep(
                stepName='Step-3', u1=2*epso, u2=0.000, u3=0.000)
        elif carga=='xz':
            mdb.models['Cell'].boundaryConditions['BC-rp2'].setValuesInStep(
                stepName='Step-3', u1=0.000, u2=2*epso, u3=0.000)
        elif carga=='yz':
            mdb.models['Cell'].boundaryConditions['BC-rp2'].setValuesInStep(
                stepName='Step-3', u1=0.000, u2=0.000, u3=2*epso)

        job = 'Job-'+carga
        ### Analise MEF
        mdb.Job(name=job, model='Cell', description='', type=ANALYSIS, atTime=None, 
            waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, 
            getMemoryFromAnalysis=True, explicitPrecision=SINGLE, 
            nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
            contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
            resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
        mdb.jobs[job].submit(consistencyChecking=OFF)

    
