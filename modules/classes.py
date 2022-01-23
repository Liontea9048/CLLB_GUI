import tkinter.ttk as ttk
from tkinter import *
import tkinter.font as ft
from modules.variables import *

class mLabel(Label):
    
    def __init__(self, masterFrame, expText="Type Explanation", expXPos=labelPosX, \
        expYPos=pos_y, unitsText="", unitsXPos=unitsXpos, unitsYPos=pos_y):
        self = Label(masterFrame, text=expText, justify="left");
        self.place(x=expXPos, y=expYPos);
        
        self = Label(masterFrame, text=unitsText);
        self.place(x=unitsXPos, y=unitsYPos);
        
class mEntry(Entry):
    
    def __init__(self, masterFrame, initVar=0, xPos=varInputXpos, yPos=30, flages="normal", twoLines=0):
        self = Entry(masterFrame, width=10, relief="solid", bd=2, justify="right");
        if twoLines: self.place(x=xPos, y=yPos+5);
        else: self.place(x=xPos, y=yPos)
        
        # For PTI
        if flages == "PTI":
            self.PTI_txt_var = StringVar()
            if initVar =="0.0" or initVar == "0." or initVar == "0":
                self.PTI_txt_var.set("Disable")
            else:
                self.PTI_txt_var.set(initVar)
            self.config(textvariable=self.PTI_txt_var)
            def TurnToDisable(event):
                if self.get() == "0.0" or self.get() == "0." or  self.get() == "0":
                    self.PTI_txt_var.set("Disable")
            self.bind("<Leave>", TurnToDisable)
            self.bind("<Return>", TurnToDisable)
            
        else:
            self.insert(0, initVar);
        
class mCombobox(ttk.Combobox):
    
    def __init__(self, masterFrame, initIndex, xPos=varInputXpos, yPos=10, flags="RLO"):
        self = ttk.Combobox(masterFrame, width = 8, height = 7,\
                state="readonly", justify="right");
        
        if flags == "RLO":
            # Reocording length options
            self.Recording_length_options = ["128 ns", "256 ns", \
                "512 ns", "1 \u03BCs", "2 \u03BCs", "4 \u03BCs", "8 \u03BCs"];
            self.RLO_index = ["1","2","3","8","16","32","64"];
            self.config(values=self.Recording_length_options)
            self.current(self.RLO_index.index(initIndex))
            
        elif flags == "IPP":
            # Input Pulse Polarity, 0 for negative and 1 for positive
            self.IPP_lst = ["Negative", "Positive"]
            self.IPP_index = ["0", "1"]
            self.config(values=self.IPP_lst)
            self.current(self.IPP_index.index(initIndex))
            
        elif flags == "AM":
            self.AM_lst = ["Raw", "Filtered"]
            self.AM_index = ["0", "1"]
            self.config(values=self.AM_lst)
            self.current(self.AM_index.index(initIndex))
            
        self.place(x=xPos, y=yPos-2)

class mButton(Button):

    def __init__(self, masterFrame, btnText="Type Text", RelX=btnRelX, RelY=btnRelY):
        boldFont = ft.Font(size = 15, weight = "bold")
        self = Button(masterFrame, text=btnText, width=15, height=2, font=boldFont, padx=0, pady=0)
        self.place(relx=RelX, rely=RelY, anchor=N)
        
        
        