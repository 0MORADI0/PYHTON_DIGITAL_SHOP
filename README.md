# Python Digital Shop

A desktop digital shop application built with Python, Tkinter, and SQLite.

## Overview

Python Digital Shop is a desktop application that provides a simple shopping experience with separate interfaces for customers and administrators.

The project demonstrates GUI development, database management, user authentication, and basic e-commerce functionality.

## Features

### Customer
- User registration and login
- Browse available products
- Search products
- Browse product categories
- Add products to cart
- Checkout and place orders
- View order history
- View order details

### Administrator
- Administrator authentication
- Add new products
- Add product categories
- Delete products
- Delete categories
- Manage product images

## Technologies

- Python
- Tkinter
- SQLite
- SQL
- Object-Oriented Programming

## Project Structure

```text
PYTHON_DIGITAL_SHOP/
│
└── tkinter shop last version/
    ├── admin.py
    ├── adminpanel.py
    ├── cart.py
    ├── dashbord.py
    ├── database.py
    ├── login.py
    ├── main.py
    ├── product.py
    ├── signup.py
    ├── tkclass.py
    ├── shop.db
    └── images/
```

## Requirements

- Python 3.12 or newer
- Tkinter
- SQLite

Tkinter and SQLite are included with most standard Python installations.

## Installation

1. Download or clone this repository.
2. Open the project folder.
3. Configure the administrator environment variables.
4. Run the application:

```bash
python main.py
```

## Administrator Configuration

Set the following environment variables before running the application:

```text
SHOP_ADMIN_NAME
SHOP_ADMIN_PASSWORD
```

Do not publish administrator credentials or passwords in the source code.

## Notes

- Product images are stored in the `images` directory.
- The SQLite database is created automatically when the application starts.
- This project is developed as a learning project demonstrating Python desktop application development.

## Author

0MORADI0

GitHub: https://github.com/0MORADI0
