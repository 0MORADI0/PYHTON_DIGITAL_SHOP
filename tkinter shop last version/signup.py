from tkclass import *
from tkinter import messagebox
from database import *
from dashbord import *
class signup(tkclass):
    def __init__(self):
        pass
    def set_var(self,username,password):
        has_int=False
        has_str=False
        has_upper=False
        has_lower=False
        has_special=False
        if username=="" or password=="":
            messagebox.showerror("ERROR","PLS FILL ALL THE ENTRIES")
            return
        if len(password)<6:
            messagebox.showinfo("PASSWORD","YOUR PASSWORD SHOULD BE UP TO 6 OR MORE LETTERS \n AND IT SHOULD INCLUDE: \n 1.LETTERS(BETTER TO USE BOTH UPPER AND LOWER) \n 2.SPECIAL ITEMS \n 3.NUMBERS \n AT LEAST YOU SHOULD USE TWO OF THIS ITEMS IN YOUR PASSWORD TO GET ACCEPTED \n BUT FOR A BETTER SECURITY I RECOMMEND YOU TO USE 3 OF THEM AND USE BOTH UPPER AND LOWER CASE LETTERS \n THANKS FOR ATTENTION")
            return
        for pw in password:
            if pw.isdigit():
                has_int=True
            elif pw.isalpha():
                has_str=True
                if pw.isupper():
                    has_upper=True
                elif pw.islower():
                    has_lower=True
            else:
                has_special=True
        if has_str is False and has_special is False and has_int or has_int is False and has_special is False and has_str or has_str is False and has_int is False and has_special:
            messagebox.showerror("ERROR","YOUR PASSWORD IS TOO WEAK")
            messagebox.showinfo("PASSWORD","YOUR PASSWORD SHOULD BE UP TO 6 OR MORE LETTERS \n AND IT SHOULD INCLUDE: \n 1.LETTERS(BETTER TO USE BOTH UPPER AND LOWER) \n 2.SPECIAL ITEMS \n 3.NUMBERS \n AT LEAST YOU SHOULD USE TWO OF THIS ITEMS IN YOUR PASSWORD TO GET ACCEPTED \n BUT FOR A BETTER SECURITY I RECOMMEND YOU TO USE 3 OF THEM AND USE BOTH UPPER AND LOWER CASE LETTERS \n THANKS FOR ATTENTION")
            return
        if has_int and has_str and has_special is False or has_int and has_special and has_str is False or has_str and has_special and has_int is False:
            messagebox.showinfo("WELCOME","YOUR PASSWORD IS ACCEPTABLE")
        elif has_special and has_str and has_int:
            messagebox.showinfo("WELCOME","YOUR PASSWORD IS GOOD")
        elif has_special and has_upper and has_lower and has_int:
            messagebox.showinfo("WELCOME","YOUR PASSWORD IS A MASTER PIECE")
        
        result=database().signin(username,password)
        if result:
            self.su.hide_window()
            dashbord(username,password).dash_window()
        else:
            messagebox.showerror("ERROR","NAME HAS BEEN ALREADY TAKEN")
    def signup_window(self,previous_window):
        self.su=tkclass("SIGNUP","700x400",False)
        self.su.protocol("WM_DELETE_WINDOW",lambda:None)
        self.su.label("PLS ENTER YOUR NAME AND YOUR PASSWORD:")
        self.su.label("NAME:")
        self.su.entry("fname")
        self.su.label("PASSWORD:")
        self.su.entry("pass",show="*")
        self.su.label("YOUR PASSWORD SHOULD BE UP TO 6 OR MORE LETTERS \n AND IT SHOULD INCLUDE: \n 1.LETTERS(BETTER TO USE BOTH UPPER AND LOWER) \n 2.SPECIAL ITEMS \n 3.NUMBERS \n AT LEAST YOU SHOULD USE TWO OF THIS ITEMS IN YOUR PASSWORD TO GET ACCEPTED \n BUT FOR A BETTER SECURITY I RECOMMEND YOU TO USE 3 OF THEM AND USE BOTH UPPER AND LOWER CASE LETTERS \n THANKS FOR ATTENTION",font=("Segoe UI",9,"bold"))
        self.su.button("SUBMIT",command=lambda:self.set_var(self.su.entryinput("fname"),self.su.entryinput("pass")),cursor="hand2")
        self.su.button(text="BACK",command=lambda:self.su.back_window(previous_window,is_short=False))
