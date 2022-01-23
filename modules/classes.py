from modules.variables import *


class mLabel(Label):
    
    def __init__(self, masterFrame, expText="Type Explanation", expXPos=labelPosX, \
        expYPos=pos_y, unitsText="", unitsXPos=unitsXpos, unitsYPos=pos_y):
        self = Label(masterFrame, text=expText, justify="left");
        self.place(x=expXPos, y=expYPos);
        
        self = Label(masterFrame, text=unitsText);
        self.place(x=unitsXPos, y=unitsYPos);
        
class mEntry(Entry):
    
    def __init__(self, masterFrame, initIndex=0, xPos=varInputXpos, yPos=30, twoLines=0, minVal=0, maxVal=1e+9):
        # Set the basic settings, set self to Entry, and set base variables
        self = Entry(masterFrame, width=10, relief="solid", bd=2, justify="right");
        OperatingEntries.append(self); OperatingClassess.append(self)
        self.index = initIndex; initVar = defaultVar[self.index]
        self.initVar = initVar; VariableData[self.index] = self.initVar;
        
        ## adjust the positon of yPos
        if twoLines: self.place(x=xPos, y=yPos+5);
        else: self.place(x=xPos, y=yPos)
        
        ## Set min and max value of input range
        self.minVal = minVal; self.maxVal = maxVal; self.validVar=1;
        
        self.insert(0, initVar);
        mEntry.isAllowedInitVar(self)
        ## define functions that check the input value
        def isAllowed(event):
            #check the self.initVar or self.get() has a proper type
            try:
                float(self.get())
            except ValueError:
                print(f"The input of row {self.index + 1} is not permitted. please set it as number")
                self.config(fg="red")
                mEntry.setIsAllValidVar(self, 0)
                
            if float(self.get()) < self.minVal or float(self.get()) > self.maxVal:
                self.config(fg="red")
                mEntry.setIsAllValidVar(self, 0)
                
            else:
                self.config(fg="white")
                mEntry.setIsAllValidVar(self, 1)
                
        if self.maxVal:
            self.bind("<Leave>", isAllowed)
            self.bind("<Return>", isAllowed)
        
    """ set set self.validVar to 1 if the input is valid(in ragne)
        and set isAllValidVar[self.index] to 1 to check all data are valid when the btn is clicked,
        and set VariableDate[self.index] to input data to modify setup.txt """
    def setIsAllValidVar(self, value):
        if value:
            self.validVar = 1;
            isAllValidVar[self.index] = 1
            mEntry.setVariableData(self, self.get())
            for btns in Operatingbtns:
                mButton.switchBtn(btns);
        else:
            self.validVar = 0;
            isAllValidVar[self.index] = 0
    
    # set VariableData[self.index] to input data
    def setVariableData(self, data):
        VariableData[self.index] = data;

    # check the inputs whether that is in range or not
    # if the data is not in range, note that inputs with red colored font.
    def isAllowedInitVar(self):
        #check the self.initVar or self.get() has a proper type
        try:
            float(self.initVar)
        except ValueError:
            print(f"The input of row {self.index + 1} is not permitted. please set it as number")
            
        if self.maxVal:
            if float(self.minVal) <= float(self.initVar) <= float(self.maxVal):
                self.config(fg="white")
            else:
                self.config(fg="red")
                self.validVar = 0;
                isAllValidVar[defaultVar.index(self.initVar)] = 0;
        else:
            if float(self.minVal) <= float(self.initVar):
                self.config(fg="white")
            else:
                self.config(fg="red")
                self.validVar = 0;
                isAllValidVar[defaultVar.index(self.initVar)] = 0;
        
class mCombobox(ttk.Combobox):
    
    def __init__(self, masterFrame, initIndex=0, xPos=varInputXpos, yPos=10, flags="RLO"):
        self = ttk.Combobox(masterFrame, width = 8, height = 7,\
                state="readonly", justify="right");
        OperatingComboBoxes.append(self); OperatingClassess.append(self)
        self.index = initIndex; initVar = defaultVar[self.index]; self.initVar = initVar
                
        def setVariableData(event):
            data = self.inputVar[self.showingOptions.index(self.get())]
            mCombobox.setVariableData(self, data)
        
        if flags == "RLO":
            # Reocording length options            
            self.showingOptions = ["128 ns", "256 ns", \
                "512 ns", "1 \u03BCs", "2 \u03BCs", "4 \u03BCs", "8 \u03BCs"];
            self.inputVar = ["1","2","3","8","16","32","64"];
            
            self.config(values=self.showingOptions)
            self.variableDataIndex = self.inputVar.index(initVar)
            self.current(self.variableDataIndex)
            
        elif flags == "IPP":
            # Input Pulse Polarity, 0 for negative and 1 for positive
            self.showingOptions = ["Negative", "Positive"]
            self.inputVar = ["0", "1"]
            self.config(values=self.showingOptions)
            self.variableDataIndex = self.inputVar.index(initVar)
            self.current(self.variableDataIndex)
            
        elif flags == "AM":
            self.showingOptions = ["Raw", "Filtered"]
            self.inputVar = ["0", "1"]
            self.config(values=self.showingOptions)
            self.variableDataIndex = self.inputVar.index(initVar)
            self.current(self.variableDataIndex)
            
        mCombobox.setVariableData(self, self.initVar)
        self.bind("<<ComboboxSelected>>", setVariableData)
        self.place(x=xPos, y=yPos-2)
    
    def setVariableData(self, data):
        VariableData[self.index] = data;
        
class mButton(Button):

    def __init__(self, masterFrame, btnText="Type Text", RelX=btnRelX, RelY=btnRelY, whatRun=0):
        boldFont = ft.Font(size = 15, weight = "bold")
        self = Button(masterFrame, text=btnText, width=17, height=2, font=boldFont, padx=0, pady=0)
        Operatingbtns.append(self)
        self.place(relx=RelX, rely=RelY, anchor=N)
        self.today = str(date.today()) # yyyy-mm-dd
        mButton.switchBtn(self)
        
        ## copy inputs
        def copy_inputs():
            folderPath = f"./.setupHistory"
            if not (os.path.isdir(folderPath)):
                os.makedirs(folderPath)
            else:
                pass

            fileIndex = len(os.listdir(folderPath))
            filePath = f"{folderPath}/{self.today}_{fileIndex}"
            os.system(f"cp {args.setup} {filePath}")
            h = open(filePath, "a")
            h.write(f"copied date = {str(datetime.now())}")
            h.close()
        
        #check the variables are valid 
        def modifySetupFile():
            print("Setup.txt file is set to : ", VariableData)
            g = open(args.setup, "w")
            for i in range(numOfVar):
                g.write(f"{VariableData[i]}\n");
            g.close()
        
        def execSetExe():
            os.system(args.set)
            
        def execRunExe():
            os.system(args.run)
            copy_inputs()
            Operatingbtns[-1].config(state="normal")
            OperatingComboBoxes[-1].config(values=getImportInputs())
            OperatingComboBoxes[-1].current(0)
            
        def invokeBtns():
            Operatingbtns[0].invoke()
            sleep(1)
            copy_inputs()
            os.system(f"{args.set} && {args.run}")
            
        def getImportInputs():
            folderPath = f"./.setupHistory"
            dirList = os.listdir(folderPath)
            if dirList:
                return natsort.natsorted(dirList, reverse=True)
            else:
                Operatingbtns[-1].config(state="disabled")
                return ["No History Files"]
            
        
        def refreshStatus(history): 
            # Just for showing, not applied 
            for i in range(len(history)):
                tempClass = OperatingClassess[i]; value = history[i]
                if type(tempClass) == Entry:
                    tempClass.delete(0, END)
                    tempClass.insert(0, value)
                elif type(tempClass) == ttk.Combobox:
                    tempClass.current(tempClass.inputVar.index(value))
                    
            # import msg box 
            msgBox = messagebox.askokcancel("Variables of Selected Input", "Are you sure to apply these inputs?")
            # when user select yes, set the variableData to hisory's variables
            if msgBox:
                # load variables 
                global VariableData
                global isAllValidVar
                
                # Set the history to variableData to apply history input.
                VariableData = history
                isAllValidVar = [1 for i in range(numOfVar)]
            
        def showInfo():
            # Set file Path
            fineName = OperatingComboBoxes[-1].get();
            folderPath = f"./.setupHistory"
            filePath = f"{folderPath}/{fineName}"
            
            # Read History Variables
            f = open(filePath, "r"); historyVar = []
            for i in range(numOfVar):
                var = f.readline().split()
                historyVar.append(var[0])
            f.close()
            
            # update data
            refreshStatus(historyVar);
        
        # checks all variables are valid
        if whatRun == 0: # Modify Setup.txt
            self.config(command=modifySetupFile)            
        elif whatRun == 1: # exec set
            self.config(command=execSetExe)
        elif whatRun == 2: # exec run
            self.config(command=execRunExe)
            # self.config(command=execRunExe)
        elif whatRun == 3: # import inputs from history
            self.config(command=invokeBtns)
        elif whatRun == 4: # import inputs from history
            OperatingComboBoxes[-1].config(values=getImportInputs())
            OperatingComboBoxes[-1].current(0)
            OperatingComboBoxes[-1].place(relx=0.5, rely=0.85, anchor=N)
            OperatingComboBoxes[-1].bind("<<ComboboxSelected>>", showInfo)
            self.config(command=showInfo)
        
            
    def isAllValidVar(self):
        if not (0 in isAllValidVar):
            return True;
        else:
            return False
    
    def switchBtn(self):
        if mButton.isAllValidVar(self):
            self.config(state="normal")
        else:
            self.config(state="disabled")
        
        
        