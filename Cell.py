from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
def cell(tipo, fraction, matrix, meshsize):
    if tipo == 'CCC':
        sime = float(meshsize)
        sizemesh = 7.2e-05/(sime)
        
        if fraction == '15':
            a = 955.8075e-6
        if fraction == '30':
            a = 758.47e-6
        if fraction == '45':
            a = 662.585e-6
        
        executeOnCaeStartup()
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        #Parts Creation
        s.Spot(point=(0.0, 0.0))
        s.FixedConstraint(entity=v[0])
        s.rectangle(point1=(0.0, 0.0), point2=(13.75, 13.75))
        s.EqualLengthConstraint(entity1=g[2], entity2=g[3])
        s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(a, 0.0), 
        value=a)
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=a)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        del mdb.models['Model-1'].sketches['__profile__']
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        s1.FixedConstraint(entity=g[2])
        s1.Spot(point=(0.0, 0.0))
        s1.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
        s1.FixedConstraint(entity=v[0])
        s1.Line(point1=(16.25, 0.0), point2=(0.0, 0.0))
        s1.HorizontalConstraint(entity=g[3], addUndoState=False)
        s1.Line(point1=(0.0, 0.0), point2=(0.0, 19.2429962158203))
        s1.VerticalConstraint(entity=g[4], addUndoState=False)
        s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
        s1.CoincidentConstraint(entity1=v[4], entity2=g[2], addUndoState=False)
        s1.EqualLengthConstraint(entity1=g[4], entity2=g[3])
        s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 19.2429962158203), point2=(
            19.2429962158203, 0.0), direction=CLOCKWISE)
        s1.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(10.7691106796265, 
            -8.25650024414063), value=0.0005)
        p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-2']
        p.BaseSolidRevolve(sketch=s1, angle=90.0, flipRevolveDirection=OFF)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-2']
        del mdb.models['Model-1'].sketches['__profile__']
        a = mdb.models['Model-1'].rootAssembly
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts['Part-1']
        a.Instance(name='Part-1-1', part=p, dependent=ON)
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-1', part=p, dependent=ON)
        p1 = a.instances['Part-2-1']
        p1.translate(vector=(0.00100580750000034, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-2', part=p, dependent=ON)
        p1 = a.instances['Part-2-2']
        p1.translate(vector=(0.00155580749999906, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        d11 = a.instances['Part-2-2'].datums
        e1 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=d11[1], fixedAxis=e1[7], flip=ON)
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-2'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[4])
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-1'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[3])
        a = mdb.models['Model-1'].rootAssembly
        a.InstanceFromBooleanMerge(name='Part-3', instances=(a.instances['Part-1-1'], 
            a.instances['Part-2-1'], a.instances['Part-2-2'], ), keepIntersections=ON, 
            originalInstances=SUPPRESS, domain=GEOMETRY)

        ## Material Definition - Temperature Dependent
        p = mdb.models['Model-1'].parts['Part-2']
        mdb.models['Model-1'].Material(name='Alumina')
        mdb.models['Model-1'].materials['Alumina'].Elastic(temperatureDependency=ON, 
            table=((326.0e9, 0.24, 298.0), (317.0e9, 0.24, 508.0), (300.0e9, 0.24, 868.0)))
        mdb.models['Model-1'].materials['Alumina'].Expansion(table=((7.6e-06, ), ))
        if str(matrix) == 'G3':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((72.0e9, 0.23, 337.0), (69.2e9, 0.23, 549.0), (61.7e9, 0.23, 736.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((1.16e-05, ), ))
        if str(matrix) == 'G2':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((76.0e9, 0.21, 298.0), (76.0e9, 0.21, 549.0), (76.0e9, 0.21, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((7.4e-06, ), ))

        if str(matrix) == 'G1':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((68.0e9, 0.2, 298.0), (68.0e9, 0.2, 549.0), (68.0e9, 0.2, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((4.6e-06, ), ))
        
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
            material='Alumina', thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', 
            material='Glass', thickness=None)
        p = mdb.models['Model-1'].parts['Part-3']
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-3']
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
        region = p.Set(cells=cells, name='Set-2')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

        ## Mesh Definition
        p = mdb.models['Model-1'].parts['Part-3']
        p.seedPart(size=sizemesh, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models['Model-1'].parts['Part-3']
        p.generateMesh()
        a = mdb.models['Model-1'].rootAssembly
        a.regenerate()

        ## Input File Generation
        mdb.Job(name='Cell', model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
            numCpus=1)
        mdb.jobs['Cell'].writeInput(consistencyChecking=OFF)
        #: The job input file has been written to "Job-1.inp".

        ###############################################################################################
    elif tipo == 'CFC':
        # Part Creation
        sime = float(meshsize)
        sizemesh = 6.4e-05/(sime)
        
        if fraction == '15':
            a = 1203.998e-6
        if fraction == '30':
            a = 955.614e-6
        if fraction == '45':
            a = 834.8056e-6
        
        executeOnCaeStartup()
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Spot(point=(0.0, 0.0))
        s.FixedConstraint(entity=v[0])
        s.rectangle(point1=(0.0, 0.0), point2=(15.0, 13.75))
        s.EqualLengthConstraint(entity1=g[5], entity2=g[4])
        s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(4.39339447021484, 
            -11.8999996185303), value=a)
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=a)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        del mdb.models['Model-1'].sketches['__profile__']
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        s1.FixedConstraint(entity=g[2])
        s1.Spot(point=(0.0, 0.0))
        s1.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
        s1.Line(point1=(17.5, 0.0), point2=(0.0, 0.0))
        s1.HorizontalConstraint(entity=g[3], addUndoState=False)
        s1.Line(point1=(0.0, 0.0), point2=(0.0, 15.7499961853027))
        s1.VerticalConstraint(entity=g[4], addUndoState=False)
        s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
        s1.CoincidentConstraint(entity1=v[4], entity2=g[2], addUndoState=False)
        s1.EqualLengthConstraint(entity1=g[4], entity2=g[3])
        s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 15.7499961853027), point2=(
            15.7499961853027, 0.0), direction=CLOCKWISE)
        s1.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(4.92061614990234, 
            -13.6499996185303), value=0.0005)
        p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-2']
        p.BaseSolidRevolve(sketch=s1, angle=90.0, flipRevolveDirection=OFF)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-2']
        del mdb.models['Model-1'].sketches['__profile__']

        ## Material Definition
        mdb.models['Model-1'].Material(name='Alumina')
        mdb.models['Model-1'].materials['Alumina'].Elastic(temperatureDependency=ON, 
            table=((326000000000.0, 0.24, 298.0), (309000000000.0, 0.24, 688.0), (
            302000000000.0, 0.24, 838.0)))
        mdb.models['Model-1'].materials['Alumina'].Expansion(table=((7.6e-06, ), ))
        
        if str(matrix) == 'G3':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((72.0e9, 0.23, 337.0), (69.2e9, 0.23, 549.0), (61.7e9, 0.23, 736.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((1.16e-05, ), ))
        if str(matrix) == 'G2':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((76.0e9, 0.21, 298.0), (76.0e9, 0.21, 549.0), (76.0e9, 0.21, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((7.4e-06, ), ))

        if str(matrix) == 'G1':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((68.0e9, 0.2, 298.0), (68.0e9, 0.2, 549.0), (68.0e9, 0.2, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((4.6e-06, ), ))
            
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
            material='Alumina', thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', 
            material='Glass', thickness=None)
        a = mdb.models['Model-1'].rootAssembly
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts['Part-1']
        a.Instance(name='Part-1-1', part=p, dependent=ON)
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-1', part=p, dependent=ON)
        p1 = a.instances['Part-2-1']
        p1.translate(vector=(0.00125399800000121, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-2', part=p, dependent=ON)
        p1 = a.instances['Part-2-2']
        p1.translate(vector=(0.00180399800000188, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-3', part=p, dependent=ON)
        p1 = a.instances['Part-2-3']
        p1.translate(vector=(0.00235399800000255, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        d11 = a.instances['Part-2-1'].datums
        e1 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=d11[1], fixedAxis=e1[7], flip=ON)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00524128, 
            farPlane=0.0101367, width=0.00399707, height=0.00138687, 
            viewOffsetX=4.94979e-005, viewOffsetY=-6.91218e-005)
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-1'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[4])
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances['Part-2-2'].edges
        e2 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=e1[0], fixedAxis=e2[10], flip=OFF)
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-2'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[0])
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances['Part-2-3'].edges
        e2 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=e1[1], fixedAxis=e2[8], flip=ON)
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-3'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[7])
        a = mdb.models['Model-1'].rootAssembly
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-4', part=p, dependent=ON)
        p = a.instances['Part-2-4']
        p.translate(vector=(0.00125399800000121, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        d1 = a.instances['Part-2-4'].datums
        e1 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=d1[1], fixedAxis=e1[2], flip=OFF)
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances['Part-2-4'].edges
        e2 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=e1[1], fixedAxis=e2[1], flip=ON)
        a = mdb.models['Model-1'].rootAssembly
        v1 = a.instances['Part-2-4'].vertices
        v2 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v1[1], fixedPoint=v2[2])
        #: The instance "Part-2-4" is fully constrained
        a = mdb.models['Model-1'].rootAssembly
        a.InstanceFromBooleanMerge(name='Part-3', instances=(a.instances['Part-1-1'], 
            a.instances['Part-2-1'], a.instances['Part-2-2'], a.instances['Part-2-3'], 
            a.instances['Part-2-4'], ), keepIntersections=ON, 
            originalInstances=SUPPRESS, domain=GEOMETRY)
        p = mdb.models['Model-1'].parts['Part-1']
        p = mdb.models['Model-1'].parts['Part-3']
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#f ]', ), )
        region = p.Set(cells=cells, name='Set-2')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        a = mdb.models['Model-1'].rootAssembly
        a.regenerate()
        a = mdb.models['Model-1'].rootAssembly

        mdb.Job(name='Cell', model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
            numCpus=1)
        p = mdb.models['Model-1'].parts['Part-3']
        p = mdb.models['Model-1'].parts['Part-3']

        ## Mesh Definition
        p.seedPart(size=sizemesh, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models['Model-1'].parts['Part-3']
        p.generateMesh()
        a = mdb.models['Model-1'].rootAssembly
        a.regenerate()
        a = mdb.models['Model-1'].rootAssembly
        a = mdb.models['Model-1'].rootAssembly
        mdb.jobs['Cell'].writeInput(consistencyChecking=OFF)
        #: The job input file has been written to "Cell.inp".
    if tipo == 'C':
        sime = float(meshsize)
        sizemesh = 9.6e-05/(2**sime)
        
        if fraction == '15':
            a = 758.47e-6
        if fraction == '30':
            a = 602e-6
        if fraction == '45':
            a = 525.895e-6

        executeOnCaeStartup()
        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Spot(point=(0.0, 0.0))
        s.FixedConstraint(entity=v[0])
        s.rectangle(point1=(0.0, 0.0), point2=(13.75, 12.5))
        s.EqualLengthConstraint(entity1=g[5], entity2=g[4])
        s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(5.62355804443359, 
            -7.70000076293945), value=a)
        p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=a)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-1']
        del mdb.models['Model-1'].sketches['__profile__']
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        s1.FixedConstraint(entity=g[2])
        s1.Spot(point=(0.0, 0.0))
        s1.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
        s1.FixedConstraint(entity=v[0])
        s1.Line(point1=(17.5, 0.0), point2=(0.0, 0.0))
        s1.HorizontalConstraint(entity=g[3], addUndoState=False)
        s1.Line(point1=(0.0, 0.0), point2=(0.0, 22.5749969482422))
        s1.VerticalConstraint(entity=g[4], addUndoState=False)
        s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
        s1.CoincidentConstraint(entity1=v[4], entity2=g[2], addUndoState=False)
        s1.EqualLengthConstraint(entity1=g[4], entity2=g[3])
        s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 22.5749969482422), point2=(
            22.5749969482422, 0.0), direction=CLOCKWISE)
        s1.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(12.4772567749023, 
            -13.6499977111816), value=0.0005)
        p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-2']
        p.BaseSolidRevolve(sketch=s1, angle=90.0, flipRevolveDirection=OFF)
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-2']
        del mdb.models['Model-1'].sketches['__profile__']
        
        if str(matrix) == 'G3':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((72.0e9, 0.23, 337.0), (69.2e9, 0.23, 549.0), (61.7e9, 0.23, 736.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((1.16e-05, ), ))
        if str(matrix) == 'G2':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((76.0e9, 0.21, 298.0), (76.0e9, 0.21, 549.0), (76.0e9, 0.21, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((7.4e-06, ), ))

        if str(matrix) == 'G1':
            mdb.models['Model-1'].Material(name='Glass')
            mdb.models['Model-1'].materials['Glass'].Elastic(temperatureDependency=ON, 
                table=((68.0e9, 0.2, 298.0), (68.0e9, 0.2, 549.0), (68.0e9, 0.2, 868.0)))
            mdb.models['Model-1'].materials['Glass'].Expansion(table=((4.6e-06, ), ))

        mdb.models['Model-1'].Material(name='Alumina')
        mdb.models['Model-1'].materials['Alumina'].Elastic(temperatureDependency=ON, 
            table=((326000000000.0, 0.24, 298.0), (309000000000.0, 0.24, 688.0), (
            302000000000.0, 0.24, 838.0)))
        mdb.models['Model-1'].materials['Alumina'].Expansion(table=((7.6e-06, ), ))
        
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
            material='Alumina', thickness=None)
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', 
            material='Glass', thickness=None)
        a = mdb.models['Model-1'].rootAssembly
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts['Part-1']
        a.Instance(name='Part-1-1', part=p, dependent=ON)
        p = mdb.models['Model-1'].parts['Part-2']
        a.Instance(name='Part-2-1', part=p, dependent=ON)
        p1 = a.instances['Part-2-1']
        p1.translate(vector=(0.000808470000000838, 0.0, 0.0))
        a = mdb.models['Model-1'].rootAssembly
        d11 = a.instances['Part-2-1'].datums
        e1 = a.instances['Part-1-1'].edges
        a.ParallelEdge(movableAxis=d11[1], fixedAxis=e1[7], flip=ON)
        a = mdb.models['Model-1'].rootAssembly
        v11 = a.instances['Part-2-1'].vertices
        v12 = a.instances['Part-1-1'].vertices
        a.CoincidentPoint(movablePoint=v11[1], fixedPoint=v12[4])
        a = mdb.models['Model-1'].rootAssembly
        a.InstanceFromBooleanMerge(name='Part-3', instances=(a.instances['Part-1-1'], 
            a.instances['Part-2-1'], ), keepIntersections=ON, 
            originalInstances=SUPPRESS, domain=GEOMETRY)
        p = mdb.models['Model-1'].parts['Part-2']
        p = mdb.models['Model-1'].parts['Part-3']
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models['Model-1'].parts['Part-3']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(cells=cells, name='Set-2')
        p = mdb.models['Model-1'].parts['Part-3']
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        p = mdb.models['Model-1'].parts['Part-3']
        ## Mesh
        p.seedPart(size=sizemesh, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models['Model-1'].parts['Part-3']
        p.generateMesh()
        a = mdb.models['Model-1'].rootAssembly
        a.regenerate()
        mdb.Job(name='Cell', model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
            numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
            numCpus=1)
        mdb.jobs['Cell'].writeInput(consistencyChecking=OFF)
        #: The job input file has been written to "Cell.inp".
