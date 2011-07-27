#  Copyright (C) 2007-2011  CEA/DEN, EDF R&D, OPEN CASCADE
#
#  Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
#  CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import salome
import SALOME
import SALOME_MED
import PYCALCULATOR_ORB
import os

#==============================================================================

def AnalyzeField(field):
    name = field.getName()
    desc = field.getDescription()
    nbComp = field.getNumberOfComponents()
    itNum = field.getIterationNumber()
    ordNum = field.getOrderNumber()

    print "Analysis of the field ",name," with the description ",desc
    print "iteration number ",itNum," order Number ",ordNum
    print "It has ",nbComp," component(s)"

    fieldValue = field.getValue(SALOME_MED.MED_FULL_INTERLACE)
    fieldSupport = field.getSupport()
    fieldMesh = fieldSupport.getMesh()
    fieldEntity = fieldSupport.getEntity()
    bool = fieldSupport.isOnAllElements()

    if bool:
        print "The support of this field is on all entities ",fieldEntity," of the mesh ",fieldMesh.getName()
        if fieldEntity == SALOME_MED.MED_NODE:
            nbValByComp = fieldMesh.getNumberOfNodes()
        else:
            nbValByComp = fieldMesh.getNumberOfElements(fieldEntity,SALOME_MED.MED_ALL_ELEMENTS)
        print "and its dimension (number of values by component of the field) is ",nbValByComp
    else:
        print "The support of this field is partially on entities ",fieldEntity," of the mesh ",fieldMesh.getName()
        nbValByComp = fieldSupport.getNumberOfElements(SALOME_MED.MED_ALL_ELEMENTS)
        print "and its dimension (number of values by component of the field) is ",nbValByComp

    for i in range(nbComp):
        compName = field.getComponentName(i+1)
        compUnit = field.getComponentUnit(i+1)
        print "The ",(i+1),"-th  component ",compName," with the unit ",compUnit

    for i in range(nbValByComp):
        print "  * ",fieldValue[i*nbComp:(i+1)*nbComp]

#==============================================================================

def getFieldIntObjectFromStudy(number,subnumber):
    mySO = salome.myStudy.FindObject("MEDFIELD")
    mysub = mySO.FindSubObject(number)[1]
    if mysub:
        mysubsub = mysub.FindSubObject(subnumber)[1]
        if mysubsub:
            Builder = salome.myStudy.NewBuilder()
            anAttr = Builder.FindOrCreateAttribute(mysubsub, "AttributeIOR")
            obj = salome.orb.string_to_object(anAttr.Value())
            myObj = obj._narrow(SALOME_MED.FIELDINT)
            return myObj
        else:
            print "ERROR: No FieldInt Object stored in this Study"
            return None
    else:
        print "ERROR: No FieldInt Object stored in this Study"
        return None

#==============================================================================

def getFieldDoubleObjectFromStudy(number,subnumber):
    mySO = salome.myStudy.FindObject("MEDFIELD")
    mysub = mySO.FindSubObject(number)[1]
    if mysub:
        mysubsub = mysub.FindSubObject(subnumber)[1]
        if mysubsub:
            Builder = salome.myStudy.NewBuilder()
            anAttr = Builder.FindOrCreateAttribute(mysubsub, "AttributeIOR")
            obj = salome.orb.string_to_object(anAttr.Value())
            myObj = obj._narrow(SALOME_MED.FIELDDOUBLE)
            return myObj
        else:
            print "ERROR: No FieldDouble Object stored in this Study"
            return None
    else:
        print "ERROR: No FieldDouble Object stored in this Study"
        return None

#==============================================================================

studyname = salome.myStudyName
studynameId = salome.myStudyId

print "We are working in the study ",studyname," with the ID ",studynameId
print ""

filePath=os.environ["MED_ROOT_DIR"]
filePath=filePath+"/share/salome/resources/med/"
medFile=filePath+"pointe.med"
fieldname = "fieldcelldouble"

print "Load the Med Component "
med_comp = salome.lcc.FindOrLoadComponent("FactoryServer", "MED")

try:
    fieldcell  = med_comp.readFieldInFile(medFile,studyname,fieldname,-1,-1)
except SALOME.SALOME_Exception, ex:
    print ex.details
    print ex.details.type
    print ex.details.text
    print ex.details.sourceFile
    print ex.details.lineNumber
    raise

print fieldcell
print fieldcell.getName()
print fieldcell.getDescription()
print fieldcell.getNumberOfComponents()


AnalyzeField(fieldcell)



print "Loading of the CalculatorPy Component "
calculator = salome.lcc.FindOrLoadComponent("FactoryServerPy", "PYCALCULATOR")
print "calculator = "
dir(calculator)

alpha = 2.0
print "Multiplication of fieldcelldouble by alpha"
fieldcellalpha = calculator.Mul(fieldcell,alpha)
print fieldcellalpha
AnalyzeField(fieldcellalpha)

print "Adding of alpha*fieldcelldouble and fieldcelldouble"
fieldcelladd = calculator.Add(fieldcell,fieldcellalpha)
print fieldcelladd
AnalyzeField(fieldcelladd)

print "Put fieldcelladd in study"
fieldcelladd.addInStudy(salome.myStudy,fieldcelladd)

print "update Salome GUI"
salome.sg.updateObjBrowser(1)

print "Get back Field from study"
# we grab the second field in MEDFIELD - first iteration
fieldcelldouble = getFieldDoubleObjectFromStudy(2,1)
print fieldcelldouble
AnalyzeField(fieldcelldouble)


print "Fin du test PYCALCULATOR"
