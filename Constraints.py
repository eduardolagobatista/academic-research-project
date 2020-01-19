from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
def constr(arq):
    executeOnCaeStartup()
    #O modelo a ser usado deve estar na pasta abaqus/modelos
    ## Escreva o nome do arquivo .cae
    ##
    arquivo = "C:/Users/duhju/Desktop/abaqus/modelos/" + arq + ".cae"
    mdb.openAuxMdb(pathName=arquivo)
    mdb.copyAuxMdbModel(fromName='Cell', toName='Cell')
    mdb.closeAuxMdb()
    p1 = mdb.models['Cell'].parts['Cell']
    a = mdb.models['Cell'].rootAssembly
    p = mdb.models['Cell'].parts['Cell']
    a = mdb.models['Cell'].rootAssembly
    #a = mdb.models['Model-1'].rootAssembly
    #del mdb.models['Model-1']
    a = mdb.models['Cell'].rootAssembly


    ############################# Reference Points / Sets ###########################
    a.ReferencePoint(point=(0.0015, 0.0005, 0.0))
    a.ReferencePoint(point=(0.0015, 0.0, 0.0))
    #a.ReferencePoint(point=(0.0015, -0.0005, 0.0))
    r1 = a.referencePoints
    refPoints1=(r1[20], )
    a.Set(referencePoints=refPoints1, name='Set-rp1')
    #: The set 'Set-rp1' has been created (1 reference point).
    #refPoints1=(r1[22], )
    #a.Set(referencePoints=refPoints1, name='Set-rp3')
    #: The set 'Set-rp3' has been created (1 reference point).
    r1 = a.referencePoints
    refPoints1=(r1[21], )
    a.Set(referencePoints=refPoints1, name='Set-rp2')
    #: The set 'Set-rp2' has been created (1 reference point).


    #####################################################################################################################
    ############################## Geometry Limits ######################################################################
    p = mdb.models['Cell'].parts['Cell']
    #xmin, xmax, ymin, ymax, zmin, zmax = -4.7781e-04, 4.7781e-04, -4.7781e-04, 4.7781e-04, 0, 0.000955615

    nnodes = len(p.nodes)

    xmin, ymin, zmin, xmax, ymax, zmax = 0, 0, 0, 0, 0, 0
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if (x < xmin):
            xmin = x
        if (y < ymin):
            ymin = y
        if (z < zmin):
            zmin = z
        if(x > xmax):
            xmax = x
        if(y > ymax):
            ymax = y
        if(z > zmax):
            zmax = z

    ########################################################################################################################
    p = mdb.models['Cell'].parts['Cell']
    qsi = 0.00000001
    nnodes = len(p.nodes)
    n=1
        ########################################### Sets Creation #############################################################

              
        ##############3 Middle Point
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if (x == 0.0 and y == 0.0 and z == 0.0):
            center_node = p.nodes[k:k+1]
            p.Set(nodes=center_node, name='center_node')



    ########################################## Boundary Conditions #####################################################
    a = mdb.models['Cell'].rootAssembly
    a.regenerate()
    region = a.instances['Cell-1'].sets['center_node']

    # Setar quais os deslocamentos e rotacoes serao restringidos no center point!!!!
    mdb.models['Cell'].DisplacementBC(name='BC-1', createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

    # Setar quais os deslocamentos e rotacoes serao aplicados nos Reference Points!!!!
    ##### RP 1
    region = a.sets['Set-rp1']
    mdb.models['Cell'].DisplacementBC(name='BC-rp1', createStepName='Step-1', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

    ##### RP 2
    region = a.sets['Set-rp2']
    mdb.models['Cell'].DisplacementBC(name='BC-rp2', createStepName='Step-1', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

    ##### RP 3
    #region = a.sets['Set-rp3']
    #mdb.models['Cell'].DisplacementBC(name='BC-rp3', createStepName='Step-1', region=region, u1=UNSET, u2=UNSET, u3=1e-07, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)


    ## Determinar se alguma BC sera suprimida ou se sera aplicada aos dois RP's
    ####################
    #mdb.models['Cell'].boundaryConditions['BC-2'].suppress()
    ####################



    ##################### Cantos


    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if (((x>xmin-qsi)and(x<xmin+qsi))or((x>xmax-qsi)and(x<xmax+qsi)))and(((y>ymin-qsi)and(y<ymin+qsi))or((y>ymax-qsi)and(y<ymax+qsi)))and(((z>zmin-qsi)and(z<zmin+qsi))or((z>zmax-qsi)and(z<zmax+qsi))):
            if (((x>xmin-qsi)and(x<xmin+qsi))and((y>ymin-qsi)and(y<ymin+qsi))and((z>zmin-qsi)and(z<zmin+qsi))):
                corner_a = p.nodes[k:k+1]
                p.Set(nodes=corner_a, name='a_corner')
            if (((x>xmin-qsi)and(x<xmin+qsi))and((y>ymin-qsi)and(y<ymin+qsi))and((z>zmax-qsi)and(z<zmax+qsi))):
                corner_e = p.nodes[k:k+1]
                p.Set(nodes=corner_e, name='e_corner')
            if (((x>xmin-qsi)and(x<xmin+qsi))and((y>ymax-qsi)and(y<ymax+qsi))and((z>zmin-qsi)and(z<zmin+qsi))):
                corner_b = p.nodes[k:k+1]
                p.Set(nodes=corner_b, name='b_corner')
            if (((x>xmin-qsi)and(x<xmin+qsi))and((y>ymax-qsi)and(y<ymax+qsi))and((z>zmax-qsi)and(z<zmax+qsi))):
                corner_f = p.nodes[k:k+1]
                p.Set(nodes=corner_f, name='f_corner')
            if (((x>xmax-qsi)and(x<xmax+qsi))and((y>ymin-qsi)and(y<ymin+qsi))and((z>zmin-qsi)and(z<zmin+qsi))):
                corner_d = p.nodes[k:k+1]
                p.Set(nodes=corner_d, name='d_corner')
            if (((x>xmax-qsi)and(x<xmax+qsi))and((y>ymin-qsi)and(y<ymin+qsi))and((z>zmax-qsi)and(z<zmax+qsi))):
                corner_h = p.nodes[k:k+1]
                p.Set(nodes=corner_h, name='h_corner')
            if (((x>xmax-qsi)and(x<xmax+qsi))and((y>ymax-qsi)and(y<ymax+qsi))and((z>zmin-qsi)and(z<zmin+qsi))):
                corner_c = p.nodes[k:k+1]
                p.Set(nodes=corner_c, name='c_corner')
            if (((x>xmax-qsi)and(x<xmax+qsi))and((y>ymax-qsi)and(y<ymax+qsi))and((z>zmax-qsi)and(z<zmax+qsi))):
                corner_g = p.nodes[k:k+1]
                p.Set(nodes=corner_g, name='g_corner')
            

    mdb.models['Cell'].Equation(name='A_G_eq_1', terms=((-1.0, 'Cell-1.a_corner', 1), (1.0, 'Cell-1.g_corner', 1), (-1.0, 'Set-rp1', 1), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 2)))
    mdb.models['Cell'].Equation(name='A_G_eq_2', terms=((-1.0, 'Cell-1.a_corner', 2), (1.0, 'Cell-1.g_corner', 2), (-1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 3)))
    mdb.models['Cell'].Equation(name='A_G_eq_3', terms=((-1.0, 'Cell-1.a_corner', 3), (1.0, 'Cell-1.g_corner', 3), (-1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 2), (-1.0, 'Set-rp2', 3)))

        
    mdb.models['Cell'].Equation(name='B_H_eq_1', terms=((-1.0, 'Cell-1.b_corner', 1), (1.0, 'Cell-1.h_corner', 1), (-1.0, 'Set-rp1', 1), (1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 2)))
    mdb.models['Cell'].Equation(name='B_H_eq_2', terms=((-1.0, 'Cell-1.b_corner', 2), (1.0, 'Cell-1.h_corner', 2), (1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 3)))
    mdb.models['Cell'].Equation(name='B_H_eq_3', terms=((-1.0, 'Cell-1.b_corner', 3), (1.0, 'Cell-1.h_corner', 3), (-1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 2), (1.0, 'Set-rp2', 3)))

        
    mdb.models['Cell'].Equation(name='F_D_eq_1', terms=((1.0, 'Cell-1.f_corner', 1), (-1.0, 'Cell-1.d_corner', 1), (1.0, 'Set-rp1', 1), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 2)))
    mdb.models['Cell'].Equation(name='F_D_eq_2', terms=((1.0, 'Cell-1.f_corner', 2), (-1.0, 'Cell-1.d_corner', 2), (-1.0, 'Set-rp1', 2), (1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 3)))
    mdb.models['Cell'].Equation(name='F_D_eq_3', terms=((1.0, 'Cell-1.f_corner', 3), (-1.0, 'Cell-1.d_corner', 3), (-1.0, 'Set-rp1', 3), (1.0, 'Set-rp2', 2), (-1.0, 'Set-rp2', 3)))

        
    mdb.models['Cell'].Equation(name='E_C_eq_1', terms=((-1.0, 'Cell-1.e_corner', 1), (1.0, 'Cell-1.c_corner', 1), (-1.0, 'Set-rp1', 1), (-1.0, 'Set-rp2', 1), (1.0, 'Set-rp2', 2)))
    mdb.models['Cell'].Equation(name='E_C_eq_2', terms=((-1.0, 'Cell-1.e_corner', 2), (1.0, 'Cell-1.c_corner', 2), (-1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 1), (1.0, 'Set-rp2', 3)))
    mdb.models['Cell'].Equation(name='E_C_eq_3', terms=((-1.0, 'Cell-1.e_corner', 3), (1.0, 'Cell-1.c_corner', 3), (1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 2), (-1.0, 'Set-rp2', 3)))
                          
    mdb.saveAs(pathName=arquivo)


    ################## Arestas

    ab = []
    hg = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((x > xmin-qsi) and (x < xmin+qsi)) and ((z > zmin-qsi) and (z < zmin+qsi)) and ((y > ymin+qsi)and(y < ymax-qsi)):
            ab.append(k)
        elif ((x> xmax-qsi) and (x < xmax+qsi)) and ((z < zmax+qsi)and(z > zmax-qsi)) and ((y > ymin+qsi)and(y < ymax-qsi)):
            hg.append(k)

    for k in ab:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in hg:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((y1 > y-qsi)and(y1 < y+qsi)):
                AB = p.nodes[k:k+1]
                HG = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'AB_HG_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'AB_HG_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'AB_HG_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=AB, name=name_set1)
                p.Set(nodes=HG, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((-1.0, constraint1, 1), (1.0, constraint2, 1), (-1.0, 'Set-rp1', 1), (-1.0, 'Set-rp2', 2)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((-1.0, constraint1, 2), (1.0, constraint2, 2), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 3)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((-1.0, constraint1, 3), (1.0, constraint2, 3), (-1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 2)))
                hg.remove(j)
                break
            
    dc = []
    ef = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((x > xmin-qsi) and (x < xmin+qsi)) and ((z > zmax-qsi) and (z < zmax+qsi)) and ((y > ymin+qsi)and(y < ymax-qsi)):
            ef.append(k)
        elif ((x > xmax-qsi) and (x < xmax+qsi)) and ((z < zmin+qsi)and(z > zmin-qsi)) and ((y > ymin+qsi)and(y < ymax-qsi)):
            dc.append(k)

    for k in dc:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in ef:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((y1 > y-qsi)and(y1 < y+qsi)):
                DC = p.nodes[k:k+1]
                EF = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'DC_EF_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'DC_EF_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'DC_EF_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=DC, name=name_set1)
                p.Set(nodes=EF, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((1.0, constraint1, 1), (-1.0, constraint2, 1), (-1.0, 'Set-rp1', 1), (1.0, 'Set-rp2', 2)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((1.0, constraint1, 2), (-1.0, constraint2, 2), (-1.0, 'Set-rp2', 1), (1.0, 'Set-rp2', 3)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((1.0, constraint1, 3), (-1.0, constraint2, 3), (1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 2)))
                ef.remove(j)
                break

    eh = []
    bc = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((y > ymin-qsi) and (y < ymin+qsi)) and ((z > zmax-qsi) and (z < zmax+qsi)) and ((x > xmin+qsi)and(x < xmax-qsi)):
            eh.append(k)
        elif ((y > ymax-qsi) and (y < ymax+qsi)) and ((z < zmin+qsi)and(z > zmin-qsi)) and ((x > xmin+qsi)and(x < xmax-qsi)):
            bc.append(k)

    for k in bc:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in eh:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((x1 > x-qsi)and(x1 < x+qsi)):
                BC = p.nodes[k:k+1]
                EH = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'BC_EH_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'BC_EH_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'BC_EH_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=BC, name=name_set1)
                p.Set(nodes=EH, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((1.0, constraint1, 1), (-1.0, constraint2, 1), (-1.0, 'Set-rp2', 1), (1.0, 'Set-rp2', 2)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((1.0, constraint1, 2), (-1.0, constraint2, 2), (-1.0, 'Set-rp1', 2), (1.0, 'Set-rp2', 3)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((1.0, constraint1, 3), (-1.0, constraint2, 3), (1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 3)))
                eh.remove(j)
                break

    fg = []
    ad = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((y > ymax-qsi) and (y < ymax+qsi)) and ((z > zmax-qsi) and (z < zmax+qsi)) and ((x > xmin+qsi)and(x < xmax-qsi)):
            fg.append(k)
        elif ((y > ymin-qsi) and (y < ymin+qsi)) and ((z < zmin+qsi)and(z > zmin-qsi)) and ((x > xmin+qsi)and(x < xmax-qsi)):
            ad.append(k)

    for k in fg:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in ad:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((x1 > x-qsi)and(x1 < x+qsi)):
                FG = p.nodes[k:k+1]
                AD = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'FG_AD_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'FG_AD_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'FG_AD_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=FG, name=name_set1)
                p.Set(nodes=AD, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((1.0, constraint1, 1), (-1.0, constraint2, 1), (-1.0, 'Set-rp2', 1), (-1.0, 'Set-rp2', 2)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((1.0, constraint1, 2), (-1.0, constraint2, 2), (-1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 3)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((1.0, constraint1, 3), (-1.0, constraint2, 3), (-1.0, 'Set-rp1', 3), (-1.0, 'Set-rp2', 3)))
                ad.remove(j)
                break
            
    ae = []
    cg = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((x > xmin-qsi) and (x < xmin+qsi)) and ((y > ymin-qsi) and (y < ymin+qsi)) and ((z > zmin+qsi)and(z < zmax-qsi)):
            ae.append(k)
        elif ((x > xmax-qsi) and (x < xmax+qsi)) and ((y < ymax+qsi)and(y > ymax-qsi)) and ((z > zmin+qsi)and(z < zmax-qsi)):
            cg.append(k)

    for k in cg:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in ae:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((z1 > z-qsi)and(z1 < z+qsi)):
                CG = p.nodes[k:k+1]
                AE = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'CG_AE_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'CG_AE_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'CG_AE_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=CG, name=name_set1)
                p.Set(nodes=AE, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((1.0, constraint1, 1), (-1.0, constraint2, 1), (-1.0, 'Set-rp1', 1), (-1.0, 'Set-rp2', 1)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((1.0, constraint1, 2), (-1.0, constraint2, 2), (-1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 1)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((1.0, constraint1, 3), (-1.0, constraint2, 3), (-1.0, 'Set-rp2', 2), (-1.0, 'Set-rp2', 3)))
                ae.remove(j)
                break

    bf =[]
    dh =[]
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((x > xmin-qsi) and (x < xmin+qsi)) and ((y > ymax-qsi) and (y < ymax+qsi)) and ((z > zmin+qsi)and(z < zmax-qsi)):
            bf.append(k)
        elif ((x > xmax-qsi) and (x < xmax+qsi)) and ((y < ymin+qsi)and(y > ymin-qsi)) and ((z > zmin+qsi)and(z < zmax-qsi)):
            dh.append(k)

    for k in dh:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in bf:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((z1 > z-qsi)and(z1 < z+qsi)):
                DH = p.nodes[k:k+1]
                BF = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'DH_BF_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'DH_BF_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'DH_BF_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=DH, name=name_set1)
                p.Set(nodes=BF, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((1.0, constraint1, 1), (-1.0, constraint2, 1), (-1.0, 'Set-rp1', 1), (1.0, 'Set-rp2', 1)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((1.0, constraint1, 2), (-1.0, constraint2, 2), (1.0, 'Set-rp1', 2), (-1.0, 'Set-rp2', 1)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((1.0, constraint1, 3), (-1.0, constraint2, 3), (-1.0, 'Set-rp2', 2), (1.0, 'Set-rp2', 3)))
                bf.remove(j)
                break
            
    mdb.saveAs(pathName=arquivo)            

    ################################3 Faces

    abfe = []
    dcgh = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((x > xmin-qsi) and (x < xmin+qsi)) and ((y > ymin+qsi) and (y < ymax-qsi)) and ((z > zmin+qsi) and (z < zmax-qsi)):
            abfe.append(k)
        elif ((x > xmax-qsi) and (x < xmax+qsi)) and ((y > ymin+qsi) and (y < ymax-qsi)) and ((z > zmin+qsi) and (z < zmax-qsi)):
            dcgh.append(k)

    for k in abfe:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in dcgh:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((y1 > y-qsi) and (y1 < y+qsi)) and ((z1 > z-qsi) and (z1 < z+qsi)):
                ABFE = p.nodes[k:k+1]
                DCGH = p.nodes[j:j+1]
                name_set1 = 'set_node_' + str(k)
                name_set2 = 'set_node_' + str(j)
                constraint1 = 'Cell-1.' + name_set1
                constraint2 = 'Cell-1.' + name_set2
                eq_name1 = 'ABFE_DCGH_eq_' + str(k) + '_' + str(j) + '_1'
                eq_name2 = 'ABFE_DCGH_eq_' + str(k) + '_' + str(j) + '_2'
                eq_name3 = 'ABFE_DCGH_eq_' + str(k) + '_' + str(j) + '_3'
                p.Set(nodes=ABFE, name=name_set1)
                p.Set(nodes=DCGH, name=name_set2)
                mdb.models['Cell'].Equation(name=eq_name1, terms=((-1.0, constraint1, 1), (1.0, constraint2, 1), (-1.0, 'Set-rp1', 1)))
                mdb.models['Cell'].Equation(name=eq_name2, terms=((-1.0, constraint1, 2), (1.0, constraint2, 2), (-1.0, 'Set-rp2', 1)))
                mdb.models['Cell'].Equation(name=eq_name3, terms=((-1.0, constraint1, 3), (1.0, constraint2, 3), (-1.0, 'Set-rp2', 2)))
                dcgh.remove(j)
                break



    aehd = []
    bfgc = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((y > ymin-qsi) and (y < ymin+qsi)) and ((x > xmin+qsi) and (x < xmax-qsi)) and ((z > zmin+qsi) and (z < zmax-qsi)):
            aehd.append(k)
        elif ((y > ymax-qsi) and (y < ymax+qsi)) and ((x > xmin+qsi) and (x < xmax-qsi)) and ((z > zmin+qsi) and (z < zmax-qsi)):
            bfgc.append(k)

    for k in aehd:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in bfgc:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((x1 > x-qsi) and (x1 < x+qsi)):
                if ((z1 > z-qsi) and (z1 < z+qsi)):
                    AEHD = p.nodes[k:k+1]
                    BFGC = p.nodes[j:j+1]
                    name_set1 = 'set_node_' + str(k)
                    name_set2 = 'set_node_' + str(j)
                    constraint1 = 'Cell-1.' + name_set1
                    constraint2 = 'Cell-1.' + name_set2
                    eq_name1 = 'AEHD_BFGC_eq_' + str(k) + '_' + str(j) + '_1'
                    eq_name2 = 'AEHD_BFGC_eq_' + str(k) + '_' + str(j) + '_2'
                    eq_name3 = 'AEHD_BFGC_eq_' + str(k) + '_' + str(j) + '_3'
                    p.Set(nodes=AEHD, name=name_set1)
                    p.Set(nodes=BFGC, name=name_set2)
                    mdb.models['Cell'].Equation(name=eq_name1, terms=((-1.0, constraint1, 1), (1.0, constraint2, 1), (-1.0, 'Set-rp2', 1)))
                    mdb.models['Cell'].Equation(name=eq_name2, terms=((-1.0, constraint1, 2), (1.0, constraint2, 2), (-1.0, 'Set-rp1', 2)))
                    mdb.models['Cell'].Equation(name=eq_name3, terms=((-1.0, constraint1, 3), (1.0, constraint2, 3), (-1.0, 'Set-rp2', 3)))
                    bfgc.remove(j)
                    break

    abcd = []
    efgh = []
    for k in range(nnodes):
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        if ((z > zmin-qsi) and (z < zmin+qsi)) and ((x > xmin+qsi) and (x < xmax-qsi)) and ((y > ymin+qsi) and (y < ymax-qsi)):
            abcd.append(k)
        elif ((z > zmax-qsi) and (z < zmax+qsi)) and ((x > xmin+qsi) and (x < xmax-qsi)) and ((y > ymin+qsi) and (y < ymax-qsi)):
            efgh.append(k)

    for k in abcd:
        x, y, z = p.nodes[k].coordinates[0], p.nodes[k].coordinates[1], p.nodes[k].coordinates[2]
        for j in efgh:
            x1, y1, z1 = p.nodes[j].coordinates[0], p.nodes[j].coordinates[1], p.nodes[j].coordinates[2]
            if ((x1 > x-qsi) and (x1 < x+qsi)):
                if ((y1 > y-qsi) and (y1 < y+qsi)):
                    ABCD = p.nodes[k:k+1]
                    EFGH = p.nodes[j:j+1]
                    name_set1 = 'set_node_' + str(k)
                    name_set2 = 'set_node_' + str(j)
                    constraint1 = 'Cell-1.' + name_set1
                    constraint2 = 'Cell-1.' + name_set2
                    eq_name1 = 'ABCD_EFGH_eq_' + str(k) + '_' + str(j) + '_1'
                    eq_name2 = 'ABCD_EFGH_eq_' + str(k) + '_' + str(j) + '_2'
                    eq_name3 = 'ABCD_EFGH_eq_' + str(k) + '_' + str(j) + '_3'
                    p.Set(nodes=ABCD, name=name_set1)
                    p.Set(nodes=EFGH, name=name_set2)
                    mdb.models['Cell'].Equation(name=eq_name1, terms=((-1.0, constraint1, 1), (1.0, constraint2, 1), (-1.0, 'Set-rp2', 2)))
                    mdb.models['Cell'].Equation(name=eq_name2, terms=((-1.0, constraint1, 2), (1.0, constraint2, 2), (-1.0, 'Set-rp2', 3)))
                    mdb.models['Cell'].Equation(name=eq_name3, terms=((-1.0, constraint1, 3), (1.0, constraint2, 3), (-1.0, 'Set-rp1', 3)))
                    efgh.remove(j)
                    break
                              
    mdb.saveAs(pathName=arquivo)



