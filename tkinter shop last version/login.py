from tkclass import *
from tkinter import messagebox
from database import *
from dashbord import *
from adminpanel import *

class login(tkclass):
    def __init__(self):
        pass
    def verify(self,name,password):
        if adminpanel().verify(name,password,self.log):
            return
        result=database().login(name,password)
        if result:
            self.log.hide_window()
            dashbord(name,password).dash_window()
        else:
            messagebox.showerror("ERROR","USER NOT FOUND")
    def login_window(self,previous_window):
        self.log=tkclass("LOGIN","700x400",False)
        self.log.protocol("WM_DELETE_WINDOW",lambda:None)
        self.log.label("PLS ENTER YOUR CURRENT NAME AND PASSWORD:")
        self.log.label("NAME:")
        self.log.entry("fname")
        self.log.label("PASSWORD:")
        self.log.entry("pass",show="*")
        
        self.log.button("SUBMIT",command=lambda:self.verify(self.log.entryinput("fname"),self.log.entryinput("pass")),cursor="hand2")
        self.log.button(text="BACK",command=lambda:self.log.back_window(previous_window,is_short=False))
        