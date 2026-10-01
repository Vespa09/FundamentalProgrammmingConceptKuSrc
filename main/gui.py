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
    if entryrgPass1.cget('show') == "*":

        entryrgPass1.configure(show = '')
        buttonRgsp1.configure(text='😮')

    else:

        entryrgPass1.configure(show = '*')
        buttonRgsp1.configure(text='😑')

def show_passwordRg2():
    if entryrgPass2.cget('show') == "*":

        entryrgPass2.configure(show = '')
        buttonRgsp2.configure(text='😮')

    else:

        entryrgPass2.configure(show = '*')
        buttonRgsp2.configure(text='😑')

def multi_page(target_frame):

    lableError.configure(text='')
    lblRgError.configure(text='')


    main_frame.pack_forget()
    login_frame.pack_forget()
    register_frame.pack_forget()
    Booking.pack_forget()
    Order.pack_forget()
    Check_Bill.pack_forget()

    target_frame.pack(fill='both',expand = True ,)

current_user = ''
name = ''
current_role = "customer"
def check_pass():
    global name, current_user, current_role
    username = enteruser.get().strip()
    password = enterpass.get()

    if not username or not password:
        lableError.configure(text='กรุณากรอก Username และ Password')
        return None

    try:
        input_user = {"user": username,"password":password}
        datauser = logic.logic_function(input_user)
        if datauser:
            into_user = data.get_user_info(username)
            current_user = username
            if into_user :
                current_role = into_user["role"]
                name = into_user["firstname"]


            lblheadmain1.configure(text = f"ผู้ใช้งาน: {name} ({current_role.upper()})")

            enteruser.delete(0, 'end')
            enterpass.delete(0, 'end')

            multi_page(main_frame)
        else:
            lableError.configure(text='Username หรือ Password ไม่ถูกต้อง')

    except Exception as e:
        lableError.configure(text='เกิดข้อผิดพลาดในการเชื่อมต่อระบบ')
        print(f"[Error check_pass]: {e}")


def register():
    usernameRg = entryrgUser.get().strip()
    password1 = entryrgPass1.get()
    password2 = entryrgPass2.get()
    firstname = entryrgFName.get().strip()
    lastname = entryrgLName.get().strip()
    phone = entryrgPhone.get().strip()
    email = entryrgEmail.get().strip()

    if not usernameRg or not password1 or not firstname or not lastname or not phone:
        lblRgError.configure(text='กรุณากรอกข้อมูลให้ครบถ้วน', text_color='#ff0000')
        return None

    if len(password1) < 6:
        lblRgError.configure(text='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร', text_color='#ff0000')
        return None

    if password1 != password2:
        lblRgError.configure(text = 'รหัสผ่านไม่ตรงกัน', text_color='#ff0000')
        return None
        
    if len(phone) < 10 or len(phone) > 10 or phone[0] != '0' or not phone.isdigit():
        lblRgError.configure(text='กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง', text_color='#ff0000')
        return None
    
    if email == '':
        email = None

    if email and ('@' not in email or '.' not in email):
        lblRgError.configure(text='กรุณากรอกอีเมลให้ถูกต้อง', text_color='#ff0000')
        return None
    try:
        regis = data.register_user(usernameRg,password1,firstname,lastname,phone,email)
        if regis is True :
            lblRgError.configure(text='Register successful',text_color="#00ff00")

            entryrgUser.delete(0, 'end')
            entryrgPass1.delete(0, 'end')
            entryrgPass2.delete(0, 'end')
            entryrgFName.delete(0, 'end')
            entryrgLName.delete(0, 'end')
            entryrgPhone.delete(0, 'end')
            entryrgEmail.delete(0, 'end')

            multi_page(login_frame)
        elif regis == 1:
            lblRgError.configure(text='Username Duplicated', text_color='#ff0000')
        elif regis == 2:
            lblRgError.configure(text='Phone Number Duplicated', text_color='#ff0000')
        elif regis == 3:
            lblRgError.configure(text='Email Duplicated', text_color='#ff0000')
        else:
            lblRgError.configure(text='Register Failed', text_color='#ff0000')
    except Exception as e:
        lblRgError.configure(text='เกิดข้อผิดพลาดในการลงทะเบียน', text_color='#ff0000')
        print(f"[Error register]: {e}")

def logout():
    global current_user, name
    current_user = ''
    name = ''
    lblheadmain1.configure(text = '')
    multi_page(login_frame)
    
def transection_main(choice : str):
    '''ฟังก์ชันที่ทำงานหลังเลือก choice ในหน้า main'''

    if choice == "Booking":
        multi_page(Booking)

    elif choice == "Order":
        multi_page(Order)

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

def clear_clipboard(event):
    """ฟังก์ชันสำหรับล้าง clipboard"""
    event.clipboard_clear()
    return "break"  # ป้องกันการดำเนินการต่อไปของ event



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

security_events = [
    "<Control-c>", "<Control-C>",
    "<Command-c>", "<Command-C>",   # สำหรับ macOS
    "<Control-x>", "<Control-X>",
    "<Command-x>", "<Command-X>",   # สำหรับ macOS
    "<<Copy>>", "<<Cut>>",
    "<Button-3>"                     # คลิกขวา
]

# ผูก Event ทั้งกับ CTkEntry และ _entry ดั้งเดิมที่อยู่ภายใน
for event_pattern in security_events:
    enterpass.bind(event_pattern,lambda e: clear_clipboard(enterpass))
    enterpass._entry.bind(event_pattern, lambda e: clear_clipboard(enterpass._entry))

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

entryrgUser = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Username ของคุณ")
entryrgPass1 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณ")
entryrgPass2 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณอีกครั้ง")
entryrgFName = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Firstname ของคุณ")
entryrgLName = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Lastname ของคุณ")
entryrgPhone = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Phone ของคุณ")
entryrgEmail = ctk.CTkEntry(register_frame,placeholder_text="ใส่ E-mail ของคุณ")

buttonRgsp1 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg1)
buttonRgsp2 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg2)
buttonRg = ctk.CTkButton(register_frame,text='Enter',command=register)
buttonRgback =ctk.CTkButton(register_frame,text="Back",command=lambda: multi_page(login_frame))

lblrg1.pack()
lblRgError.pack()
lblrg2.pack(pady = 5)
entryrgUser.pack()
lblrg3.pack(pady=5)
entryrgPass1.pack()
buttonRgsp1.pack()
entryrgPass2.pack()
buttonRgsp2.pack()
lblrg4.pack(pady = 5)
entryrgFName.pack()
lblrg5.pack(pady = 5)
entryrgLName.pack()
lblrg6.pack()
entryrgPhone.pack()
lblrg7.pack()
entryrgEmail.pack()

buttonRg.pack()
buttonRgback.pack(pady = 5)

security_events = [
    "<Control-c>", "<Control-C>",
    "<Command-c>", "<Command-C>",   # สำหรับ macOS
    "<Control-x>", "<Control-X>",
    "<Command-x>", "<Command-X>",   # สำหรับ macOS
    "<<Copy>>", "<<Cut>>",
    "<Button-3>"                     # คลิกขวา
]

# ผูก Event ทั้งกับ CTkEntry และ _entry ดั้งเดิมที่อยู่ภายใน
for event_pattern in security_events:
    entryrgPass1.bind(event_pattern,lambda e: clear_clipboard(entryrgPass1))
    entryrgPass1._entry.bind(event_pattern, lambda e: clear_clipboard(entryrgPass1._entry))
    entryrgPass2.bind(event_pattern,lambda e: clear_clipboard(entryrgPass2))
    entryrgPass2._entry.bind(event_pattern, lambda e: clear_clipboard(entryrgPass2._entry))

# ============================================================================================================

# ================================================== frame main ==============================================

header_frame = ctk.CTkFrame(main_frame)
menu_options = ["Booking","Order","Check Bill"]

lblmain1 = ctk.CTkLabel(main_frame,text=f'Welcome to PyRestaurent')
lblheadmain1 = ctk.CTkLabel(header_frame,text = name)
buttonlogout = ctk.CTkButton(header_frame,text='logout',
                             fg_color = "#f74242",
                            hover_color='#cc0000',
                            command=logout,
                            width= 70,
                            height= 14 )

#options_main = ctk.CTkOptionMenu(main_frame,values=menu_options,command=transection_main)
segmented_botton = ctk.CTkSegmentedButton(main_frame,values=menu_options,command=segment_clike)

header_frame.pack(side="top", fill="x",padx=10, pady=(10, 15))
lblmain1.pack()
segmented_botton.pack()
segmented_botton.set("Select option")
#options_main.pack()
#options_main.set("Select option")

buttonlogout.pack(side = 'right',pady = 10, padx = 10)
lblheadmain1.pack(side = 'right',pady = 1 , padx = 5)

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
