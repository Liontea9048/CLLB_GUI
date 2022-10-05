from modules.variables import *

class MLabel(Label):
    
    def __init__(self, masterFrame, expText="Type Explanation", expXPos=labelPosX, \
        expYPos=pos_y, unitsText="", unitsXPos=unitsXpos, unitsYPos=pos_y):
        self = Label(masterFrame, text=expText, justify="left");
        self.place(x=expXPos, y=expYPos);
        
        self = Label(masterFrame, text=unitsText);
        self.place(x=unitsXPos, y=unitsYPos);
        
class MEntry(Entry):
    
    def __init__(self, masterFrame, initIndex=0, xPos=varInputXpos, yPos=30, twoLines=0, minVal=0, maxVal=1e+9, name="none"):
        # Set the basic settings, set self to Entry, and set base variables
        self = Entry(masterFrame, width=10, relief="solid", bd=2, justify="right", fg="black");
        # OperatingEntries.append(self); OperatingClassess.append(self)
        OperatingEntries[name] = self; OperatingClassess[name] = self
        self.name = name
        self.index = initIndex; initVar = defaultVar[self.index]
        self.initVar = initVar; VariableData[self.index] = self.initVar;
        
        ## adjust the positon of yPos
        if twoLines: self.place(x=xPos, y=yPos+5);
        else: self.place(x=xPos, y=yPos)
        
        ## Set min and max value of input range
        self.minVal = minVal; self.maxVal = maxVal; self.validVar=1;
        
        self.insert(0, initVar);
        MEntry.isAllowedInitVar(self)
        ## define functions that check the input value
        def isAllowed(event):
            #check the self.initVar or self.get() has a proper type
            try:
                float(self.get())
            except ValueError:
                print(f"The input of row {self.index + 1} is not permitted. please set it as number")
                self.config(fg="red", bg="white")
                MEntry.setIsAllValidVar(self, 0)
                
            if float(self.get()) < self.minVal or float(self.get()) > self.maxVal:
                self.config(fg="red", bg="white")
                MEntry.setIsAllValidVar(self, 0)
                
            else:
                self.config(fg="black", bg="white")
                MEntry.setIsAllValidVar(self, 1)
                isStart[0] = 0
                
                
        def refreshOptions(event):
            MEntry.refreshOptions(self)
        if self.maxVal:
            if self.name != "IP":
                self.bind("<Leave>", isAllowed)
                self.bind("<Return>", isAllowed)
                # self.bind("<Leave>", refreshOptions)
                # self.bind("<Return>", refreshOptions)
            else:
                self.config(fg="black", bg="white")
                pass
        
    """ set set self.validVar to 1 if the input is valid(in ragne)
        and set isAllValidVar[self.index] to 1 to check all data are valid when the btn is clicked,
        and set VariableDate[self.index] to input data to modify setup.txt """
    def setIsAllValidVar(self, value):
        if value:
            self.validVar = 1;
            isAllValidVar[self.index] = 1
            MEntry.setVariableData(self, self.get())
            for btns in Operatingbtns.items():
                MButton.switchBtn(btns[1]);
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
        def isAllowed(event):
            #check the self.initVar or self.get() has a proper type
            try:
                float(self.get())
            except ValueError:
                print(f"The input of row {self.index + 1} is not permitted. please set it as number")
                self.config(fg="red", bg="white")
                MEntry.setIsAllValidVar(self, 0)
                
            if float(self.get()) < self.minVal or float(self.get()) > self.maxVal:
                self.config(fg="red", bg="white")
                MEntry.setIsAllValidVar(self, 0)
                
            else:
                self.config(fg="black", bg="white")
                MEntry.setIsAllValidVar(self, 1)
        
        if self.name != "IP":    
            if self.maxVal:
                if float(self.minVal) <= float(self.initVar) <= float(self.maxVal):
                    self.config(fg="black", bg="white")
                else:
                    self.config(fg="red", bg="white")
                    self.validVar = 0;
                    isAllValidVar[defaultVar.index(self.initVar)] = 0;
            else:
                if float(self.minVal) <= float(self.initVar):
                    self.config(fg="black", bg="white")
                else:
                    self.config(fg="red", bg="white")
                    self.validVar = 0;
                    isAllValidVar[defaultVar.index(self.initVar)] = 0;
    
    def getPlotting(self, mplot):
        self.plotting = mplot;
        
    def refreshOptions(self):
        self.plotting.updateOptions();
    
class MCombobox(ttk.Combobox):
    
    def __init__(self, masterFrame, initIndex=0, xPos=varInputXpos, yPos=10, flags="RLO"):
        self = ttk.Combobox(masterFrame, width = 8, height = 7,\
                state="readonly", justify="right");
        # OperatingComboBoxes.append(self); OperatingClassess.append(self)
        OperatingComboBoxes[flags] = self; OperatingClassess[flags] = self;
        self.index = initIndex; initVar = defaultVar[self.index]; self.initVar = initVar
        self.plotting = 0
                
        def setVariableData(event):
            data = self.inputVar[self.showingOptions.index(self.get())]
            MCombobox.setVariableData(self, data)
            isStart[0] = 0
            
        def refreshOptions(event):
            MCombobox.refreshOptions(self);
        
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
            
        elif flags == "Data":
            self.showingOptions = ["Background", "Am-241", "Cs-137", "Ba-133", "Eu-152", "Co-60", "241AmBe", "Cf-252"]
            self.inputVar = ["Background", "Am-241", "Cs-137", "Ba-133", "Eu-152", "Co-60", "241AmBe", "Cf-252"]
            self.config(values=self.showingOptions)
            self.variableDataIndex = self.inputVar.index(initVar)
            self.current(self.variableDataIndex)
        
        elif flags == "WF":
            self.showingOptions = ["Do not", "Save Waveforms"]
            self.inputVar = ["0", "1"]
            self.config(values=self.showingOptions)
            self.variableDataIndex = self.inputVar.index(initVar)
            self.current(self.variableDataIndex)
            
        MCombobox.setVariableData(self, self.initVar)
        self.bind("<<ComboboxSelected>>", setVariableData)
        # self.bind("<<ComboboxSelected>>", refreshOptions)
        self.place(x=xPos, y=yPos-2)
    
    def getPlotting(self, mplot):
        self.plotting = mplot;
        
    def refreshOptions(self):
        self.plotting.updateOptions();
            
    def setVariableData(self, data):
        VariableData[self.index] = data;
        
    def setVariableData(self, data):
        VariableData[self.index] = data;
               
class MButton(Button):

    def __init__(self, masterFrame, btnText="Type Text", RelX=btnRelX, RelY=btnRelY, whatRun="modify"):
        boldFont = ft.Font(size = 10, weight = "bold")
        self = Button(masterFrame, text=btnText, width=17, height=2, font=boldFont, padx=0, pady=0)
        Operatingbtns[whatRun] = self
        self.place(relx=RelX, rely=RelY, anchor=N)
        self.historyVar = []; self.isStart = [0]
        self.today = str(date.today()) # yyyy-mm-dd
        self.lg, self.sg = 0, 0
        # self.asd = 0
        
        MButton.switchBtn(self)
        
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
            copy_inputs()
            Operatingbtns["ApplyHistory"].config(state="normal")
            OperatingComboBoxes["import"].config(values=getImportInputs())
            OperatingComboBoxes["import"].current(0)
        
        def execSetExe():
            os.system(f"{args.set} {VariableData[-3]}")
            
        def execRunExe():
            os.system(f"{args.run} {VariableData[-3]} {VariableData[-2]} {VariableData[-1]} 1 10 &")
            Operatingbtns["ApplyHistory"].config(state="normal")
            OperatingComboBoxes["import"].config(values=getImportInputs())
            OperatingComboBoxes["import"].current(0)
                    
        def writeLog(text):
            f = open("./cllb.log", "a")
            f.write(f"{text} at : {str(datetime.now())}\n")
            f.close()
            
        def Start():
            os.system("rm -rf ./killme.txt")
            os.system("rm -rf ./waveFiles/*")
            writeLog("start")
            modifySetupFile()
            execSetExe()
            execRunExe()
        
        def Stop():
            # make killme.txt file to shut down the measurements
            f = open("killme.txt", "w")
            f.close()
            writeLog("killed")
            os.system("rm -rf ./killme.txt")
            # os.system("rm -rf ./waveFiles/*")
            isStopped[0] = 1
            # stop reading and plotting the wave forms
            
        def getImportInputs():
            folderPath = f"./.setupHistory"
            dirList = os.listdir(folderPath)
            if dirList:
                return natsort.natsorted(dirList, reverse=True)
            else:
                Operatingbtns["ApplyHistory"].config(state="disabled")
                return ["No History Files"]
            
        
        def refreshStatus(): 
            # import msg box 
            msgBox = messagebox.askokcancel("Variables of Selected Input", "Are you sure to apply these inputs?")
            # when user select yes, set the variableData to hisory's variables
            if msgBox:
                # load variables 
                global VariableData
                global isAllValidVar
                
                # Set the history to variableData to apply history input.
                VariableData = self.history
                isAllValidVar = [1 for i in range(numOfVar)]
            
        def showInfo(event):
            # Set file Path
            fineName = OperatingComboBoxes["import"].get();
            folderPath = f"./.setupHistory"
            filePath = f"{folderPath}/{fineName}"
            
            # Read History Variables
            f = open(filePath, "r"); self.history = []
            for i in range(numOfVar):
                var = f.readline().split()
                self.history.append(var[0])
            f.close()
            
            # Just for showing, not applied 
            for i in range(len(self.history)):
                key = list(OperatingClassess.keys())[i]
                tempClass = OperatingClassess[key];
                value = self.history[i]
                if type(tempClass) == Entry:
                    tempClass.delete(0, END)
                    tempClass.insert(0, value)
                elif type(tempClass) == ttk.Combobox:
                    tempClass.current(tempClass.inputVar.index(value))
            
            # update data
            # refreshStatus(historyVar);
            
        def activeBtn():
            self.config(state="normal")
            
        def plotOption():
            try:
                # self.SG = int(OperatingEntries["SG"].get())
                # self.LG = int(OperatingEntries["LG"].get()) 
                sglg[0] = int(OperatingEntries["SG"].get())
                sglg[1] = int(OperatingEntries["LG"].get())
                isStart[0] == 0
                # print(sglg)
                # print(int(OperatingEntries["SG"].get()), int(OperatingEntries["LG"].get()))
                
            except:
                print("Please Gate Parameters in integer")
                self.config(state="disabled")
                self.after(1000, activeBtn)
                
        # def updateInfo(event):
        #     try:
        #         # self.SG = int(OperatingEntries["SG"].get())
        #         # self.LG = int(OperatingEntries["LG"].get()) 
        #         sglg[0] = int(OperatingEntries["SG"].get())
        #         sglg[1] = int(OperatingEntries["LG"].get())
        #         isStart[0] == 0
                
        #     except:
        #         pass
            
        # checks all variables are valid
        # not used 
        if whatRun == "modify": # Modify Setup.txt
            self.config(command=modifySetupFile)            
        elif whatRun == "Set": # exec set
            self.config(command=execSetExe)
        elif whatRun == "Run": # exec run
            self.config(command=execRunExe)
            # self.config(command=execRunExe)
        # not used 
        
        elif whatRun == "Start": # import inputs from history
            self.config(command=Start)
        elif whatRun == "Stop": # import inputs from history
            self.config(command=Stop)
            
        elif whatRun == "ApplyHistory": # import inputs from history
            OperatingComboBoxes["import"].config(values=getImportInputs())
            OperatingComboBoxes["import"].current(0)
            OperatingComboBoxes["import"].place(relx=0.5, rely=0.65, anchor=N)
            OperatingComboBoxes["import"].bind("<<ComboboxSelected>>", showInfo)
            self.config(command=refreshStatus)
        
        elif whatRun == "plotOption": # import inputs from history
            self.config(command=plotOption)
            # self.bind("")
            
    def isAllValidVar(self):
        if not (0 in isAllValidVar):
            return True;
        else:
            return False
    
    def switchBtn(self):
        if MButton.isAllValidVar(self):
            self.config(state="normal")
        else:
            self.config(state="disabled")
        
    def convertStart(self):
        self.isStart = [1]
        
    def returnStart(self):
        return self.today
    
    def updateSGLG(self):
        try:
            Isnew0 = (sglg[0] != int(OperatingEntries["SG"].get()))
            Isnew1 = (sglg[1] != int(OperatingEntries["LG"].get()))
            if Isnew0 or Isnew1:
                sglg[0] = int(OperatingEntries["SG"].get())
                sglg[1] = int(OperatingEntries["LG"].get())
                isStart[0] == 0
            else:
                isStart[0] == 1;
                
            
            
            
        except:
            print("Please Gate Parameters in integer")   
    
class MPlot():
    
    def __init__(self, masterFrame):
        self.figure = Figure(figsize=(7,6)); 
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Wave Form", fontsize=20)
        self.ax.set_xlabel("Time (ns)", fontsize=18)
        self.ax.set_ylabel("Wave Height (adc)", fontsize = 18)
        self.RLO = int(VariableData[2])
        timelist = [128, 256, 512, 1024, 2048, 4096, 8192]
        indexlist = [1, 2, 3, 8, 16 ,32 ,64]
        self.RLO = timelist[indexlist.index(self.RLO)]
        self.masterFrame = masterFrame
        self.rise = 0
        self.SG, self.LG = sglg[0], sglg[1]
        self.lst = []
            
        # self.showingOptions = ["128 ns", "256 ns", \
        #         "512 ns", "1 \u03BCs", "2 \u03BCs", "4 \u03BCs", "8 \u03BCs"];
        #     self.inputVar = ["1","2","3","8","16","32","64"];
        
        font1 = {
            "family": "DejaVu Sans",
            "color": "black",
            "size": 15}
        
        self.offSet = int(VariableData[4])
        self.Threshold = self.offSet - int(VariableData[6])

        self.minimumChannel = self.offSet + 1000
        self.isRunning = 0;
        self.numbering_ReadFile = 0;
        if self.minimumChannel <= maximumChannel: 
            ymax = self.minimumChannel
        else: 
            ymax = maximumChannel
        self.ax.set_xlim(0, self.RLO); 
        self.ax.set_ylim(0, ymax)
        self.ax.grid(alpha = 0.3, color="grey")
        
        # line variables
        xstart = self.RLO / 30
        xend = xstart + xstart*3
        xprimestart = xend 
        
        # horizontal lines 
        self.offSetLine = self.ax.hlines(self.offSet, 0, self.RLO, colors="green", linestyle="--")
        self.lst.append(self.ax.hlines(self.offSet+350, xstart, xend, colors="green", linestyle="--"))
        self.lst.append(self.ax.text(xprimestart, self.offSet+300, "Offset", fontdict=font1))
        
        self.thresholdLine = self.ax.hlines(self.Threshold, 0, self.RLO, colors="red", linestyle="--")
        self.lst.append(self.ax.hlines(self.offSet+150, xstart, xend, colors="red", linestyle="--"))
        self.lst.append(self.ax.text(xprimestart, self.offSet+150, "Threshold", fontdict=font1))

        # vertical lines 
        self.riseLine = self.ax.vlines(self.rise, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
        self.sgLine = self.ax.vlines(self.SG, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
        self.lgLine = self.ax.vlines(self.LG, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
    
        self.canvas = FigureCanvasTkAgg(self.figure, masterFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=15, pady=15)
        plt.pause(0.001)
        
    def readAndPlotData(self, n):
        filename = os.path.join(folderPath, f"FADC_EventMode__{n}.dat")
        try:
            f = open(filename, "rb")
        except:
            return False
        
        for i in range(1):
            byte = f.read(1)
            data = bytearray(byte)
            
        #record Length
        rl = data[0] & 0xFF;
        data_length = rl * 128 - 1;
        nsample = rl * 64 - 6;
    
        # read data
        data = bytearray()
        for i in range(data_length):
            byte = f.read(1)
            data.extend(bytearray(byte))
        if (rl != 0xFF):
            # get mid
            mid = data[0] & 0xFF;
            # print(f"mid : {mid}")
            # get channel #
            channel = data[1] & 0xF;
            # print(f"channel : {channel}")  
            # get trigger pattern
            trig_pattern = (data[1] >> 4) & 0xF;
            # print(f"trig : {trig_pattern}")  

            # get time stamp
            time_stamp = data[2] & 0xFF;
            lltmp = data[3] & 0xFF;
            lltmp = lltmp << 8;
            time_stamp = time_stamp + lltmp;
            lltmp = data[4] & 0xFF;
            lltmp = lltmp << 16;
            time_stamp = time_stamp + lltmp;
            lltmp = data[5] & 0xFF;
            lltmp = lltmp << 24;
            time_stamp = time_stamp + lltmp;
            lltmp = data[6] & 0xFF;
            lltmp = lltmp << 32;
            time_stamp = time_stamp + lltmp;
            time_stamp = time_stamp * 8;
            # print(f"time_stamp : {time_stamp}")  

            # get event number
            event_num = data[7] & 0xFF;
            tmp = data[8] & 0xFF;
            tmp = tmp << 8;
            event_num = event_num + tmp;
            tmp = data[9] & 0xFF;
            tmp = tmp << 16;
            event_num = event_num + tmp;
            tmp = data[10] & 0xFF;
            tmp = tmp << 24;
            event_num = event_num + tmp;
            # print(f"event_num : {event_num}")  

            # get waveform
            adc = []
            xlist = []; ylist = []
            self.isFound = False
            for i in range(nsample):    
                adc.append(data[2 * i + 11] & 0xFF)
                tmp = data[2 * i + 12] & 0xFF;
                tmp = tmp << 8;
                adc[i] = adc[i] + tmp;
                
                if self.isFound == False and (adc[i] < self.Threshold):
                    self.rise = (i * 2)
                    self.isFound = True;
                
                xlist.append(i * 2); ylist.append(adc[i])

            # print(f"mid = {mid}, ch = {channel}, trigger pattern = {trig_pattern}, time stamp = {time_stamp} ns, event # = {event_num}\n")
            
            # print("----------adsasdasd")
            # # for i in range (int(len(xlist)/2)):
            # for i in ylist:
            #     # print(xlist[i], ylist[i],self.Threshold)
            #     # print (int(adc[i]), self.Threshold)
            #     if self.isFound == False and (i < self.Threshold):
            #         self.rise = (i * 2)
            #         self.isFound = True;
            # print("-----------------------------------------------")
            
            # sleep(10)
            
            # plot region 
            try:
                self.line.set_xdata(xlist)
                self.line.set_ydata(ylist)
                # figure.clear()
                self.figure.canvas.draw()
                self.figure.canvas.flush_events()
                plt.pause(0.001)        
            except:
                self.line, = self.ax.plot(xlist, ylist)
                plt.pause(0.001)
            
        f.close()
        # os.system(f"rm -rf {filename}")
        return True

    def startPlotting(self):
        try:
            f = open("killme.txt", "r")
            return False
        except:
            if self.readAndPlotData(self.numbering_ReadFile):
                self.updateReadFile()
            else:
                pass
            
    def updateReadFile(self):
        self.numbering_ReadFile += 1;
        
    def updateSGLG(self, SG, LG):
        self.SG = SG
        self.LG = LG
        
    def updateOptions(self):
        
        # make all lines invisible
        self.offSetLine.set_visible(False)
        self.thresholdLine.set_visible(False)
        self.riseLine.set_visible(False)
        self.sgLine.set_visible(False)
        self.lgLine.set_visible(False)
        
        for _ in self.lst:
            _.set_visible(False)
        
        # self.ax.cla()
        # self.ax.set_title("Wave Form", fontsize=20)
        # self.ax.set_xlabel("Time (ns)", fontsize=18)
        # self.ax.set_ylabel("Wave Height (adc)", fontsize = 18)
        self.RLO = int(VariableData[2])
        timelist = [128, 256, 512, 1024, 2048, 4096, 8192]
        indexlist = [1, 2, 3, 8, 16 ,32 ,64]
        self.RLO = timelist[indexlist.index(self.RLO)]
        self.offSet = int(VariableData[4])
        self.Threshold = self.offSet - int(VariableData[6])
        self.SG, self.LG = sglg[0], sglg[1]
        self.minimumChannel = self.offSet + 1000
        if self.minimumChannel <= maximumChannel: 
            ymax = self.minimumChannel
        else: 
            ymax = maximumChannel
        
        self.ax.set_xlim(0, self.RLO); 
        self.ax.set_ylim(0, ymax)
        # self.ax.grid(alpha = 0.3, color="grey")
        
        # self.offsetLine = self.ax.hlines(self.offSet, 0, self.RLO, colors="green", linestyle="--")
        # self.thresholdLine = self.ax.hlines(self.Threshold, 0, self.RLO, colors="red", linestyle="--")
        
        font1 = {
                "family": "DejaVu Sans",
                "color": "black",
                "size": 15}
        
        # line variables
        xstart = self.RLO / 30
        xend = xstart + xstart*3
        xprimestart = xend 
        
        # horizontal lines 
        self.offSetLine = self.ax.hlines(self.offSet, 0, self.RLO, colors="green", linestyle="--")
        self.lst.append(self.ax.hlines(self.offSet+350, xstart, xend, colors="green", linestyle="--"))
        self.lst.append(self.ax.text(xprimestart, self.offSet+300, "Offset", fontdict=font1))
        
        self.thresholdLine = self.ax.hlines(self.Threshold, 0, self.RLO, colors="red", linestyle="--")
        self.lst.append(self.ax.hlines(self.offSet+150, xstart, xend, colors="red", linestyle="--"))
        self.lst.append(self.ax.text(xprimestart, self.offSet+150, "Threshold", fontdict=font1))

        # vertical lines git
        self.riseLine = self.ax.vlines(self.rise, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
        self.sgLine = self.ax.vlines(self.rise+self.SG, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
        self.lgLine = self.ax.vlines(self.rise+self.LG, 0, maximumChannel, colors="gray", linestyle="--", alpha = 0.7)
        # print("------------------------------")
        # print(self.rise, self.SG, self.LG)
        # print("------------------------------")
        # print(self.offSet, self.Threshold)
    
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=15, pady=15)
        plt.pause(0.001)
