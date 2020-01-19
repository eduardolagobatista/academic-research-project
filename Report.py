from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

def relat(matrix, resf):

    cargas = ['xx', 'yy', 'zz', 'xy', 'xz', 'yz']
    for carga in cargas:
        job = 'Job-'+carga
        job_path = 'C:/Temp/'+job+'.odb'
        reporto = matrix+'_'+carga+'_'+str(resf)+'.rpt'
        session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=195.443634033203, 
            height=90.3294296264648)
        session.viewports['Viewport: 1'].makeCurrent()
        session.viewports['Viewport: 1'].maximize()
        executeOnCaeStartup()
        session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
            referenceRepresentation=ON)
        o1 = session.openOdb(name=job_path)
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        #: Model: C:/Temp/Job-2.odb
        #: Number of Assemblies:         1
        #: Number of Assembly instances: 0
        #: Number of Part instances:     1
        #: Number of Meshes:             2
        #: Number of Element Sets:       3
        #: Number of Node Sets:          8457
        #: Number of Steps:              3
        odb = session.odbs[job_path]
        nf = NumberFormat(numDigits=8, precision=0, format=ENGINEERING)
        session.fieldReportOptions.setValues(numberFormat=nf)
        session.writeFieldReport(fileName=reporto, append=ON, 
            sortItem='Element Label', odb=odb, step=2, frame=1, 
            outputPosition=INTEGRATION_POINT, variable=(('E', INTEGRATION_POINT, ((
            COMPONENT, 'E11'), (COMPONENT, 'E22'), (COMPONENT, 'E33'), (COMPONENT, 
            'E12'), (COMPONENT, 'E13'), (COMPONENT, 'E23'), )), ('S', 
            INTEGRATION_POINT, ((COMPONENT, 'S11'), (COMPONENT, 'S22'), (COMPONENT, 
            'S33'), (COMPONENT, 'S12'), (COMPONENT, 'S13'), (COMPONENT, 'S23'), )), ))
