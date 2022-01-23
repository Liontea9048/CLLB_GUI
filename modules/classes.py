import tkinter.ttk as ttk
from tkinter import *
import tkinter.font as ft
from modules.variables import *

class mEntry(Entry):
    def __init__(self, masterFrame, initVar, xPos=varInputXpos, yPos=10):
        self = Entry(masterFrame, width=10, relief="solid", bd=2, justify="right");
        self.insert(0, initVar);
        self.place(x=xPos, y=yPos);
        
    