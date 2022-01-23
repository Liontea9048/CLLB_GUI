# import tkinter.ttk as ttk
# from tkinter import *
# import tkinter.font as ft
# from modules.variables import *
from modules.classes import *

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
Acq_time_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# 2. High Voltage in Voltes
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "High Voltage", expYPos=pos_y, unitsText="V", unitsYPos=pos_y)
HV_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# 3. Recording Length
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "Recording Length", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
RL_cmbox = mCombobox(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# 4. Pedestal Trigger interval in ms, 0 for disable
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "Pedestal Trigeer interval", expYPos=pos_y, unitsText="ms", unitsYPos=pos_y)
PTI_entry = mEntry(frame_var, initVar = defaultVar[defaultVarIndex], yPos=pos_y, flages="PTI")

# 5. ADC offset value (0-4095)
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "ADC Offset Value, Range: 0 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
AO_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# 6. ADC waveform delay from trigger point, 0 ~ 8,000
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "ADC Waveform Delay from Trigger Point,\nRange: 0 - 8000", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
AWD_entry = AO_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y, twoLines=1)

# 7. Discrimination Threshold, 1 ~ 4095
pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
mLabel(frame_var, "Discrimination Threshold, \nRange: 1 - 4095", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
DT_entry = AO_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y, twoLines=1)

# 8. Input Pulse Polarity, 0 = negative, 1 = positive
pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
mLabel(frame_var, "Input Pulse Polarity", expYPos=pos_y, unitsText="", unitsYPos=pos_y)
IPP_cmbox = mCombobox(frame_var, defaultVar[defaultVarIndex], yPos=pos_y, flags="IPP")

# 9. Peak Sum Width in ns (8 ~ 8000 ns)
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "Peak Sum Width, Range: 8 - 8000", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
PSW_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# 10. ADC mode, 0 = raw, 1 = filtered
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "ADC Mode", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
AM_cmbox = mCombobox(frame_var, defaultVar[defaultVarIndex], yPos=pos_y, flags="AM")

# 11. Peak to Tail Start Delay, 0 ~ 8000 ns
pos_y, defaultVarIndex = updateYposAndIndex()
mLabel(frame_var, "Peak to Tail Start Delay,\nRange: 0 - 8000", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y+5)
PTSD_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y, twoLines=1)

# 12. Tail/Body Ratio Threshold
pos_y, defaultVarIndex = updateYposAndIndex(degree=40)
mLabel(frame_var, "Tail/Body Ratio Threshold", expYPos=pos_y, unitsText="ns", unitsYPos=pos_y)
TBRT_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)

# ------------------------ Set and Run Frame ------------------------ #
# ------------------------ Frame - Right side
frame_SetAndRun = LabelFrame(root, relief="solid", bd=2, text="SET and RUN", \
                        width=250, height=430,labelanchor="nw")
frame_SetAndRun.place(x=btnFramePadX, y=btnFramePadY)

# ------------------------ Button for running the set up.
## Modify the setup.txt
btnModifySetupTxt = mButton(frame_SetAndRun, btnText="Modify Setup.txt")
# btnModifySetupTxt = Button(frame_SetAndRun, text="Modify Setup.txt", width=15, height=2, font=boldFont, padx=0, pady=0)
# btnModifySetupTxt.place(relx=0.5, rely=0.05, anchor=N)

## Execute set*.exe
btnExecSet = mButton(frame_SetAndRun, btnText="Execute Set.exe", RelY=updateBtnPosition())
# btnExecSet = Button(frame_SetAndRun, text="Execute Set.exe", width=15, height=2, font=boldFont, padx=0, pady=0)
# btnExecSet.place(relx=0.5, rely=0.20, anchor=N)

## Execute run*.exe
btnExecRun = mButton(frame_SetAndRun, btnText="Execute Run.exe", RelY=updateBtnPosition())
# btnExecRun = Button(frame_SetAndRun, text="Execute Run.exe", width=15, height=2, font=boldFont, padx=0, pady=0)
# btnExecRun.place(relx=0.5, rely=0.35, anchor=N)

## Open input Folders
btnOpenInputs = mButton(frame_SetAndRun, btnText="Open Inputs Directory", RelY=updateBtnPosition())
# btnOpenInputs = Button(frame_SetAndRun, text="Open Inputs Directory", width=15, height=2, font=boldFont, padx=0, pady=0)
# btnOpenInputs.place(relx=0.5, rely=0.50, anchor=N)

## Open Output Folders
btnOpenOutputs = mButton(frame_SetAndRun, btnText="Open Outputs Directory", RelY=updateBtnPosition())
# btnOpenOutputs = Button(frame_SetAndRun, text="Open Outputs Directory", width=15, height=2, font=boldFont, padx=0, pady=0)
# btnOpenOutputs.place(relx=0.5, rely=0.65, anchor=N)

root.mainloop()