import customtkinter as ctk
import os
import order
import logic
import data

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
username = ''
def enter_user():
    global username
    username = enteruser.get()
    password = enterpass.get()
    input_user = {"user": username,"password":password}
    return input_user

def show_password():
    if enterpass.cget('show') == "*":

        enterpass.configure(show = '')
        buttonsp.configure(text='😮')

    else:

        enterpass.configure(show = '*')
        buttonsp.configure(text='😑')

def multi_page(target_frame):

    main_frame.pack_forget()
    login_frame.pack_forget()

    target_frame.pack(fill='both',expand = True ,)

def check_pass():

    data = logic.logic_function(enter_user())
    if data:
        multi_page(main_frame)
    else:
        lableError.configure(text='Username หรือ Password ไม่ถูกต้อง')




app = ctk.CTk()

app.title("PyRestaurant")
app._set_appearance_mode("system")
app.geometry("500x600")

login_frame = ctk.CTkFrame(app,fg_color='transparent')
main_frame = ctk.CTkFrame(app,fg_color='transparent')

lable1 = ctk.CTkLabel(login_frame,
    text="Welcome To PyRestaurant",
    text_color="#00FF3C"
)
lable2 = ctk.CTkLabel(login_frame,
    text="Username "

)
lable3 = ctk.CTkLabel(login_frame,
    text="Password"
)
lableError = ctk.CTkLabel(login_frame,text='',text_color='#ff0000')

enteruser = ctk.CTkEntry(login_frame,placeholder_text="ใส่ Username ของคุณ")
enterpass = ctk.CTkEntry(login_frame,show='*',placeholder_text="ใส่ Password ของคุณ")

button = ctk.CTkButton(login_frame,
    text='Enter',
                       text_color="#fcfdfb",
                       fg_color="#5eff00",
                       hover_color='#ff0000',
                       command= check_pass
                       )

buttonback = ctk.CTkButton(
    login_frame, text='back',
    text_color="#f4f1f1",
    fg_color='#ff0000',
    hover_color="#1500ff",
    command= clearscreen
)
buttonsp = ctk.CTkButton(login_frame,text='😑',fg_color='transparent',hover=False,command=show_password)

login_frame.pack(pady=40, padx=40, fill="both", expand=True)
lable1.pack()
lableError.pack()
lable2.pack()
enteruser.pack()
lable3.pack()
enterpass.pack(pady = (10,0))
buttonsp.pack( pady = (0,5))
button.pack(pady = 10)
buttonback.pack()
enter_user()


'''frame main'''

lblmain1 = ctk.CTkLabel(main_frame,text=f'Hello {username}')
buttonlogout = ctk.CTkButton(main_frame,text='logout',hover_color='#ff0000',command=lambda : multi_page(login_frame))
lblmain1.pack()
buttonlogout.pack()

app.mainloop()
