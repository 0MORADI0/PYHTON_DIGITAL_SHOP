from tkinter import messagebox
from tkclass import *

class cart:
    def __init__(self):
        self.cart=[]
    def add_to_cart(self,productid,productname,productprice,productquantity):
        for item in self.cart:
            if item["product_id"]==productid:
                return self.update_quantity(productid,item["product_quantity"]+productquantity)
        self.cart.append({"product_id":productid,"product_name":productname,"product_price":productprice,"product_quantity":productquantity})
    def increase_quantity(self,pid):
        for item in self.cart:
            if item["product_id"]==pid:
                self.update_quantity(pid,item["product_quantity"]+1)
                return
    def decrease_quantity(self,pid):
        for item in self.cart:
            if item["product_id"]==pid:
                if item["product_quantity"]>1:
                    nquantity=item["product_quantity"]-1
                    if nquantity<=0:
                        self.remove_from_cart(pid)
                    else:
                        self.update_quantity(pid,nquantity)
                return
    def remove_from_cart(self,productid):
        for items in self.cart:
            if items["product_id"]==productid:
                self.cart.remove(items)
                return
    def update_quantity(self,productid,quantity):
        for items in self.cart:
            if items["product_id"]==productid:
                items["product_quantity"]=quantity
                return True
        return False
    def cart_total(self):
        total=0
        for item in self.cart:
            total+=(item["product_price"]*item["product_quantity"])
        return total
    def clear_cart(self):
        self.cart.clear()
    def cart_window(self,checkout=None):
        if self.cart == []:
            messagebox.showerror("ERROR","PLEASE ADD SOMETHING")
            return
        self.cartwin=tkclass("CART","700x200",False,color="#263653")
        canvas=Canvas(self.cartwin)
        scrollbar=Scrollbar(self.cartwin,orient="vertical",command=canvas.yview)
        product_frame=Frame(self.cartwin,bg="#18233F",padx=15,pady=12,highlightbackground="#263653",highlightthickness=1)
        canvas.create_window((0,0),window=product_frame,anchor="nw")
        product_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        for item in self.cart:
            productframe=Frame(product_frame,bg="#18233F",padx=200,pady=12,highlightbackground="#263653",highlightthickness=1)
            productframe.pack()
            Label(productframe,text=f"name:{item["product_name"]}\nprice:{item["product_price"]}\nquantity:{item["product_quantity"]}",fg="#00E5F0",bg="#18233F",font=("Segoe UI", 20, "bold")).pack()
            CART_btn=Button(productframe,text="remove",command=lambda id=item["product_id"]:self.remove_and_refresh(id),bg="red",font=("Segoe UI",14,"bold"),relief="raised",bd=5)
            CART_btn.bind("<Enter>",lambda event,btn=CART_btn: btn.configure(bg="#CC5CDE"))
            CART_btn.bind("<Leave>",lambda event,btn=CART_btn: btn.configure(bg="red"))
            CART_btn.pack()
        
        self.cartwin.button("CHECKOUT",command=lambda:(checkout(),self.cartwin.close()),bg="green",fg="red",height="10")
        self.cartwin.mainloop()
    def remove_and_refresh(self,id):
        self.remove_from_cart(id)
        self.cartwin.close()
    def clean(self):
        self.cart.clear()
