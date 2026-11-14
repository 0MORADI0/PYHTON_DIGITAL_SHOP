from tkinter import *
from tkinter import Tk
import tkinter as tk
import webbrowser
class tkclass(tk.Tk):
    def __init__(self,NAME,geometry=None,resizable=None,color="#0B1020"):
        super().__init__()
        self.title(NAME)
        self.geometry(geometry)
        self.resizable(resizable,resizable)
        self.configure(bg=color)
        self.vars={}
    def button(self,text,command=None,x=None,y=None,row=None,column=None,sticky=None,pady=None,cursorenter="#16F3FF",bg="#4DDBD2",font=("Segoe UI",14,"bold"),relief="flat",bd=5,**kwargs):
        btn=Button(self,text=text,command=command,bg=bg,font=font,relief=relief,bd=bd,**kwargs)
        btn.bind("<Enter>",lambda event: btn.configure(bg=cursorenter))
        btn.bind("<Leave>",lambda event: btn.configure(bg=bg))
        if x is None and y is None and row is None and column is None and sticky is None and pady is None:
            btn.pack()
            return
        if y is not None or x is not None:
            btn.place(x=x,y=y)
            return
        btn.grid(row=row,column=column,sticky=sticky,pady=pady)
    def label(self,text,x=None,y=None,row=None,column=None,sticky=None,pady=None,bg="#0B1020",fg="#00E5F0",font=("Segoe UI",14,"bold"),**kwargs):
        lbl=Label(self,text=text,bg=bg,fg=fg,font=font,**kwargs)
        if y is None and x is None and row is None and column is None and sticky is None and pady is None:
            lbl.pack()
            return
        if y is not None or x is not None:
            lbl.place(x=x,y=y)
            return
        lbl.grid(row=row,column=column,sticky=sticky,pady=pady)
    def entry(self,varname,show=None,bg="#191D30",fg="#FFFFFF",insertbackground="#00E5F0",font=("Segoe UI",16),justify="center",relief="flat",highlightthickness=2,highlightbackground="#00E5F0",highlightcolor="#B026FF",**kwargs):
        var=StringVar(self)
        self.vars[varname]=var
        self.ent=Entry(self,textvariable=var,show=show,bg=bg,fg=fg,insertbackground=insertbackground,font=font,justify=justify,relief=relief,highlightthickness=highlightthickness,highlightbackground=highlightbackground,highlightcolor=highlightcolor,**kwargs)
        self.ent.pack()
    def entryinput(self,varname):
        return self.vars[varname].get()
    def entryoutput(self,varname,output):
        return self.vars[varname].set(output)
    def frame(self,**kwargs):
        frame=Frame(self,**kwargs)
        frame.pack()
        return frame
    def hide_window(self):
        self.withdraw()
    def back_window(self,previous_window,is_short=True,x=300,y=150):
        self.destroy()
        previous_window.deiconify()
        if is_short is True:
            previous_window.label("SEE MY OTHER PROJECTS\nBY CLICKING BUTTON BLOW:",bg="#0B1020",fg="#00E5F0",font=("Segoe UI",14,"bold"),x=230,y=200)
            previous_window.button("click here",command=lambda:webbrowser.open("https://github.com/0MORADI0"),bg="#0B1020",fg="#00FFFF",cursorenter="#4E5252",font=("Segoe UI",14,"bold"),x=310,y=260)
        else:
            previous_window.label("SEE MY OTHER PROJECTS BY CLICKING BUTTON BLOW:",bg="#0B1020",fg="#00E5F0",font=("Segoe UI",14,"bold"),x=100,y=340)
            previous_window.button("click here",command=lambda:webbrowser.open("https://github.com/0MORADI0"),bg="#0B1020",fg="#00FFFF",cursorenter="#4E5252",font=("Segoe UI",14,"bold"),x=300,y=370)
    def close(self):
        self.destroy()
