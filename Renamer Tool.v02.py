''' 
Navin Kamal
Renamer Tool.v02
Free Licence
Dont forget to give credit :)
'''

import maya.cmds as cmds
import string as st

class NvN_Window():
    #constructor
    def __init__(self):
        self.window = "renamerWindow"
        self.title = "NvN Tools"
        self.size = (400, 600)
        # close old window is open
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
        if cmds.windowPref(self.window, q=True, ex=True):
            cmds.windowPref(self.window, r=True)
        #create new window
        self.window = cmds.window(self.window, title=self.title, w=400, h=500)
        self.masterLayout = cmds.columnLayout(adjustableColumn = False, w=400, h=500)
        cmds.text(label = "RenamerTool.v02", h = 30 ,w=400,fn="boldLabelFont", bgc=(0.188, 0.627, 0.627))
        cmds.separator(height=10,w=400 , style= 'none')
        #Replace With:
        cmds.rowColumnLayout(numberOfColumns=2,h=50,columnWidth = [(1,120),(2,300)])
        cmds.text(label="Search For: >")
        self.searchFor = cmds.textFieldGrp("searchWithName", editable=True)
        cmds.text(label="Replace With: >")
        self.replaceWith = cmds.textFieldGrp("replaceWithName" , editable=True )
        cmds.setParent(self.masterLayout)
        cmds.separator(height=5,w=400, style= 'none' )       
        #Radio Buttons
        cmds.rowLayout( numberOfColumns=4 , h=40,columnWidth = [(1,10),(2,150),(3,160),(4,80)])
        cmds.radioCollection()
        cmds.text(l="")
        cmds.radioButton("selectedRadioBTNname", label = "Selected",  )
        cmds.radioButton("hierarchyRadioBTNname", label = "Hierarchy" ,select = True )
        cmds.radioButton("allRadioBTNname", label = "All" )
        cmds.setParent(self.masterLayout)
        cmds.separator(height=10,w=400 )
        self.searchForBtn = cmds.button(label='Go',h=30,w=400,command=self.selection)
        cmds.separator(height=10 )
        #Suffix and Prefix section
        cmds.rowColumnLayout(numberOfColumns=2,h=60,columnWidth = [(1,120),(2,230)])
        cmds.button(label="Prefix_",width = 100, command = self.prefix)
        cmds.textField("prefixName",w = 200,editable=True)
        cmds.button(label="_Suffix",width = 100, command = self.suffix)
        cmds.textField("suffixName",w = 200,editable=True)            
        cmds.setParent(self.masterLayout)        
        cmds.separator(height=20,w=400)

        #Renamer (Selection Hierarchy)
        cmds.rowColumnLayout(numberOfColumns=4,h=30,columnWidth = [(1,100),(2,80),(3,120),(4,80)])
        cmds.text(label='ChooseSide: >')
        cmds.optionMenu("sideOption")
        cmds.menuItem(label = "None")
        cmds.menuItem(label = "Mid")
        cmds.menuItem(label = "Left")
        cmds.menuItem(label = "Right")
        cmds.text(label='  Naming Method: >')
        self.namingMenu = cmds.optionMenu("alphNumericOption", cc=self.updatePaddingState)  # <--- added cc callback
        cmds.menuItem(label = "123...")
        cmds.menuItem(label = "ABC...")
        cmds.menuItem(label = "abc...")
        cmds.setParent(self.masterLayout)
        
        cmds.rowColumnLayout(numberOfColumns=2,h=30,columnWidth = [(1,120),(2,80)])
        cmds.text(label='Padding:')
        self.paddingField = cmds.intField("userGivenPadding",w = 80,editable=True, v = 1)
        cmds.setParent(self.masterLayout)
        
        
        cmds.rowColumnLayout(numberOfColumns=2,h=30,columnWidth = [(1,120),(2,240)])
        cmds.text(label='Rename This: >')
        cmds.textField("userGivenName",w = 200,editable=True)
        cmds.setParent(self.masterLayout)
        cmds.separator(height=10, style= 'none' )
        cmds.button(label = "Go", w=400, h=30, command = self.namingSystem)
        cmds.separator(height=40,w=400)
        cmds.button(label = "Close", w=400, h=30, command = self.closeUI)
        cmds.separator(height=10, style= 'none' )
        #display new window
        cmds.showWindow()
        

    def closeUI(self,*arg):
        cmds.deleteUI(self.window, window=True)

    def updatePaddingState(self, *args):
        """Enable padding only for numeric mode"""
        method = cmds.optionMenu("alphNumericOption", q=True, v=True)
        if method == "123...":
            cmds.intField("userGivenPadding", e=True, en=True)
        else:
            cmds.intField("userGivenPadding", e=True, en=False)

    def to_excel_letters(self, num, upper=True):
        """Convert 1-based index to Excel-style letters (A..Z → AA, AB...)"""
        letters = ""
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            letters = chr(65 + remainder if upper else 97 + remainder) + letters
        return letters

    def selection(self, *args):
        selection_optionA = cmds.radioButton("selectedRadioBTNname", q=True, sl=1)
        selection_optionB = cmds.radioButton("hierarchyRadioBTNname", q=True, sl=1)
        selection_optionC = cmds.radioButton("allRadioBTNname", q=True, sl=1)
        searchName = cmds.textFieldGrp('searchWithName',q=True,text=True)
        replaceName = cmds.textFieldGrp('replaceWithName',q=True,text=True)
        if selection_optionA == True:
            selectedObjectA = cmds.ls(selection = True)
            if len(selectedObjectA)<1:
                cmds.warning("No object is currently selected. Please select object")
            else:
                for objA in selectedObjectA:
                    replacedNameA = objA.replace(searchName,replaceName)
                    newNameA = cmds.rename(objA, replacedNameA)
        if selection_optionB == True:
            selectedObjectB = cmds.ls(selection = True,dag=1)
            hierarchyChildren = cmds.listRelatives(selectedObjectB,children =True, type="transform")
            if len(selectedObjectB)<1:
                cmds.warning("No object is currently selected.Please select object")
            else:
                replacedNameB = selectedObjectB[0].replace(searchName,replaceName)
                newNameB = cmds.rename(selectedObjectB[0], replacedNameB)
                for objB in hierarchyChildren:
                    replacedNameB = objB.replace(searchName,replaceName)
                    newNameB = cmds.rename(objB, replacedNameB)
        if selection_optionC == True:
            all_obj = "*%s*"%searchName
            if len(all_obj)<1:
                print("please type the string in search for")
            else:
                all_objs = cmds.ls(all_obj, typ="transform")
                for objC in all_objs:
                    replacedNameC = objC.replace(searchName,replaceName)
                    newNameB = cmds.rename(objC, replacedNameC)

    def suffix(self,*arg):
        suffixNameA = cmds.textField("suffixName" ,q=True,text=True)
        selectedObjectForSuffix = cmds.ls(sl=True)
        if len(selectedObjectForSuffix)<1:
            cmds.warning("No Object is currently selected.Please Select a object")
        else:
            for selectedSuffixObject in selectedObjectForSuffix:
                addedSuffixName = selectedSuffixObject + suffixNameA
                renameSuffixName = cmds.rename(selectedSuffixObject,addedSuffixName)

    def prefix(self,*arg):
        prefixNameA = cmds.textField("prefixName" ,q=True,text=True)
        selectedObjectForPrefix = cmds.ls(sl=True)
        if len(selectedObjectForPrefix)<1:
            cmds.warning("No Object is currently selected.Please Select a object")
        else:
            for selectedPrefixObject in selectedObjectForPrefix:
                addedPrefixName = prefixNameA + selectedPrefixObject
                renamePrefixName =cmds.rename(selectedPrefixObject,addedPrefixName)           

    def namingSystem(self,*arg):       
        namingSystemUserGivenText = cmds.textField("userGivenName" ,q=True,text=True)
        namingSystemUserGivenPadding = cmds.intField("userGivenPadding" ,q=True,value=True)
        selectedObjectForNamingSystem = cmds.ls(selection = True, dag =1)    
        hierarchyChildrenForNamingSystem = cmds.listRelatives(selectedObjectForNamingSystem,children =True, type="transform")
        totalCountOfObjects = len(hierarchyChildrenForNamingSystem ) + 1
        side = ['','mid_','l_','r_']
        currentListOfSide = cmds.optionMenu('sideOption', query=True, value = True)
        currentValueOfNamingMethod = cmds.optionMenu('alphNumericOption', query=True, value=True)

        sideArrayValue = [] 
        if(currentListOfSide == "None"):
            sideArrayValue.append(0)
        if(currentListOfSide == "Mid"):
            sideArrayValue.append(1)
        if(currentListOfSide == "Left"):
            sideArrayValue.append(2)
        if(currentListOfSide == "Right"):
            sideArrayValue.append(3)
        sideName = sideArrayValue [0]

        sideAndMthodCombinedName = side[sideName] + namingSystemUserGivenText
        
        slTop = cmds.ls(selection = True)
        slTopDag = cmds.ls(selection = True,dag =True)
        slChild = cmds.listRelatives(slTopDag,children =True, type="transform")
        topAndChild = slTop + slChild       
        if len(selectedObjectForNamingSystem)<1:
            cmds.warning("No Object is currently selected.Please Select a object")
        else:
            if(currentValueOfNamingMethod == "123..."):
                for allCountings,allNamings in zip((range(totalCountOfObjects)),(topAndChild)):
                    # zero-padded numbering
                    countString = str(allCountings+1).zfill(namingSystemUserGivenPadding)
                    newNameForObjects = sideAndMthodCombinedName + "_" + countString
                    cmds.rename(allNamings,newNameForObjects)

            if(currentValueOfNamingMethod == "ABC..."):
                for i, obj in enumerate(topAndChild, 1):  # 1-based
                    letter = self.to_excel_letters(i, upper=True)
                    newUpperAlphaName = sideAndMthodCombinedName + "_" + letter
                    cmds.rename(obj, newUpperAlphaName)
                 
            if(currentValueOfNamingMethod == "abc..."):
                for i, obj in enumerate(topAndChild, 1):  # 1-based
                    letter = self.to_excel_letters(i, upper=False)
                    newLowerAlphaName = sideAndMthodCombinedName + "_" + letter
                    cmds.rename(obj,newLowerAlphaName)                    

myWindow = NvN_Window()
