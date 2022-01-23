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
lb_intro.place(x=10, y=10)

# ------------------------ Frame ------------------------
frame_var = LabelFrame(root, relief="solid", bd=2, text="VARIABLES", \
                        width=450, height=430, labelanchor="nw")
frame_var.place(x=10, y=pos_y)

# 1. Acquisition Time, in seconds -> this will be converted into ns in set files
Label(frame_var, text="Acquisiton Time").place(x=10,y=pos_y)
# Acq_time_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
# Acq_time_entry.insert(0, defaultVar[defaultVarIndex])
# Acq_time_entry.place(x=varInputXpos, y=pos_y)
Acq_time_entry = mEntry(frame_var, defaultVar[defaultVarIndex], yPos=pos_y)
Label(frame_var, text="s").place(x=unitsXpos, y=pos_y)

# 2. High Voltage in Voltes
# pos_y += 30; defaultVarIndex +=1;
pos_y, defaultVarIndex = updateYposAndIndex()

Label(frame_var, text="High Voltage").place(x=10,y=pos_y)
HV_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
HV_entry.insert(0, defaultVar[defaultVarIndex])
HV_entry.place(x=varInputXpos, y=pos_y)
Label(frame_var, text="V").place(x=unitsXpos,y=pos_y)

# 3. Recording Length
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="Recording Length").place(x=10,y=pos_y)
Recording_length_options = ["128 ns", "256 ns", "512 ns", "1 \u03BCs", "2 \u03BCs", "4 \u03BCs", "8 \u03BCs"]
RL_cmbox = ttk.Combobox(frame_var, width = 8, height=7, values=Recording_length_options, state="readonly", justify="right")
# recording length index list
RLO_index = ["1","2","3","8","16","32","64"]
RL_cmbox.current(RLO_index.index(defaultVar[defaultVarIndex]))
RL_cmbox.place(x=varInputXpos, y=pos_y-2)

# 4. Pedestal Trigger interval in ms, 0 for disable
pos_y+=30; defaultVarIndex +=1;
## define unit text change
def TurnToDisable(event):
    if PTI_entry.get() == "0.0" or PTI_entry.get() == "0." or  PTI_entry.get() == "0":
        PTI_txt_var.set("Disable")
PTI_txt_var = StringVar()

## Set PTI_txt_var to Disable or a number (if not 0)
if defaultVar[defaultVarIndex] == "0.0" \
    or defaultVar[defaultVarIndex] == "0." \
    or  defaultVar[defaultVarIndex] == "0":
        PTI_txt_var.set("Disable")
else:    
    PTI_txt_var.set(defaultVar[defaultVarIndex])
    
Label(frame_var, text="Pedestal Trigeer interval").place(x=10,y=pos_y)
PTI_entry = Entry(frame_var, width=10, textvariable=PTI_txt_var,relief="solid", bd=2, justify="right")
PTI_entry.place(x=varInputXpos, y=pos_y)
## ms or disabled
Label(frame_var, text="ms").place(x=unitsXpos,y=pos_y)
PTI_entry.bind("<Leave>", TurnToDisable)

# 5. ADC offset value (0-4095)
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="ADC Offset Value, Range: 0 - 4095").place(x=10,y=pos_y)
AO_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
AO_entry.insert(0, defaultVar[defaultVarIndex])
AO_entry.place(x=varInputXpos, y=pos_y)
Label(frame_var).place(x=unitsXpos,y=pos_y)

# 6. ADC waveform delay from trigger point, 0 ~ 8,000
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="ADC Waveform Delay from Trigger Point,\nRange: 0 - 8000", justify="left").place(x=10,y=pos_y)
AWD_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
AWD_entry.insert(0, defaultVar[defaultVarIndex])
AWD_entry.place(x=varInputXpos, y=pos_y+5)
Label(frame_var).place(x=unitsXpos,y=pos_y)

# 7. Discrimination Threshold, 1 ~ 4095
pos_y+=40; defaultVarIndex +=1;
Label(frame_var, text="Discrimination Threshold, \nRange: 1 - 4095", justify="left").place(x=10,y=pos_y)
DT_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
DT_entry.insert(0, defaultVar[defaultVarIndex])
DT_entry.place(x=varInputXpos, y=pos_y+5)
Label(frame_var).place(x=unitsXpos,y=pos_y)

# 8. Input Pulse Polarity, 0 = negative, 1 = positive
pos_y+=40; defaultVarIndex +=1;
Label(frame_var, text="Input Pulse Polarity", justify="left").place(x=10,y=pos_y)
IPP_lst = ["Negative", "Positive"]
IPP_cmbox = ttk.Combobox(frame_var, width = 8, height=7, values=IPP_lst, state="readonly", justify="right")
IPP_index = ["0", "1"]
IPP_cmbox.current(IPP_index.index(defaultVar[defaultVarIndex]))
IPP_cmbox.place(x=varInputXpos, y=pos_y-2)

# 9. Peak Sum Width in ns (8 ~ 8000 ns)
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="Peak Sum Width, Range: 8 - 8000", justify="left").place(x=10,y=pos_y)
PSW_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
PSW_entry.insert(0, defaultVar[defaultVarIndex])
PSW_entry.place(x=varInputXpos, y=pos_y)
Label(frame_var, text="ns").place(x=unitsXpos,y=pos_y)

# 10. ADC mode, 0 = raw, 1 = filtered
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="ADC Mode", justify="left").place(x=10,y=pos_y)
AM_lst = ["Raw", "Filtered"]
AM_cmbox = ttk.Combobox(frame_var, width = 8, height=7, values=AM_lst, state="readonly", justify="right")
AM_index = ["0", "1"]
AM_cmbox.current(AM_index.index(defaultVar[defaultVarIndex]))
AM_cmbox.place(x=varInputXpos, y=pos_y-2)

# 11. Peak to Tail Start Delay, 0 ~ 8000 ns
pos_y+=30; defaultVarIndex +=1;
Label(frame_var, text="Peak to Tail Start Delay,\nRange: 0 - 8000", justify="left").place(x=10,y=pos_y)
PTSD_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
PTSD_entry.insert(0, defaultVar[defaultVarIndex])
PTSD_entry.place(x=varInputXpos, y=pos_y+5)
Label(frame_var, text="ns").place(x=unitsXpos,y=pos_y+5)

# 12. Tail/Body Ratio Threshold
pos_y+=40; defaultVarIndex +=1;
Label(frame_var, text="Tail/Body Ratio Threshold", justify="left").place(x=10,y=pos_y)
PTSD_entry = Entry(frame_var, width=10, relief="solid", bd=2, justify="right")
PTSD_entry.insert(0, defaultVar[defaultVarIndex])
PTSD_entry.place(x=varInputXpos, y=pos_y)

# ------------------------ Set and Run Frame ------------------------ #

# ------------------------ Frame - Right side
frame_SetAndRun = LabelFrame(root, relief="solid", bd=2, text="SET and RUN", \
                        width=250, height=430,labelanchor="nw")
frame_SetAndRun.place(x=btnFramePadX, y=btnFramePadY)

# ------------------------ Button for running the set up.
## Font Style
boldFont = ft.Font(size = 15, weight = "bold")

## Modify the setup.txt
btnModifySetupTxt = Button(frame_SetAndRun, text="Modify Setup.txt", width=15, height=2, font=boldFont, padx=0, pady=0)
btnModifySetupTxt.place(relx=0.5, rely=0.05, anchor=N)

## Execute set*.exe
btnExecSet = Button(frame_SetAndRun, text="Execute Set.exe", width=15, height=2, font=boldFont, padx=0, pady=0)
btnExecSet.place(relx=0.5, rely=0.20, anchor=N)

## Execute run*.exe
btnExecRun = Button(frame_SetAndRun, text="Execute Run.exe", width=15, height=2, font=boldFont, padx=0, pady=0)
btnExecRun.place(relx=0.5, rely=0.35, anchor=N)

## Open input Folders
btnOpenInputs = Button(frame_SetAndRun, text="Open Inputs Directory", width=15, height=2, font=boldFont, padx=0, pady=0)
btnOpenInputs.place(relx=0.5, rely=0.50, anchor=N)

## Open Output Folders
btnOpenOutputs = Button(frame_SetAndRun, text="Open Outputs Directory", width=15, height=2, font=boldFont, padx=0, pady=0)
btnOpenOutputs.place(relx=0.5, rely=0.65, anchor=N)

root.mainloop()