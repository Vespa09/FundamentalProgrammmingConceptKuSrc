import customtkinter as ctk
import os
import order
import logic
import data

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_password():
    if enterpass.cget('show') == "*":

        enterpass.configure(show = '')
        buttonsp.configure(text='😮')

    else:

        enterpass.configure(show = '*')
        buttonsp.configure(text='😑')

def show_passwordRg1():
    if enterpass.cget('show') == "*":

        entryrg2.configure(show = '')
        buttonRgsp1.configure(text='😮')

    else:

        entryrg2.configure(show = '*')
        buttonRgsp1.configure(text='😑')

def show_passwordRg2():
    if enterpass.cget('show') == "*":

        entryrg3.configure(show = '')
        buttonRgsp2.configure(text='😮')

    else:

        entryrg3.configure(show = '*')
        buttonRgsp2.configure(text='😑')

def multi_page(target_frame):

    main_frame.pack_forget()
    login_frame.pack_forget()
    register_frame.pack_forget()
    Booking.pack_forget()
    Order.pack_forget()
    Check_Bill.pack_forget()

    target_frame.pack(fill='both',expand = True ,)

def check_pass():
    username = enteruser.get()
    password = enterpass.get()
    input_user = {"user": username,"password":password}

    data = logic.logic_function(input_user)
    if data:
        multi_page(main_frame)
    else:
        lableError.configure(text='Username หรือ Password ไม่ถูกต้อง')

def register():
    usernameRg = entryrg1.get()
    password1 = entryrg2.get()
    password2 = entryrg3.get()
    firstname = entryrg4.get()
    lastname = entryrg5.get()
    phone = entryrg6.get()
    email = entryrg7.get()
        
    if password1 != password2:
        lblRgError.configure(text = 'รหัสผ่านไม่ตรงกัน')
        return None
    
    if email == '':
        email = None

    regis = data.register_user(usernameRg,password1,firstname,lastname,phone,email)
    if regis :
        lblRgError.configure(text='Register successful',text_color="#00ff00")
        multi_page(main_frame)
    else:
        lblRgError.configure(text='Username Duplicated')
    
def transection_main(choice : str):
    '''ฟังก์ชันที่ทำงานหลังเลือก choice ในหน้า main'''

    if choice == "Booking":
        multi_page(Booking)

    elif choice == "Order":
        multi_page(order)

    elif choice == "Check Bill":
        multi_page(Check_Bill)

    else: 
        print("Hello world")

def segment_clike(value):
    if value == "Booking":
        multi_page(Booking)
    elif value == "Order":
        multi_page(Order)
    elif value == "Check Bill":
        multi_page(Check_Bill)
    else:
        print("Hello world")




#   =============================================== main app ===============================================
app = ctk.CTk()

app.title("PyRestaurant")
app._set_appearance_mode("system")
app.geometry("500x600")
# ==========================================================================================================

# ============================================= page frame =================================================

login_frame = ctk.CTkFrame(app,fg_color='transparent')
register_frame = ctk.CTkFrame(app,fg_color='transparent')
main_frame = ctk.CTkFrame(app,fg_color='transparent')
Booking = ctk.CTkFrame(app,fg_color='transparent')
Order = ctk.CTkFrame(app,fg_color='transparent')
Check_Bill = ctk.CTkFrame(app,fg_color='transparent')

# ==========================================================================================================

# ============================================ login frame =================================================
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
lable4 = ctk.CTkLabel(login_frame,
                      text="Don't have ID ?")
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
buttonregis = ctk.CTkButton(login_frame
                            ,text="Register",
                            fg_color='transparent',
                            hover=False,
                            command=lambda: multi_page(register_frame)
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
lable4.pack()
buttonregis.pack()
buttonback.pack()
# ============================================================================================================

# ================================================== register frame ==========================================

lblrg1 = ctk.CTkLabel(register_frame,text="Register")
lblrg2 = ctk.CTkLabel(register_frame,text="Username")
lblrg3 = ctk.CTkLabel(register_frame,text="Password")
lblrg4 = ctk.CTkLabel(register_frame,text="Firstname")
lblrg5 = ctk.CTkLabel(register_frame,text="Lastname")
lblrg6 = ctk.CTkLabel(register_frame,text="Phone")
lblrg7 = ctk.CTkLabel(register_frame,text="E-mail")
lblRgError = ctk.CTkLabel(register_frame,text='',text_color='#ff0000')

entryrg1 = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Username ของคุณ")
entryrg2 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณ")
entryrg3 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณอีกครั้ง")
entryrg4 = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Firstname ของคุณ")
entryrg5 = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Lastname ของคุณ")
entryrg6 = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Phone ของคุณ")
entryrg7 = ctk.CTkEntry(register_frame,placeholder_text="ใส่ E-mail ของคุณ")

buttonRgsp1 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg1)
buttonRgsp2 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg2)
buttonRg = ctk.CTkButton(register_frame,text='Enter',command=register)
buttonRgback =ctk.CTkButton(register_frame,text="Back",command=lambda: multi_page(login_frame))

lblrg1.pack()
lblRgError.pack()
lblrg2.pack(pady = 5)
entryrg1.pack()
lblrg3.pack(pady=5)
entryrg2.pack()
buttonRgsp1.pack()
entryrg3.pack()
buttonRgsp2.pack()
lblrg4.pack(pady = 5)
entryrg4.pack()
lblrg5.pack(pady = 5)
entryrg5.pack()
lblrg6.pack()
entryrg6.pack()
lblrg7.pack()
entryrg7.pack()

buttonRg.pack()
buttonRgback.pack(pady = 5)

# ============================================================================================================

# ================================================== frame main ==============================================
header_frame = ctk.CTkFrame(main_frame)
menu_options = ["Booking","Order","Check Bill"]

lblmain1 = ctk.CTkLabel(main_frame,text=f'Welcome to PyRestaurent')
buttonlogout = ctk.CTkButton(header_frame,text='logout',
                            hover_color='#ff0000',
                            command=lambda : multi_page(login_frame),
                            width= 70,
                            height= 14 )

#options_main = ctk.CTkOptionMenu(main_frame,values=menu_options,command=transection_main)
segmented_botton = ctk.CTkSegmentedButton(main_frame,values=menu_options,command=segment_clike)

header_frame.pack(side="top", fill="x", pady=(0, 20))
lblmain1.pack()
segmented_botton.pack()
segmented_botton.set("Select option")
#options_main.pack()
#options_main.set("Select option")

buttonlogout.pack(side = 'right',pady = 1, padx = 0)

# ============================================================================================================

#============================================= Booking frame =================================================
# ============================================================================================================
lblbk1 = ctk.CTkLabel(Booking,text='Booking Table')
lblbk2 = ctk.CTkLabel(Booking,text='Table Available')
lblbklist = ctk.CTkLabel(Booking,text='')
btbackMain = ctk.CTkButton(Booking,text='Back',hover_color='#ff0000',command=lambda: multi_page(main_frame))

lblbk1.pack()
lblbk2.pack()
lblbklist.pack()
btbackMain.pack()
# ============================================================================================================

# ============================================ Order frame ===================================================
# ============================================================================================================

lblod1 = ctk.CTkLabel(Order,text='Order')
lblod2 = ctk.CTkLabel(Order,text='All Menu')
lblodlist = ctk.CTkLabel(Order,text='')
btbackMainOd = ctk.CTkButton(Order,text='Back',hover_color='#ff0000',command=lambda: multi_page(main_frame))

lblod1.pack()
lblod2.pack()
lblodlist.pack()
btbackMainOd.pack()
# ============================================================================================================

# ============================================ check bill frame ==============================================
# ============================================================================================================

lblCb1 = ctk.CTkLabel(Check_Bill,text='Check Bill')
lblCb2 = ctk.CTkLabel(Check_Bill,text='All Order')
lblCblist = ctk.CTkLabel(Check_Bill,text='')
btbackMainCb = ctk.CTkButton(Check_Bill,text='Back',hover_color='#ff0000',command=lambda: multi_page(main_frame))

lblCb1.pack()
lblCb2.pack()
lblCblist.pack()
btbackMainCb.pack()
# ============================================================================================================

app.mainloop()
