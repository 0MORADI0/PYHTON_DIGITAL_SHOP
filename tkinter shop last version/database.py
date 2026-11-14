from tkinter import messagebox
from sqlite3 import *
import sqlite3
import hashlib
from admin import *

class database:
    def __init__(self):
        self.connection=sqlite3.connect("shop.db",check_same_thread=False)
        self.connection.row_factory=sqlite3.Row
        self.cursor=self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE NOT NULL);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,price REAL NOT NULL,stock INTEGER NOT NULL,category_id INTEGER NOT NULL,FOREIGN KEY (category_id) REFERENCES categories(id));""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,order_date TEXT NOT NULL,order_status TEXT NOT NULL,FOREIGN KEY (user_id) REFERENCES users(id));""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS order_items(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,product_id INTEGER NOT NULL,quantity INTEGER NOT NULL,FOREIGN KEY (order_id) REFERENCES orders(id),FOREIGN KEY (product_id) REFERENCES products(id));""")
        if adminpassword:
            self.cursor.execute("INSERT INTO users(name,password,role) VALUES(?,?,'admin') ON CONFLICT(name) DO UPDATE SET password=excluded.password,role='admin';",
                                (adminname,self.hash_pass(adminpassword)))
        self.cursor.execute("PRAGMA table_info(products)")
        columns=[column[1] for column in self.cursor.fetchall()]
        if "image" not in columns:
            self.cursor.execute("""ALTER TABLE products ADD COLUMN image TEXT""")
            self.connection.commit()
        self.connection.commit()
    def hash_pass(self,password):
        return hashlib.sha256(password.encode()).hexdigest()
    def signin(self,name,password):
        try:
            password=self.hash_pass(password)
            self.cursor.execute("INSERT INTO users(name,password,role) VALUES (?,?,?);",
                            (name,password,"user"))
            self.connection.commit()
            return True
        except:
            self.connection.rollback()
            return False
    def login(self,name,password):
        password=self.hash_pass(password)
        self.cursor.execute("SELECT DISTINCT name FROM users WHERE name=? AND password=? AND role = ?;",
                                (name,password,"user"))
        result=self.cursor.fetchone()
        if result:
            return True
        else:
            return False
    def get_user_id(self,name,pw):
        pw=self.hash_pass(pw)
        self.cursor.execute("SELECT id FROM users WHERE name=? AND password=?;",
                            (name,pw))
        result=self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def add_category(self,name):
        try:
            self.cursor.execute("INSERT INTO categories(name) VALUES (?);",
                                (name,))
            self.connection.commit()
            return True
        except:
            self.connection.rollback()
            return False
    def delete_category(self,name):
        self.cursor.execute("SELECT id FROM categories WHERE name=?;",
                            (name,))
        result=self.cursor.fetchone()
        if result is None:
            messagebox.showerror("ERROR",f"{name} NOT IN CATEGORIES")
            return
        category_id=result[0]
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE category_id=?;",
                            (category_id,))
        products=self.cursor.fetchone()
        products_count=products[0]
        if products_count>0:
            anser=messagebox.askyesno("ARE YOU SURE",f"ARE YOU SURE YOU WANT TO DELETE{name} AND {products_count} PRODUCTS IN IT?")
            if not anser:
               return
        self.cursor.execute("DELETE FROM products WHERE category_id=?;",
                            (category_id,))
        self.cursor.execute("DELETE FROM categories WHERE id=?;",
                            (category_id,))
        messagebox.showinfo("INFO",f"{name} CATEGORY DELETED SUCCSSFULY")
        self.connection.commit()
    def delete_product(self,name,category_name):
        self.cursor.execute("SELECT id from categories WHERE name=?;",
                            (category_name,))
        result=self.cursor.fetchone()
        if result is None:
            messagebox.showerror("ERROR",f"{category_name} NOT FOUND IN CATEGORIES")
            return
        category_id=result[0]
        self.cursor.execute("DELETE FROM products WHERE name=? AND category_id=?;",
                            (name,category_id))
        result=self.cursor.rowcount
        if result==0:
            messagebox.showerror("ERROR",f"{name} NOT FOUND ")
            return
        messagebox.showinfo("INFO",f"{name} DELTED FROM {category_name}")
        self.connection.commit()
    def add_products(self,name,price,stock,category_name,image):
        self.cursor.execute("SELECT id FROM categories WHERE name=?;",
                            (category_name,))
        category_result=self.cursor.fetchone()
        if category_result is None:
            if not self.add_category(category_name):
                return False
            self.cursor.execute("SELECT id FROM categories WHERE name=?;",
                                (category_name,))
            messagebox.showinfo("INFO",f"{category_name} NOT FOUND BUT WE MADE THIS CATEGORY FOR YOU")
            category_result=self.cursor.fetchone()
        category_id=category_result[0]
        self.cursor.execute("SELECT id FROM products WHERE name = ? AND category_id=?;",
                            (name,category_id))
        product_result=self.cursor.fetchone()
        if product_result:
            product_id=product_result[0]
            self.cursor.execute("UPDATE products SET stock=stock+? WHERE id=?;",
                                (stock,product_id))
            messagebox.showinfo("INFO",f"{name}'s stock updated")
        else:
            self.cursor.execute("INSERT INTO products(name,price,stock,category_id,image) VALUES (?,?,?,?,?);",
                                (name,price,stock,category_id,image))
            messagebox.showinfo("INFO","PRODUCT ADDED")
        self.connection.commit()
    def get_products(self):
        self.cursor.execute("SELECT products.id,products.name,products.price,products.stock,categories.name,products.image FROM products JOIN categories ON products.category_id=categories.id;")
        result=self.cursor.fetchall()
        return result
    def add_order(self,userid,orderdate):
            self.cursor.execute("INSERT INTO orders(user_id,order_date,order_status) VALUES (?,?,?);",
                            (userid,orderdate,"pending"))
            self.connection.commit()
            return self.cursor.lastrowid
    def add_order_items(self,orderid,productid,quantity):
        try:
            self.cursor.execute("INSERT INTO order_items(order_id,product_id,quantity) VALUES (?,?,?);",
                            (orderid,productid,quantity))
            self.connection.commit()
            return True
        except:
            return False
    def get_order_items(self,orderid):
        self.cursor.execute("SELECT order_items.product_id, products.name,products.price,order_items.quantity FROM order_items JOIN products ON order_items.product_id=products.id WHERE order_items.order_id= ?;",
                            (orderid,))
        return self.cursor.fetchall()
    def update_stock(self,pid,pquantity):
        self.cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?;",
                            (pquantity,pid))
        self.connection.commit()
    def get_product_stock(self,pid):
        self.cursor.execute("SELECT stock FROM products WHERE id = ?;",
                            (pid,))
        result=self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0
    def get_orders(self,uid):
        self.cursor.execute("SELECT id,order_date FROM orders WHERE user_id = ?;",
                            (uid,))
        return self.cursor.fetchall()
    def get_categories(self):
        self.cursor.execute("SELECT id,name FROM categories;")
        return self.cursor.fetchall()
    def get_product_by_category(self,cid):
        self.cursor.execute("SELECT products.id,products.name,products.price,products.stock,categories.name,products.image FROM products JOIN categories ON products.category_id = categories.id WHERE categories.id = ?;",
                            (cid,))
        return self.cursor.fetchall()
    def search_products(self,text):
        self.cursor.execute("SELECT products.id,products.name,products.price,products.stock,categories.name,products.image FROM products JOIN categories ON products.category_id=categories.id WHERE products.name LIKE ?;",
                            (f"%{text}%",))
        return self.cursor.fetchall()
    def admin_log(self,name,pw):
        pw=self.hash_pass(str(pw))
        self.cursor.execute("SELECT * FROM users WHERE name=? AND password=? AND role=?;",
                            (name,pw,"admin"))
        result=self.cursor.fetchall()
        if result:
            return result
        else:
            return None