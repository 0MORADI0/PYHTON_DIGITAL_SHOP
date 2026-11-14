from tkclass import *
from signup import *
from login import *
from dashbord import *
from product import *

main=tkclass("win","700x450",False)
signup=signup()
login=login()

main.label("WELCOME TO MY APP DEAR USER")
main.label("please choose a way blow to continue")
main.button("SIGNUP",command=lambda:(main.hide_window(),signup.signup_window(main)),height="10",width="20",x=400,y=65,bg="green",fg="blue",cursor="hand2",cursorenter="#00E5F0")
main.button("LOGIN",command=lambda:(main.hide_window(),login.login_window(main)),height="10",width="20",x=100,y=65,bg="red",fg="green",cursor="hand2",cursorenter="#FF01BB")
main.mainloop()