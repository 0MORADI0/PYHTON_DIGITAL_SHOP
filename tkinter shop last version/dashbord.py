from tkclass import *
from tkinter import messagebox
from database import *
from cart import *
import os

class dashbord(tkclass):
    def __init__(self,usrname,pw):
        self.db=database()
        self.user_id=self.db.get_user_id(usrname,pw)
        self.usrname=usrname
        self.pw=pw
        self.dashcart=cart()
    def dash_window(self):
        self.dash = tkclass("DASHBOARD", "700x400", False)
        self.dash.configure(bg="#0B1020")
        self.dash.label("DIGITAL SHOP",x=240, y=35,fg="#00E5F0",font=("Segoe UI", 24, "bold"))
        self.dash.label(f"Welcome,{self.usrname}",x=250, y=85,fg="#FFFFFF",font=("Segoe UI", 12))
        buttons = [("PRODUCTS",100,140,lambda: (self.dash.hide_window(), self.product_window())),("CART",390,140,lambda: self.dashcart.cart_window(self.checkout)),("CATEGORIES",100,245,lambda: (self.dash.hide_window(), self.category_window())),("ORDERS",390,245,lambda:(self.dash.hide_window(),self.orders_window()))]
        for text,x,y,command in buttons:
            self.dash.button(text,command=command,x=x,y=y,width=22,height=3,bg="#18233F",fg="#FFFFFF",cursor="hand2",cursorenter="#00E5F0",relief="flat",bd=0,font=("Segoe UI", 13, "bold"))

        self.dash.mainloop()
    def product_window(self,back_button_disable=False):
        products=self.db.get_products()
        product_window=tkclass("PRODUCTS","700x400",False,color="#263653")
        
        canvas=Canvas(product_window)
        scrollbar=Scrollbar(product_window,orient="vertical",command=canvas.yview)
        product_frame=Frame(product_window,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        def show_products(products):
            for widget in product_frame.winfo_children():
                widget.destroy()
            for product in products:
                product_id=product[0]
                product_name=product[1]
                product_price=product[2]
                product_stock=product[3]
                product_category=product[4]
                product_image=PhotoImage(file=self.resolve_image_path(product[5]),master=product_window)
                product_image=product_image.subsample(1,1)
                frame = Frame(product_frame,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
                frame.pack(fill="x",padx=10,pady=10)
                image_label=Label(frame,image=product_image)
                image_label.grid(row=0,column=0,rowspan=5,padx=10)
                image_label.image=product_image
                Label(frame,text=f"NAME:{product_name}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=0, column=1, sticky="w", pady=5)
                Label(frame,text=f"|price:{product_price}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=1,column=1,sticky="w",pady=3)
                Label(frame,text=f"|stock:{product_stock}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=2,column=1,sticky="w",pady=3)
                Label(frame,text=f"|category:{product_category}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=3,column=1,sticky="w",pady=3)
                ATC_btn = Button(frame,text="ADD TO CART",command=lambda pid=product_id,pname=product_name,pprice=product_price:self.dashcart.add_to_cart(pid,pname,pprice,1),cursor="hand2",bg="#00BFA6",fg="#0B1020",activebackground="#00E5F0",activeforeground="#0B1020",height=2,width=15,font=("Segoe UI", 11, "bold"),relief="flat",bd=0)
                ATC_btn.bind("<Enter>",lambda event,btn=ATC_btn:btn.configure(bg="#00E5F0"))
                ATC_btn.bind("<Leave>",lambda event,btn=ATC_btn:btn.configure(bg="#00BFA6"))
                ATC_btn.grid(row=0,column=2,padx=25,sticky="e")
                
        product_window.entry("search",width=500)
        def search():
            text=product_window.entryinput("search")
            if text=="":
                products=self.db.get_products()
            else:
                products=self.db.search_products(text)
            show_products(products)
        product_window.button(text="SEARCH",command=search,bg="green",fg="red",x=325)
        show_products(self.db.get_products())
        if back_button_disable is False:
            product_window.button(text="BACK",command=lambda:product_window.back_window(self.dash),bg="red",fg="green",x=10)
            product_window.protocol("WM_DELETE_WINDOW",lambda:None)
        product_window.mainloop()
    def orders_window(self):
        orders_window=tkclass("ORDERS","700x200",False,color="#263653")
        orders_window.protocol("WM_DELETE_WINDOW",lambda:None)
        if self.user_id is None:
            return
        orders=self.db.get_orders(self.user_id)
        canvas=Canvas(orders_window)
        scrollbar=Scrollbar(orders_window,orient="vertical",command=canvas.yview)
        product_frame=Frame(orders_window,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        for order in orders:
            order_id=order[0]
            order_date=order[1]
            frame=Frame(product_frame,bg="#18233F",padx=150,pady=40,highlightbackground="#263653",highlightthickness=1)
            frame.pack()
            Label(frame,text=f"ORDER ID : {order_id}\nDATE : {order_date}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 20, "bold")).grid(row=0,column=0,rowspan=5,padx=10)
            DETAILS_btn=Button(frame,text="DETAILS...",command=lambda oid = order_id : self.show_details(oid),bg="green",fg="red",font=("Segoe UI",14,"bold"),relief="raised",bd=5)
            DETAILS_btn.bind("<Enter>",lambda event,btn=DETAILS_btn: btn.configure(bg="#00E5F0"))
            DETAILS_btn.bind("<Leave>",lambda event,btn=DETAILS_btn: btn.configure(bg="green"))
            DETAILS_btn.grid()
            
        orders_window.button(text="BACK",command=lambda:orders_window.back_window(self.dash),bg="red",fg="green",height=10,width=20)
        orders_window.mainloop()
    def checkout(self):
        if self.user_id is None:
            return
        order_id=self.db.add_order(self.user_id,"1405")
        for item in self.dashcart.cart:
            stock=self.db.get_product_stock(item["product_id"])
            if item["product_quantity"]>stock:
                messagebox.showerror("ERROR",f"LACK OF STOCKS FOR {item["product_name"]}")
                return
            self.db.add_order_items(order_id,item["product_id"],item["product_quantity"])
            self.db.update_stock(item["product_id"],item["product_quantity"])
        self.dashcart.clear_cart()
    def show_details(self,orderid):
        detail_window=tkclass("PRODUCT DETAILS","700x400",False,color="#18233F")
        items=self.db.get_order_items(orderid)
        total=0
        canvas=Canvas(detail_window)
        scrollbar=Scrollbar(detail_window,orient="vertical",command=canvas.yview)
        product_frame=Frame(detail_window,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set,bg="#18233F")
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        for item in items:
            name=item[1]
            price=item[2]
            quantity=item[3]
            line_total= price * quantity
            total+=line_total
            frame=Frame(product_frame,bg="#18233F",padx=200,pady=40,highlightbackground="#263653",highlightthickness=1)
            frame.pack()
            Label(frame,text=f"NAME : {name}\nPRICE : {price} $\nQUANTITY : x {quantity}\nLINE TOTAL : {line_total} $",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=0,column=10,sticky="w",pady=30)
        detail_window.label(f"TOTAL\n{total}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 20, "bold"))
        detail_window.mainloop()
    def category_window(self):
        category_window=tkclass("CATEGORIES","700x400",False,color="#F8F8F8")
        category_window.protocol("WM_DELETE_WINDOW",lambda:None)
        category_window.button("ALL PRODUCTS",command=lambda:self.product_window(True),bg="blue",fg="red")
        categories=self.db.get_categories()
        canvas=Canvas(category_window)
        scrollbar=Scrollbar(category_window,orient="vertical",command=canvas.yview)
        product_frame=Frame(category_window,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        for category in categories:
            cid=category[0]
            cname=category[1]
            frame=Frame(product_frame,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
            frame.pack(fill="x",padx=10,pady=10)
            CNAME_btn=Button(frame,text=cname,command=lambda cid=cid:self.category_products(cid),bg="green",fg="black",width=53,height=8,font=("Segoe UI",14,"bold"),relief="raised",bd=5)
            CNAME_btn.bind("<Enter>",lambda event,btn=CNAME_btn: btn.configure(bg="#00E5F0"))
            CNAME_btn.bind("<Leave>",lambda event,btn=CNAME_btn: btn.configure(bg="green"))
            CNAME_btn.pack(anchor="center")
        category_window.button(text="BACK",command=lambda:category_window.back_window(self.dash),bg="red",fg="green")
        category_window.mainloop()
    def category_products(self,cid):
        cproduct_window=tkclass("CATEGORY PRODUCTS","700x400",False)
        cproducts=self.db.get_product_by_category(cid)
        canvas=Canvas(cproduct_window)
        scrollbar=Scrollbar(cproduct_window,orient="vertical",command=canvas.yview)
        product_frame=Frame(cproduct_window,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        for cproduct in cproducts:
            cp_id=cproduct[0]
            cp_name=cproduct[1]
            cp_price=cproduct[2]
            cp_stock=cproduct[3]
            cp_category=cproduct[4]
            product_image=PhotoImage(file=self.resolve_image_path(cproduct[5]),master=cproduct_window)
            product_image=product_image.subsample(1,1)
            frame = Frame(product_frame,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
            frame.pack(fill="x",padx=10,pady=10)
            image_label=Label(frame,image=product_image)
            image_label.grid(row=0,column=0,rowspan=5,padx=10)
            image_label.image=product_image
            Label(frame,text=f"|NAME:{cp_name}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=0,column=1,sticky="w",pady=3)
            Label(frame,text=f"|price:{cp_price}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=1,column=1,sticky="w",pady=3)
            Label(frame,text=f"|stock:{cp_stock}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=2,column=1,sticky="w",pady=3)
            Label(frame,text=f"|category:{cp_category}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 12, "bold")).grid(row=3,column=1,sticky="w",pady=3)
            CATC_btn = Button(frame,text="ADD TO CART",command=lambda pid=cp_id,pname=cp_name,pprice=cp_price:self.dashcart.add_to_cart(pid,pname,pprice,1),cursor="hand2",bg="#00BFA6",fg="#0B1020",activebackground="#00E5F0",activeforeground="#0B1020",height=2,width=15,font=("Segoe UI", 11, "bold"),relief="flat",bd=0)
            CATC_btn.bind("<Enter>",lambda event,btn=CATC_btn:btn.configure(bg="#00E5F0"))
            CATC_btn.bind("<Leave>",lambda event,btn=CATC_btn:btn.configure(bg="#00BFA6"))
            CATC_btn.grid(row=0,column=2,padx=25,sticky="e")
            
        cproduct_window.mainloop()
    def resolve_image_path(self,image_path):
        base_dir=os.path.dirname(os.path.abspath(__file__))
        if image_path and os.path.isabs(image_path):
            return image_path
        if image_path:
            path=os.path.join(base_dir,image_path)
            if os.path.exists(path):
                return path
            old_path=os.path.join(base_dir,"images",os.path.basename(image_path))
            if os.path.exists(old_path):
                return old_path
        return os.path.join(base_dir,"images","DEFAULT.png")
    def search_products(self,text):
        products=self.db.search_products(text)