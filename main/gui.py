import customtkinter as ctk
from tkcalendar import *
import os
import order
import logic
import data
import datetime

def timenows()->str:
    timenow = datetime.datetime.now()
    formatted = timenow.strftime("%H:%M:%S")
    return formatted

def day_now() -> str :
    daynow = datetime.datetime.now()
    formatted = daynow.strftime("%Y-%m-%d")
    return formatted

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

    if target_frame == Booking :
        load_table_data()

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

def auto_set_end_time(selected_start_time: str):
    """ฟังก์ชันคำนวณเวลาช่องที่สองให้บวกจากช่องแรก 1 ชั่วโมงอัตโนมัติ"""
    try:
        time_fmt = "%H:%M"
        # 1. แปลง String เวลาเป็น datetime object
        start_dt = datetime.datetime.strptime(selected_start_time, time_fmt)
        end_time = datetime.datetime.strptime(option_time2.get(), time_fmt)

        max_time = datetime.datetime.strptime("23:00", time_fmt)
        
        # 2. บวกเวลาเพิ่ม 1 ชั่วโมง
        end_dt = start_dt + datetime.timedelta(hours=1)
        end_str = end_dt.strftime(time_fmt)

        if start_dt < end_time:
            return
        # หากเลือก 23:00 น. หรือเวลาคำนวณทะลุข้ามวัน ให้จำกัดไว้ที่ 23:00 น.
        elif selected_start_time == "23:00" or end_str < selected_start_time:
            end_str = "23:00"
        
        # 3. อัปเดตค่าของ option_time2
        option_time2.set(end_str)
    except Exception as e:
        print(f"[Error auto_set_end_time]: {e}")

def show_msg_error(message:str):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Error")
    dialog.geometry('300x150')
    dialog.grab_set()
    lableError = ctk.CTkLabel(dialog, text=message, text_color='#ff0000')
    lableError.pack(pady=20)

    entererror = ctk.CTkButton(dialog, text='OK', command=dialog.destroy)
    entererror.pack(pady=10)



#   =============================================== main app ===============================================
app = ctk.CTk()

app.title("PyRestaurant")
app._set_appearance_mode("system")
app.geometry("500x700")
# ==========================================================================================================

# ============================================= page frame =================================================

def enter_booking():
    entry_table = entryBkTable.get().strip().upper()  # เช่น "A1"
    date_user = entryBkdate.get()          # เช่น "2026-10-04"
    time_start = option_time1.get()        # เช่น "16:00"
    time_end = option_time2.get()          # เช่น "17:00"


    if not entry_table:
        show_msg_error("กรุณากรอกเลขโต๊ะ")
        return
    


    # 1. ตรวจสอบการเลือกเวลาเริ่มต้นและจบ
    if time_start == time_end:
        show_msg_error("กรุณาเลือกเวลาเริ่มต้นและเวลาสิ้นสุดให้แตกต่างกัน")
        return
    elif time_start > time_end:
        show_msg_error("กรุณาเลือกเวลาเริ่มต้นก่อนเวลาสิ้นสุด")
        return

    # 2. รวมวันที่และเวลาเข้าด้วยกันแล้วแปลงเป็น datetime object
    try:
        booking_datetime = datetime.datetime.strptime(f"{date_user} {time_start}", "%Y-%m-%d %H:%M")
    except ValueError:
        show_msg_error("รูปแบบวันที่หรือเวลาไม่ถูกต้อง")
        return

    # 3. เปรียบเทียบกับเวลาปัจจุบัน ณ วินาทีนี้
    if booking_datetime < datetime.datetime.now():
        show_msg_error("ไม่สามารถจองเวลาย้อนหลังได้ กรุณาเลือกเวลาในอนาคต")
        return
    
    data_avb_table = data.get_table_available(entry_table, date_user, f"{time_start} - {time_end}")
    if  data_avb_table is not None and len(data_avb_table) > 0:
        show_msg_error(f"โต๊ะ {entry_table} ไม่ว่างในวันที่ {date_user} เวลา {time_start} - {time_end}")
        return

    timeuser = f"{time_start} - {time_end}"

    dialog = ctk.CTkToplevel(app)
    dialog.title("ยืนยันการจอง")
    dialog.geometry('350x180')
    dialog.grab_set()

    lblCon = ctk.CTkLabel(dialog, text=f"ยืนยันการจองโต๊ะ {entry_table} หรือไม่?", font=("Arial", 14, "bold"))
    lblCon.pack(pady=20)

    btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
    btn_frame.pack(pady=10)

    def on_comfirm():
        dialog.destroy()

        data.create_reservation(entry_table,current_user,date_user,timeuser)
        dialog_Order = ctk.CTkToplevel(app)
        dialog_Order.title("Your want to order?")
        dialog_Order.geometry('350x180')
        dialog_Order.grab_set()

        lblOrder = ctk.CTkLabel(dialog_Order, text=f"คุณต้องการสั่งอาหารหรือไม่?", font=("Arial", 14, "bold"))
        lblOrder.pack(pady=20)

        btn_frame_order = ctk.CTkFrame(dialog_Order,fg_color='transparent')
        btn_frame_order.pack(pady=10)

        def on_order():
            dialog_Order.destroy()
            multi_page(Order)

        def on_cancel_order():
            dialog_Order.destroy()
            multi_page(main_frame)  

        btnOrder_yes = ctk.CTkButton(btn_frame_order,text='Yes',fg_color="#5eff00",text_color="#000000",command=on_order,width=100)
        btnOrder_no = ctk.CTkButton(btn_frame_order,text='No',fg_color="#ff0000",text_color="#000000",command=on_cancel_order,width=100)

        btnOrder_yes.pack(side="left", padx=10)
        btnOrder_no.pack(side="right", padx=10)
        load_table_data(date_user,timeuser)


    def on_cancel():
        dialog.destroy()

    btnBk_yes = ctk.CTkButton(btn_frame,text='Yes',fg_color="#5eff00",text_color="#000000",command=on_comfirm,width=100)
    btnBk_no = ctk.CTkButton(btn_frame,text='No',fg_color="#ff0000",text_color="#000000",command=on_cancel,width=100)

    btnBk_yes.pack(side="left", padx=10)
    btnBk_no.pack(side="right", padx=10)

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
    command= app.destroy
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

enteruser.bind("<Return>", lambda event: check_pass())
enterpass.bind("<Return>", lambda event: check_pass())

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
segmented_botton.set(0,"end")
#options_main.pack()
#options_main.set("Select option")

buttonlogout.pack(side = 'right',pady = 10, padx = 10)
lblheadmain1.pack(side = 'right',pady = 1 , padx = 5)

# ============================================================================================================

#============================================= Booking frame =================================================
# ============================================================================================================

menu_timeOption = ["16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]

frame_available_table = ctk.CTkFrame(Booking)
frame_filter_table = ctk.CTkFrame(Booking,fg_color='transparent')
colum_no = ctk.CTkLabel(frame_available_table,text='NO.')
colum_capacity = ctk.CTkLabel(frame_available_table,text='Capacity')
colum_cost = ctk.CTkLabel(frame_available_table,text='Cost')
colum_status = ctk.CTkLabel(frame_available_table,text='Status')

def load_table_data(booking_date: str = day_now(), time_slot: str = "16:00 - 17:00"):

    auto_set_end_time(option_time1.get())
    headers = [colum_no,colum_status,colum_cost,colum_capacity]
    for widget in frame_available_table.winfo_children():
        if widget not in headers :
            widget.destroy()

    tables_AvB = data.get_available_tables(booking_date, time_slot)

    if tables_AvB:
        for row_idx, table in enumerate(tables_AvB, start=1):
            t_no = table["table_no"]        # เลขโต๊ะ
            t_capacity = table["capacity"]  # ความจุที่นั่ง
            t_cost = table["cost"]       # ค่าธรรมเนียม/ราคา (หรือดึงจาก DB หากมี)
            t_status = table["status"]    # สถานะ (เช่น "ว่าง")

            # แสดงผลแต่ละคอลัมน์ในแถวปัจจุบัน (row=row_idx)
            ctk.CTkLabel(frame_available_table, text=str(t_no)).grid(row=row_idx, column=0, padx=15, pady=5)
            ctk.CTkLabel(frame_available_table, text=str(t_capacity)).grid(row=row_idx, column=1, padx=10, pady=5)
            ctk.CTkLabel(frame_available_table, text=str(t_cost)).grid(row=row_idx, column=2, padx=50, pady=5)
            ctk.CTkLabel(frame_available_table, text=str(t_status), text_color="#00FF3C").grid(row=row_idx, column=3, padx=100, pady=5)
    else:
        ctk.CTkLabel(frame_available_table,text='ไม่มีโต๊ะว่าง', text_color="#ff0000").grid(row = 1,column=0,columnspan = 4 ,pady = 10)


lblbk1 = ctk.CTkLabel(Booking,text='Booking Table')
lblbk2 = ctk.CTkLabel(Booking,text='Table Available')
entryBkTable = ctk.CTkEntry(Booking,placeholder_text='กรอกเลขโต๊ะ เช่น A1')

entryBkdate = DateEntry(frame_filter_table,date_pattern= "yyyy-mm-dd",
                        width = 25 ,height = 100,font=("Helvetica", 20),
                        background = 'darkblue',foreground = 'white',borderwidth = 2)
option_time1 = ctk.CTkOptionMenu(frame_filter_table,values= menu_timeOption,
                                 width=50,height=15,
                                 fg_color='#000000',button_color="#005EFF",button_hover_color="#0041b2",
                                 command=auto_set_end_time)
option_time2 = ctk.CTkOptionMenu(frame_filter_table,values= menu_timeOption,
                                 width=50,height=15,
                                 fg_color='#000000',button_color="#005EFF",button_hover_color="#0041b2"
                                 )
enterBkfilter = ctk.CTkButton(frame_filter_table,text='Filter',
                              width=100,height=15,
                              fg_color="#005EFF",hover_color="#0041b2",
                              command=lambda: load_table_data(entryBkdate.get(),f"{option_time1.get()} - {option_time2.get()}"))


buttonBkOk = ctk.CTkButton(Booking,text='Enter',fg_color="#005EFF",hover_color="#0041b2",command=enter_booking)
btbackMain = ctk.CTkButton(Booking,text='Back',fg_color = "#ff0000",hover_color="#a80000",command=lambda: multi_page(main_frame))

lblbk1.pack()
lblbk2.pack()

entryBkdate.grid(row=0,column=0,columnspan=2,padx=10,pady=5)
option_time1.grid(row=1,column=0,padx=5,pady=10)
option_time2.grid(row=1,column=1,padx=5,pady=10)
enterBkfilter.grid(row=2,column=0,columnspan=2,pady=5)

frame_filter_table.pack(pady = 10)

frame_available_table.pack()
colum_no.grid(row=0,column =0,padx=15,pady=5)
colum_capacity.grid(row=0,column=1,padx=10,pady=5)
colum_cost.grid(row=0,column=2,padx=50,pady=5)
colum_status.grid(row=0,column=3,padx=100,pady=5)

entryBkTable.pack()

buttonBkOk.pack(pady = 5)
btbackMain.pack(pady = 5)
# ============================================================================================================

# ============================================ Order frame ===================================================
# ============================================================================================================

lblod1 = ctk.CTkLabel(Order,text='Order')
lblod2 = ctk.CTkLabel(Order,text='All Menu')
lblodlist = ctk.CTkLabel(Order,text='')
btbackMainOd = ctk.CTkButton(Order,text='Back',fg_color = "#ff0000",hover_color="#a80000",command=lambda: multi_page(main_frame))

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
