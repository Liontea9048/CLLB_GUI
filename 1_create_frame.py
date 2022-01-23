from modules.classes import *

if __name__ == "__main__":
    # ------------------------ Create main winodw and set the size of window ------------------------ #
    root = Tk()
    root.title("Setup a CLLB's Settings and Run it")
    root.geometry("730x450-800+100") # left upper in Mac
    root.resizable(False, False)

    # ------------------------ Create Labels, Set Variable Guide ------------------------ #
    ## intro
    lb_intro = Label(root, text="아래 변수들의 값을 설정하여 주십시오")
    lb_intro.place(x=labelPosX, y=10)

    # ------------------------ Frame ------------------------
    frame_var = LabelFrame(root, relief="solid", bd=2, text="VARIABLES", \
                            width=450, height=430, labelanchor="nw")
    frame_var.place(x=labelPosX, y=pos_y)

    # 1. Acquisition Time, in seconds -> this will be converted into ns in set files
    mLabel(frame_var, "Acquisiton Time", expYPos=pos_y, unitsText="s", unitsYPos=pos_y)
    Acq_time_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, maxVal=8970)

    # 2. High Voltage in Voltes
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "High Voltage", expYPos=pos_y, unitsText="V", unitsYPos=pos_y)
    HV_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y)

    # 3. Recording Length
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "Recording Length", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    RL_cmbox = mCombobox(frame_var, defaultVarIndex, yPos=pos_y)

    # 4. Pedestal Trigger interval in ms, 0 for disable
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "Pedestal Trigeer interval", expYPos=pos_y, unitsText="ms", unitsYPos=pos_y)
    PTI_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y)

    # 5. ADC offset value (0-4095)
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "ADC Offset Value, Range: 0 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    AO_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, maxVal=4095)

    # 6. ADC waveform delay from trigger point, 0 ~ 8,000
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "ADC Waveform Delay from Trigger Point,\nRange: 0 - 8000", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    AWD_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, maxVal=8000)

    # 7. Discrimination Threshold, 1 ~ 4095
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    mLabel(frame_var, "Discrimination Threshold, \nRange: 1 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    DT_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, minVal=1, maxVal=4095)

    # 8. Input Pulse Polarity, 0 = negative, 1 = positive
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    mLabel(frame_var, "Input Pulse Polarity", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
    IPP_cmbox = mCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="IPP")

    # 9. Peak Sum Width in ns (8 ~ 8000 ns)
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "Peak Sum Width, Range: 8 - 8000", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
    PSW_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, minVal=8, maxVal=8000)

    # 10. ADC mode, 0 = raw, 1 = filtered
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "ADC Mode", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
    AM_cmbox = mCombobox(frame_var, defaultVarIndex, yPos=pos_y, flags="AM")

    # 11. Peak to Tail Start Delay, 0 ~ 8000 ns
    pos_y, defaultVarIndex = updateYposAndIndex()
    mLabel(frame_var, "Peak to Tail Start Delay,\nRange: 0 - 8000", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y+5)
    PTSD_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y, twoLines=1, maxVal=8000)

    # 12. Tail/Body Ratio Threshold
    pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
    mLabel(frame_var, "Tail/Body Ratio Threshold", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
    TBRT_entry = mEntry(frame_var, defaultVarIndex, yPos=pos_y)

    # ------------------------ Set and Run Frame ------------------------ #
    frame_SetAndRun = LabelFrame(root, relief="solid", bd=2, text="SET and RUN", \
                            width=250, height=430,labelanchor="nw")
    frame_SetAndRun.place(x=btnFramePadX, y=btnFramePadY)

    # ------------------------ Button for running the set up.

    ## input history files
    Label(frame_SetAndRun, text = "Select Input File from History to Import", justify="center").place(relx=0.5, rely=0.80, anchor=N)
    importFileList = ttk.Combobox(frame_SetAndRun, width = 20, height=20, state="readonly", justify="center")
    OperatingComboBoxes.append(importFileList)

    ## Modify the setup.txt
    btnModifySetupTxt = mButton(frame_SetAndRun, btnText="Modify Setup.txt", whatRun=0)
    ## Execute set*.exe
    btnExecSet = mButton(frame_SetAndRun, btnText="Execute Set.exe", RelY=updateBtnPosition(), whatRun=1)
    ## Execute run*.exe
    btnExecRun = mButton(frame_SetAndRun, btnText="Execute Run.exe", RelY=updateBtnPosition(), whatRun=2)
    ## Open input Folders
    btnSetAndRun = mButton(frame_SetAndRun, btnText="Set And Run All Things", RelY=updateBtnPosition(), whatRun=3)
    ## Open Output Folders
    btnApplyHisotry = mButton(frame_SetAndRun, btnText="Apply Previous Input", RelY=updateBtnPosition(), whatRun=4)
    Operatingbtns[-1].place(relx=btnRelX, rely=0.70, anchor=N)

    root.mainloop()