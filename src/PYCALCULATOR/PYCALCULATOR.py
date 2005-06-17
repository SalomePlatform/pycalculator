import PYCALCULATOR_ORB__POA
import SALOME_ComponentPy

import SALOME_MED
from libMEDMEM_Swig import *
from libMedCorba_Swig import *
from libMEDClient import *

class PYCALCULATOR (PYCALCULATOR_ORB__POA.PYCALCULATOR_Gen, SALOME_ComponentPy.SALOME_ComponentPy_i ):

    def __init__(self, orb, poa, contID, containerName, instanceName,
                 interfaceName):
        print "Begin of PYCALCULATOR::__init__"
        notif = 0
        SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa, 
	       contID, containerName, instanceName, interfaceName, notif)
	self._naming_service=SALOME_ComponentPy.SALOME_NamingServicePy_i(self._orb)
        self.clients = []
        print "End of PYCALCULATOR::__init__" 

    def Add(self, field1, field2):
        print "Begin of PYCALCULATOR::Add"
        print "pointeur on first argument : ",field1
        print "            second         : ",field2

        bool = 1
        nbOfComp1 = field1.getNumberOfComponents()
        name1 = field1.getName()
        description1 = field1.getDescription()

        nbOfComp2 = field2.getNumberOfComponents()
        name2 = field2.getName()
        description2 = field2.getDescription()

        if (nbOfComp1 != nbOfComp2): bool = 0

        compName = []
        compUnit = []
        for k in range(nbOfComp1):
            kp1 = k+1
            compName.append(field1.getComponentName(kp1))
            compUnit.append(field1.getComponentUnit(kp1))
            if (bool):
                if ((compName[k] != field2.getComponentName(kp1)) or (compUnit[k] != field2.getComponentUnit(kp1))):
                    bool = 0

        support1 = field1.getSupport()
        entity1 = support1.getEntity()
        mesh1 = support1.getMesh()

        support2 = field2.getSupport()
        entity2 = support2.getEntity()
        mesh2 = support2.getMesh()

        if (support1.isOnAllElements()):
            lengthValue1 = mesh1.getNumberOfElements(entity1,SALOME_MED.MED_ALL_ELEMENTS)
            number1 = []
            for k in range(lengthValue1):
                number1.append(k)
        else:
            lengthValue1 = support1.getNumberOfElements(SALOME_MED.MED_ALL_ELEMENTS)
            number1 = support1.getNumber(SALOME_MED.MED_ALL_ELEMENTS)

        if (support2.isOnAllElements()):
            lengthValue2 = mesh2.getNumberOfElements(entity2,SALOME_MED.MED_ALL_ELEMENTS)
            number2 = []
            for k in range(lengthValue2):
                number2.append(k)
        else:
            lengthValue2 = support2.getNumberOfElements(SALOME_MED.MED_ALL_ELEMENTS)
            number2 = support2.getNumber(SALOME_MED.MED_ALL_ELEMENTS)

        # comparision of each support: due to the fact that they are CORBA
        # pointers, the comparision will be done directly throught the numbers

        if (bool):
            if ((lengthValue1 != lengthValue2) or (entity1 != entity2)):
                bool = 0

        if (bool):
            for k in range(lengthValue1):
                if (number1[k] != number2[k]):
                    bool = 0

        value1 = field1.getValue(SALOME_MED.MED_FULL_INTERLACE)

        value2 = []
        if (bool):
            value2 = field2.getValue(SALOME_MED.MED_FULL_INTERLACE)

        valueOut = []
        if (bool):
            print "CALCULATORPY::Add : The fields have the same support, they then can be added"
            for k in range(lengthValue1*nbOfComp1):
                valueOut.append((value1[k]+value2[k]))
        else:
            print "CALCULATORPY::Add : WARNING !! For some reason the fields have not the same support"
            for k in range(lengthValue1*nbOfComp1):
                valueOut.append(value1[k])

        print "CALCULATORPY::Add : Creation of the local field, nbOfComp = ",nbOfComp1, " length = ",lengthValue1

        fieldOutLocal = createLocalFieldDouble(nbOfComp1,lengthValue1)
        fieldOutLocal.setValue(MED_FULL_INTERLACE,valueOut)
        fieldOutLocal.setName("-new_Add_Field-")
        fieldOutLocal.setDescription(description1)

        for k in range(nbOfComp1):
            kp1 = k + 1
            fieldOutLocal.setComponentName(kp1,compName[k])
            fieldOutLocal.setMEDComponentUnit(kp1,compUnit[k])

        supportClient = SUPPORTClient(support1)
        self.clients.append( supportClient )
        fieldOutLocal.setSupport( supportClient )

        print "CALCULATORPY::Add : Creation of the CORBA field"

        fieldOutCorba = createCorbaFieldDouble(support1,fieldOutLocal)

        print "End of CALCULATORPY::Add"
        return fieldOutCorba

    def Mul(self, field1, x1):
        print "Begin of CALCULATORPY::Mul"
        print "pointeur on first argument : ",field1
        print "            second         : ",x1

        nbOfComp = field1.getNumberOfComponents()
        name = field1.getName()
        description = field1.getDescription()
        support = field1.getSupport()
        print ".... get Names and Unit"
        compName = []
        compUnit = []
        for k in range(nbOfComp):
            kp1 = k+1
            compName.append(field1.getComponentName(kp1))
            compUnit.append(field1.getComponentUnit(kp1))


        print ".... get mesh"
        mesh = support.getMesh()

        if (support.isOnAllElements()):
            lengthValue = mesh.getNumberOfElements(support.getEntity(),SALOME_MED.MED_ALL_ELEMENTS)
        else:
            lengthValue = support.getNumberOfElements(SALOME_MED.MED_ALL_ELEMENTS)

        value1 = field1.getValue(SALOME_MED.MED_FULL_INTERLACE)
        valueOut = []
        for k in range(lengthValue*nbOfComp):
            valueOut.append(x1*value1[k])

        print "CALCULATORPY::Mul : Creation of the local field, nbOfComp = ",nbOfComp, " length = ",lengthValue

        fieldOutLocal = createLocalFieldDouble(nbOfComp,lengthValue)
        fieldOutLocal.setValue(MED_FULL_INTERLACE,valueOut)
        fieldOutLocal.setName("-new_Mul_Field-")
        fieldOutLocal.setDescription(description)

        for k in range(nbOfComp):
            kp1 = k + 1
            fieldOutLocal.setComponentName(kp1,compName[k])
            fieldOutLocal.setMEDComponentUnit(kp1,compUnit[k])

        supportClient = SUPPORTClient(support)
        self.clients.append( supportClient )
        fieldOutLocal.setSupport( supportClient )

        print "CALCULATORPY::Mul : Creation of the CORBA field"

        fieldOutCorba = createCorbaFieldDouble(support,fieldOutLocal)

        print "End of CALCULATORPY::Mul"
        return fieldOutCorba

    def Constant(self, field1, x1):
        print "Begin of CALCULATORPY::Constant"
        print "pointeur on first argument : ",field1
        print "            second         : ",x1

        nbOfComp = field1.getNumberOfComponents()
        name = field1.getName()
        description = field1.getDescription()
        support = field1.getSupport()
        compName = []
        compUnit = []
        for k in range(nbOfComp):
            kp1 = k+1
            compName.append(field1.getComponentName(kp1))
            compUnit.append(field1.getComponentUnit(kp1))

        mesh = support.getMesh()

        if (support.isOnAllElements()):
            lengthValue = mesh.getNumberOfElements(support.getEntity(),SALOME_MED.MED_ALL_ELEMENTS)
        else:
            lengthValue = support.getNumberOfElements(SALOME_MED.MED_ALL_ELEMENTS)

        valueOut = []
        for k in range(lengthValue*nbOfComp):
            valueOut.append(x1)

        print "CALCULATORPY::Constant : Creation of the local field, nbOfComp = ",nbOfComp, " length = ",lengthValue

        fieldOutLocal = createLocalFieldDouble(nbOfComp,lengthValue)
        fieldOutLocal.setValue(MED_FULL_INTERLACE,valueOut)
        fieldOutLocal.setName("-new_Const_Field-")
        fieldOutLocal.setDescription(description)

        for k in range(nbOfComp):
            kp1 = k + 1
            fieldOutLocal.setComponentName(kp1,compName[k])
            fieldOutLocal.setMEDComponentUnit(kp1,compUnit[k])

        supportClient = SUPPORTClient(support)
        self.clients.append( supportClient )
        fieldOutLocal.setSupport( supportClient )

        print "CALCULATORPY::Constant : Creation of the CORBA field"

        fieldOutCorba = createCorbaFieldDouble(support,fieldOutLocal)

        print "End of CALCULATORPY::Constant"
        return fieldOutCorba

    def writeMEDfile(self, field1, fileName):
        print "Begin of CALCULATORPY::writeMEDfile"
        print "CALCULATORPY::writeMEDfile : pointeur on first argument : ",field1
        print "                          second         : ",fileName
        print "CALCULATORPY::writeMEDfile : NOT YET IMPLEMENTED"
        print "End of CALCULATORPY::writeMEDfile"
