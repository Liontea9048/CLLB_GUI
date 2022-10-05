from modules.classes import *

if __name__ == "__main__":
    # ------------------------ Create main winodw and set the size of window ------------------------ #
    root = Tk()
    root.title("Setup a CLLB's Settings and Run it")
    root.geometry("1300x550-800+100") # left upper in Mac
    root.resizable(True, True)

    # ------------------------ Create Labels, Set Variable Guide ------------------------ #
    ## intro
    lb_intro = Label(root, text="아래 변수들의 값을 설정하여 주십시오")
    lb_intro.place(x=labelPosX, y=10)

    # ------------------------ Frame ------------------------
    frame_var = LabelFrame(root, relief="solid", bd=2, text="VARIABLES", \
                            width=450, height=530, labelanchor="nw")
    frame_var.place(x=labelPosX, y=pos_y)

    # 1. Acquisition Time, in seconds -> this will be converted into ns in set files
    MLabel(frame_var, "Acquisiton Time", expYPos=pos_y, unitsText="s", unitsYPos=pos_y)
    Acq_time_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, maxVal=8970, name="Acq")

    # 2. High Voltage in Voltes
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "High Voltage", expYPos=pos_y, unitsText="V", unitsYPos=pos_y)
    HV_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, name="HV")

    # 3. Recording Length
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "Recording Length", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    RL_cmbox = MCombobox(frame_var, defaultVarIndex, yPos=pos_y)

    # 4. Pedestal Trigger interval in ms, 0 for disable
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "Pedestal Trigeer interval", expYPos=pos_y, unitsText="ms", unitsYPos=pos_y)
    PTI_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, name="PTI")

    # 5. ADC offset value (0-4095)
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "ADC Offset Value, Range: 0 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    AO_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, maxVal=4095, name="AO")

    # 6. ADC waveform delay from trigger point, 0 ~ 8,000
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "ADC Waveform Delay from Trigger Point,\nRange: 0 - 8000", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    AWD_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, maxVal=8000, name="AWD")

    # 7. Discrimination Threshold, 1 ~ 4095
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    MLabel(frame_var, "Discrimination Threshold, \nRange: 1 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    DT_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, minVal=1, maxVal=4095, name="DT")

    # 8. Input Pulse Polarity, 0 = negative, 1 = positive
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    MLabel(frame_var, "Input Pulse Polarity", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    IPP_cmbox = MCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="IPP")

    # 9. Peak Sum Width in ns (8 ~ 8000 ns)
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "Peak Sum Width, Range: 8 - 8000", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
    PSW_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, minVal=8, maxVal=8000, name="PSW")

    # 10. ADC mode, 0 = raw, 1 = filtered
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "ADC Mode", expYPos=pos_y, unitsYPos=pos_y)
    AM_cmbox = MCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="AM")

    # 11. Peak to Tail Start Delay, 0 ~ 8000 ns
    pos_y, defaultVarIndex = updateYposAndIndex()
    MLabel(frame_var, "Peak to Tail Start Delay,\nRange: 0 - 8000", expYPos=pos_y, unitsYPos=pos_y+5)
    PTSD_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, maxVal=8000, name="PTSD")

    # 12. Tail/Body Ratio Threshold
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    MLabel(frame_var, "Tail/Body Ratio Threshold", expYPos=pos_y, unitsYPos=pos_y)
    TBRT_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, name="TBRT")
    
    # 13. IP Address
    pos_y, defaultVarIndex = updateYposAndIndex(degree=30)
    MLabel(frame_var, "IP Address", expYPos=pos_y, unitsYPos=pos_y)
    Address_entry = MEntry(frame_var, defaultVarIndex, yPos=pos_y, name="IP")
    
    # 14. Data Type
    pos_y, defaultVarIndex = updateYposAndIndex(degree=30)
    MLabel(frame_var, "Data Type", expYPos=pos_y, unitsYPos=pos_y)
    Date_cmbox = MCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="Data")

    # 15. Save WaveForms
    pos_y, defaultVarIndex = updateYposAndIndex(degree=30)
    MLabel(frame_var, "Whether save Waverforms or not", expYPos=pos_y, unitsYPos=pos_y)
    WF_cmbox = MCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="WF")

    # ------------------------ Set and Run Frame ------------------------ #
    frame_SetAndRun = LabelFrame(root, relief="solid", bd=2, text="SET and RUN", \
                            width=250, height=300,labelanchor="nw")
    frame_SetAndRun.place(x=btnFramePadX, y=btnFramePadY)

    # ------------------------ Button for running the set up.

    btnStart = MButton(frame_SetAndRun, btnText="Start", whatRun="Start")
    btnStop = MButton(frame_SetAndRun, btnText="Stop", RelY=updateBtnPosition(), whatRun="Stop")
    
    ## input history files
    Label(frame_SetAndRun, text = "Select Input File \nfrom History to Import", justify="center").place(relx=0.5, rely=0.50, anchor=N)
    importFileList = ttk.Combobox(frame_SetAndRun, width = 20, height=20, state="readonly", justify="center")
    importFileList.place(rely = 0.5)
    OperatingComboBoxes["import"] = importFileList
    
    ## Open Output Folders
    btnApplyHisotry = MButton(frame_SetAndRun, btnText="Apply Previous Input", RelY=updateBtnPosition(), whatRun="ApplyHistory")
    # Operatingbtns["ApplyHistory"].place(relx=btnRelX, rely=0.70, anchor=N)
    
    # ---------------------- Frame for plot setting options tap
    
    frame_plotSet = LabelFrame(root, relief="solid", bd=2, text="Gate Setting", \
                            width=250, height=220,labelanchor="nw")
    frame_plotSet.place(x=btnFramePadX, y=320)
    
    # ---------------------- entries and buttons for setting up gate lines 
    _Font = ft.Font(size = 15)
    
    def updateInfo(event):
        try:
            sglg[0] = int(OperatingEntries["SG"].get())
            sglg[1] = int(OperatingEntries["LG"].get())
            isStart[0] == 0
        except:
            pass
    
    pos_x = 5; rely = 0.1
    Label(frame_plotSet, text = "ns", justify="center").place(x = 230, rely=rely, anchor=N)
    SG_Entry = Entry(frame_plotSet, width = 20, relief = "solid", \
        font = _Font, bd=2, justify="right", fg="black", bg="white"); OperatingEntries["SG"] = SG_Entry;
    SG_Entry.place(x=pos_x, rely=rely)
    SG_Entry.insert(0, "Enter Short Gate (ns)")
    
    
    rely += 0.2
    Label(frame_plotSet, text = "ns", justify="center").place(x = 230, rely=rely, anchor=N)
    LG_Entry = Entry(frame_plotSet, width = 20, relief = "solid", \
        font = _Font, bd=2, justify="right", fg="black", bg="white"); OperatingEntries["LG"] = LG_Entry;
    LG_Entry.place(x=pos_x, rely=rely)
    LG_Entry.insert(0, "Enter Long Gate (ns)")
    
    # bind
    SG_Entry.bind("<Leave>", updateInfo)
    SG_Entry.bind("<Return>", updateInfo)
    LG_Entry.bind("<Leave>", updateInfo)
    LG_Entry.bind("<Return>", updateInfo)
    
    rely += 0.2
    btnGate = MButton(frame_plotSet, btnText="Apply", RelY=rely,whatRun="plotOption")
    
    # ------------------------ Plot Frame ------------------------ #
    frame_Plot = LabelFrame(root, relief="solid", bd=2, text="Plot", \
                            width=550, height=550,labelanchor="nw")
    frame_Plot.place(x=plotFramePadX, y=plotFramePadY)

    plotting = MPlot(frame_Plot)
    btnGate.convertStart()
    # print(btnStart)
    
    def periodically_called_ftn():
        # if isStopped[0] == 1:
        #     plotting.numbering_ReadFile = 0;
        #     isStopped[0] = 0;
        
        if isStart[0] == 0:
            # isStart[0] == 1;
            # plotting.updateSGLG(btnGate.getSgLg())
            plotting.updateOptions()
        # btnGate.updateSGLG()
        # plotting.updateOptions()
        # print(isStart[0])
        plotting.startPlotting()
        root.after(10, periodically_called_ftn)
    
    periodically_called_ftn()
    
    root.mainloop()


    


    
