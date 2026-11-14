from database import *
from tkclass import *
from tkinter import filedialog
import os
import struct
from pathlib import Path
import shutil
import uuid
from admin import *

class adminpanel(tkclass):
    def __init__(self):
        self.db=database()
    def verify(self,name,pw,previous_window=None):
        if self.db.admin_log(name,pw):
            self.admin_window(previous_window)
            return True
        return False
    def admin_window(self,previous_window=None):
        previous_window.hide_window()
        self.admin_window=tkclass("ADMIN PANEL","700x400",False)
        self.admin_window.button("ADD PRODUCT",command=lambda:self.add_products_window())
        self.admin_window.button("ADD CATEGORY",command=lambda:self.add_category_window())
        self.admin_window.button("DELETE CATEGORY",command=lambda:self.delete_category_window())
        self.admin_window.button("DELETE PRODUCT",command=lambda:self.delete_product_window())
        self.admin_window.mainloop()
    def add_products_window(self):
        self.admin_window.hide_window()
        add_products_win=tkclass("ADD PRODUCTS","700x500",False)
        add_products_win.protocol("WM_DELETE_WINDOW",lambda:None)
        add_products_win.label("PRODUCT NAME:")
        add_products_win.entry("name")
        add_products_win.label("PRODUCT PRICE:")
        add_products_win.entry("price")
        add_products_win.label("PRODUCT STOCK:")
        add_products_win.entry("stock")
        add_products_win.label("PRODUCT CATEGORY:")
        add_products_win.entry("category")
        add_products_win.label("PRODUCT IMAGE:")
        add_products_win.entry("image")
        BASE_DIR=Path(__file__).resolve().parent
        IMAGE_DIR=BASE_DIR / "images"
        DEFAULT_IMAGE="images/DEFAULT.png"
        def image_verify():
            file=filedialog.askopenfilename(title="choose product image",filetypes=[("Image Files","*.png *.gif")])
            if file:
                with open(file,"rb") as img:
                    img.seek(16)
                    width,height=struct.unpack(">II",img.read(8))
                if width==250 and height==175:
                    IMAGE_DIR.mkdir(exist_ok=True)
                    filename=f"{uuid.uuid4().hex}.png"
                    destination=IMAGE_DIR / filename
                    shutil.copy2(file,destination)
                    file=f"images/{filename}"
                    messagebox.showinfo("image size verifier","image accepted")
                else:
                    file=DEFAULT_IMAGE
                    messagebox.showerror("image size verifier",f"image declined.\n YOUR IMAGE SIZE IS {width}x{height}.\nYOU SHOULD CHOOSE A 250X175 IMAGE")
                    messagebox.showinfo("IMAGE","DEFAULT IMAGE SET")
                add_products_win.entryoutput("image",file)
        add_products_win.button("...",command=image_verify,x=500,y=300)
        def submit_button():
            if not add_products_win.entryinput("image"):
                add_products_win.entryoutput("image",DEFAULT_IMAGE)
            self.add_products(add_products_win.entryinput("name"),add_products_win.entryinput("price"),add_products_win.entryinput("stock"),add_products_win.entryinput("category"),add_products_win.entryinput("image"))
            return
        add_products_win.button("SUBMIT",command=submit_button)
        add_products_win.button("BACK",command=lambda:add_products_win.back_window(self.admin_window))
        add_products_win.mainloop()
    def add_category_window(self):
        self.admin_window.hide_window()
        add_category_window=tkclass("ADD CATEGORY","700x400",False)
        add_category_window.protocol("WM_DELETE_WINDOW",lambda:None)
        add_category_window.label("CATEGORY NAME:")
        add_category_window.entry("category name")
        add_category_window.button("SUBMIT",command=lambda:self.add_category(add_category_window.entryinput("category name")))
        add_category_window.button("BACK",command=lambda:add_category_window.back_window(self.admin_window))
        add_category_window.mainloop()
    def delete_category_window(self):
        self.admin_window.hide_window()
        delete_category_window=tkclass("DELETE CATEGORY","700x400",False)
        delete_category_window.protocol("WM_DELETE_WINDOW",lambda:None)
        delete_category_window.label("CATEGORY NAME:")
        delete_category_window.entry("CATEGORY NAME")
        delete_category_window.button("DELETE",command=lambda:self.delete_category(delete_category_window.entryinput("CATEGORY NAME")))
        delete_category_window.button("BACK",command=lambda:delete_category_window.back_window(self.admin_window))
        delete_category_window.mainloop()
    def delete_product_window(self):
        self.admin_window.hide_window()
        delete_product_window=tkclass("DELETE CATEGORY","700x400",False)
        delete_product_window.protocol("WM_DELETE_WINDOW",lambda:None)
        delete_product_window.label("PRODUCT NAME:")
        delete_product_window.entry("PRODUCT NAME")
        delete_product_window.label("PRODUCT CATEGORY:")
        delete_product_window.entry("PRODUCT CATEGORY")
        delete_product_window.button("DELETE",command=lambda:self.delete_product(delete_product_window.entryinput("PRODUCT NAME"),delete_product_window.entryinput("PRODUCT CATEGORY")))
        delete_product_window.button("BACK",command=lambda:delete_product_window.back_window(self.admin_window))
        delete_product_window.mainloop()
    def add_products(self,name,price,stock,category_name,image):
        try:
            price=float(price)
            stock=int(stock)
        except ValueError:
            messagebox.showerror("ATTENTION","PRICE AND STOCK SHOULD BE INTEGER NOT A STRING")
            return
        if price<0 or stock<0:
            messagebox.showerror("ATTENTION","YOU SHOULD ENTER A POSITIVE NUMBER NOT A NEGATIVE ONE")
            return
        name=name.upper()
        category_name=category_name.upper()
        self.db.add_products(name,price,stock,category_name,image)
    def add_category(self,name):
        name=name.upper()
        if not self.db.add_category(name):
            messagebox.showinfo("INFO","CATEGORY ALREADY EXISTED")
            return
        messagebox.showinfo("INFO","CATEGORY ADDED")
    def delete_category(self,name):
        name=name.upper()
        self.db.delete_category(name)
    def delete_product(self,name,category_name):
        name=name.upper()
        category_name=category_name.upper()
        self.db.delete_product(name,category_name)