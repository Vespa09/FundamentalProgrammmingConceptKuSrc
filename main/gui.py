import sys
import subprocess
import importlib

# รายชื่อ Library ที่จำเป็น
REQUIRED_PACKAGES = ["customtkinter", "tkcalendar"]

for package in REQUIRED_PACKAGES:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"[Auto-Installer] ไม่พบ {package} กำลังทำการติดตั้งให้อัตโนมัติ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import customtkinter as ctk
from tkcalendar import *
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
    Cart.pack_forget()
    Check_Bill.pack_forget()

    if target_frame == Booking :
        load_table_data()

    elif target_frame == Order :
        load_data_reservations()

    elif target_frame == Cart :
        reload_cart()

    elif target_frame == Check_Bill:
        load_check_bill_data()

    elif target_frame == main_frame:
        segmented_botton.set('')


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
        lblRgError.configure(text='กรุณากรอกข้อมูลให้ครบถ้วน', text_color='#E74C3C')
        return None

    if len(password1) < 6:
        lblRgError.configure(text='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร', text_color='#E74C3C')
        return None

    if password1 != password2:
        lblRgError.configure(text = 'รหัสผ่านไม่ตรงกัน', text_color='#E74C3C')
        return None
        
    if len(phone) < 10 or len(phone) > 10 or phone[0] != '0' or not phone.isdigit():
        lblRgError.configure(text='กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง', text_color='#E74C3C')
        return None
    
    if email == '':
        email = None

    if email and ('@' not in email or '.' not in email):
        lblRgError.configure(text='กรุณากรอกอีเมลให้ถูกต้อง', text_color='#E74C3C')
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
            lblRgError.configure(text='Username นี้ถูกใช้งานแล้ว', text_color='#E74C3C')
        elif regis == 2:
            lblRgError.configure(text='เบอร์นี้ถูกใช้งานแล้ว', text_color='#E74C3C')
        elif regis == 3:
            lblRgError.configure(text='Email นี้ถูกใช้งานแล้ว', text_color='#E74C3C')
        else:
            lblRgError.configure(text='Register Failed', text_color='#E74C3C')
    except Exception as e:
        lblRgError.configure(text='เกิดข้อผิดพลาดในการลงทะเบียน', text_color='#E74C3C')
        print(f"[Error register]: {e}")

def logout():
    global current_user, name
    current_user = ''
    name = ''
    lblheadmain1.configure(text = '')
    clear_cart()
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

def show_msg_error(message:str,color : str = '#E74C3C'):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Error")
    dialog.geometry('300x150')
    dialog.grab_set()
    lableError = ctk.CTkLabel(dialog, text=message, text_color=color)
    lableError.pack(pady=20)

    entererror = ctk.CTkButton(dialog, text='OK', command=dialog.destroy)
    entererror.pack(pady=10)

def load_menu():
    """ฟังก์ชันสำหรับดึงเมนูอาหารและเครื่องดื่ม"""
    menu_food = order.menu_food()
    menu_drink = order.menu_drink()
    return menu_food, menu_drink

def confirm_order():
    """ฟังก์ชันสำหรับยืนยันการสั่งอาหาร"""
    if current_user:
        result = data.add_order()
        if result:
            show_msg_error("ยืนยันการสั่งอาหารเรียบร้อยแล้ว")
        else:
            show_msg_error("ไม่สามารถยืนยันการสั่งอาหารได้")
    else:
        show_msg_error("กรุณาเข้าสู่ระบบก่อนทำรายการ")

def change_qty(item_id: int, delta: int):
    """ปรับตัวเลขบนหน้าจอชั่วคราว"""
    current = screen_count.get(item_id, 0)
    new_qty = max(0, current + delta)  # ป้องกันไม่ให้ต่ำกว่า 0
    screen_count[item_id] = new_qty
    qty_labels[item_id].configure(text=str(new_qty))    

def change_qty2(item_id: int,table_no:str, delta: int):
    """ปรับตัวเลขบนหน้าจอชั่วคราว"""
    for item in cart_items :
        if item['id'] == item_id and item['table']['table_no'] == table_no :
            item['qty'] += delta
            if item['qty'] <= 0 :
                cart_items.remove(item)
            break
    reload_cart()   

    

def confirm_to_cart():
    """กดปุ่ม CON เพื่อโยนรายการที่มีจำนวน > 0 เข้า Cart"""
    current_res = get_current_reservation()

    # เช็กว่าผู้ใช้เลือกโต๊ะที่จองไว้แล้วหรือยัง
    if not current_res or option_table.get() == 'ไม่มีโต๊ะที่จองไว้':
        show_msg_error("กรุณาจองโต๊ะก่อนสั่งอาหาร")
        return

    if len(option_table.get()) <= 0 or option_table.get() == 'ไม่มีโต๊ะที่จองไว้' :
        show_msg_error("กรุณาจองโต๊ะก่อนสั่งอาหาร")
        return
        
    has_items = False
    for item in menu:
        item_id = item[0]
        qty = screen_count.get(item_id, 0)

        if qty > 0:
            has_items = True

            cart_item = next((x for x in cart_items if x["id"] == item_id and x['table']['table_no'] == current_res['table_no']), None)
            # ถ้ามีในตะกร้าแล้วให้บวกทบ ถ้ายังไม่มีให้สร้างใหม่
            if cart_item:
                cart_item['qty'] += qty
            else:
                cart_items.append({
                    "id" : item_id,
                    "name": item[1],
                    "price": item[2],
                    "qty": qty,
                    "table":current_res
                })

            # รีเซ็ตตัวเลขบนหน้าจอกลับเป็น 0
            screen_count[item_id] = 0
            qty_labels[item_id].configure(text="0")

    if has_items:
        reload_cart()
    else:
        show_msg_error("กรุณาเพิ่มรายการอาหารก่อนยืนยัน")
        return
    


def update_cart(cart:list[dict]):
    "comfirm order in cart"
    if not cart_items:
        show_msg_error('ไม่มีสินค้าในตะกร้า')
        return
    
    res = order.add_order(cart,current_user)
    if res:
        dialog = ctk.CTkToplevel(app)
        dialog.title("ต้องการชำระเงินเลยหรือไม่")
        dialog.geometry('350x180')
        dialog.grab_set()
        
        lblCon = ctk.CTkLabel(dialog, text=f"สั่งอาหารเรียบร้อย\nคุณต้องการชำระเงินเลยหรือไม่?", font=("Arial", 14, "bold"))
        lblCon.pack(pady=20)
        
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=10)
        
            
        def on_comfirm():
            multi_page(Check_Bill)
            dialog.grab_release()
            dialog.after(10,dialog.destroy)
        
        def on_cancel():
            dialog.grab_release()
            dialog.destroy()
        
        btnBk_yes = ctk.CTkButton(btn_frame,text='ใช่',fg_color="#27AE60",hover_color="#1B6E3D",text_color="#000000",command=on_comfirm,width=100)
        btnBk_no = ctk.CTkButton(btn_frame,text='ไม่',fg_color="#E74C3C",hover_color="#b73e30",text_color="#000000",command=on_cancel,width=100)
        
        btnBk_yes.pack(side="left", padx=10)
        btnBk_no.pack(side="right", padx=10)
        clear_cart()
    else:
        show_msg_error("ERROR 200")

table_user =['ไม่มีโต๊ะที่จองไว้']
day = ["ไม่มีวันที่จองไว้"]
time = ["ไม่มีเวลาที่จองไว้"]
rowstable =[]
reservation_labels = []  # ตัวแปรสำหรับเก็บชื่อข้อความที่ไม่ซ้ำกัน
    
def load_data_reservations():

    global table_user,day,time,rowstable,reservation_labels
    rowstable = data.get_table(current_user)
    if rowstable:

        # Sort เรียงลำดับตาม วันที่ (day) และ เวลา (time) จากน้อยไปมาก
        rowstable.sort(key=lambda x: (x['day'], x['timestart']))
        
        # สร้างข้อความระบุโต๊ะ + วัน + เวลา เพื่อไม่ให้ข้อความซ้ำกัน
        reservation_labels = [
            f"{tb['table_no']} ({tb['day']} | {tb['timestart']} - {tb['timeend']})" for tb in rowstable
        ]
    else :
        table_user =['ไม่มีโต๊ะที่จองไว้']
        day = ["ไม่มีวันที่จองไว้"]
        time = ["ไม่มีเวลาที่จองไว้"]
        reservation_labels = ['ไม่มีโต๊ะที่จองไว้']

    option_table.configure(values = reservation_labels)
    option_table.set(reservation_labels[0])


def get_current_reservation() -> dict | None:
    """ดึงข้อมูล Dict การจองที่ตรงกับข้อความที่ผู้ใช้เลือกใน OptionMenu"""
    selected_text = option_table.get()
    
    if rowstable and selected_text in reservation_labels:
        # ค้นหาตำแหน่ง Index ของข้อความ แล้วดึง Dict ลำดับเดียวกันใน rowstable มาใช้งาน
        idx = reservation_labels.index(selected_text)
        return rowstable[idx]
        
    return None

def clear_cart():
    global cart_items
    cart_items.clear()

    reload_cart()

def RadioPay():
    pass

def load_check_bill_data():
    """ดึงข้อมูลรายการสั่งซื้อและยอดรวมมาแสดงในหน้า Check Bill"""
    update_cb_table_options()
    selected_table = option_cb_table.get()

    for widget in Cblist.winfo_children():
        widget.destroy()


    # ดึง dict ข้อมูลบิลจาก data.py
    bill_info = data.check_bill_user(current_user,selected_table)
    food_total = bill_info["food_total"]
    table_cost = bill_info["table_cost"]
    net_total = bill_info["net_total"]

    orders = data.group_order(current_user,selected_table)

    if net_total > 0:
        # แสดงรายการอาหารที่สั่ง
        has_food = False
        if orders:
            for idx, item in enumerate(orders, start=1):
                menu_name = item[0]
                qty = item[3]
                price = item[4]

                row_frame = ctk.CTkFrame(Cblist, fg_color="transparent")
                lbl_item = ctk.CTkLabel(row_frame, text=f"{idx}. {menu_name}  x{qty}", anchor='w', font=("Arial", 12))
                lbl_price = ctk.CTkLabel(row_frame, text=f"{price:.2f} ฿", anchor='e', font=("Arial", 12, "bold"))

                row_frame.pack(fill='x', padx=5, pady=3)
                lbl_item.pack(side='left', expand=True, fill='x')
                lbl_price.pack(side='right')
                has_food = True

        if not has_food:
                lbl_no_food = ctk.CTkLabel(
                    Cblist, 
                    text="ยังไม่ได้สั่งอาหารล่วงหน้า\n(ชำระเฉพาะค่ามัดจำโต๊ะ / ไปเลือกสั่งอาหารที่ร้าน)", 
                    text_color="#8a8888",
                    font=("Arial", 12)
                )
                lbl_no_food.pack(pady=20)

        # แสดงสรุปยอดรวมด้านล่าง
        table_label = f"โต๊ะ: {selected_table}" if selected_table != "ทุกโต๊ะ" else "รวมทุกโต๊ะ"
        lblCbcount.configure(
                text=f"📌 {table_label}\nมัดจำโต๊ะขั้นต่ำ: {table_cost:.2f} ฿  |  ค่าอาหารรวม: {food_total:.2f} ฿\n💰 ยอดชำระสุทธิ: {net_total:.2f} บาท"
            )
        btnCheckbill.configure(state="normal", fg_color="#005eff")
    else:
        lbl_empty = ctk.CTkLabel(Cblist, text="ไม่มีรายการโต๊ะหรืออาหารที่รอชำระเงิน", text_color="#8a8888")
        lbl_empty.pack(pady=20)
        lblCbcount.configure(text="ยอดรวมทั้งหมด: 0.00 บาท")
        btnCheckbill.configure(state="disabled", fg_color="#8a8888")

def update_cb_table_options():
    """อัปเดตตัวเลือกโต๊ะใน OptionMenu หน้า Check Bill"""
    unpaid_tables = data.get_user_unpaid_tables(current_user)
    if unpaid_tables:
        options = ["ทุกโต๊ะ"] + unpaid_tables
    else:
        options = ["ไม่มีโต๊ะที่ต้องชำระ"]
    
    option_cb_table.configure(values=options)
    # ถ้าค่าปัจจุบันไม่อยู่ในรายการ ให้เลือกอันแรก
    if option_cb_table.get() not in options:
        option_cb_table.set(options[0])



#   =============================================== main app ===============================================
app = ctk.CTk()

app.title("PyRestaurant")
app._set_appearance_mode("system")
app.geometry("500x700")
# ==========================================================================================================

# ============================================= page frame =================================================

def enter_booking():

    """ฟังก์ชันสำหรับยืนยันการจองโต๊ะ"""
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
    
    data_avb_table = data.get_table_available(entry_table, date_user, time_start,time_end)
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
        dialog.grab_release()
        dialog.after(10,dialog.destroy)

        table_cost = data.check_bill_table(entry_table)

        data.create_reservation(entry_table,current_user,date_user,timeuser,table_cost)
        dialog_Order = ctk.CTkToplevel(app)
        dialog_Order.title("Your want to order?")
        dialog_Order.geometry('350x180')
        dialog_Order.grab_set()

        lblOrder = ctk.CTkLabel(dialog_Order, text=f"คุณต้องการสั่งอาหารหรือไม่?", font=("Arial", 14, "bold"))
        lblOrder.pack(pady=20)

        btn_frame_order = ctk.CTkFrame(dialog_Order,fg_color='transparent')
        btn_frame_order.pack(pady=10)

        def on_order():
            dialog.grab_release()
            dialog.after(10,dialog_Order.destroy)
            multi_page(Order)

        def on_cancel_order():
            dialog.grab_release()
            dialog_Order.destroy()
            multi_page(main_frame)  

        btnOrder_yes = ctk.CTkButton(btn_frame_order,text='ใช่',fg_color="#27AE60",hover_color="#1B6E3D",text_color="#000000",command=on_order,width=100)
        btnOrder_no = ctk.CTkButton(btn_frame_order,text='ไม่',fg_color="#E74C3C",hover_color="#b73e30",text_color="#000000",command=on_cancel_order,width=100)

        btnOrder_yes.pack(side="left", padx=10)
        btnOrder_no.pack(side="right", padx=10)
        load_table_data(date_user,timeuser)


    def on_cancel():
        dialog.grab_release()
        dialog.after(10,dialog.destroy)

    btnBk_yes = ctk.CTkButton(btn_frame,text='ใช่',fg_color="#27AE60",hover_color="#1B6E3D",text_color="#000000",command=on_comfirm,width=100)
    btnBk_no = ctk.CTkButton(btn_frame,text='ไม่',fg_color="#E74C3C",hover_color="#b73e30",text_color="#000000",command=on_cancel,width=100)

    btnBk_yes.pack(side="left", padx=10)
    btnBk_no.pack(side="right", padx=10)

def enter_cart(cart:list[dict]):

    dialog = ctk.CTkToplevel(app)
    dialog.title("ยืนยันการสั่ง")
    dialog.geometry('350x180')
    dialog.grab_set()

    lblCon = ctk.CTkLabel(dialog, text=f"ยืนยันการสั่งอาหารหรือไม่?", font=("Arial", 14, "bold"))
    lblCon.pack(pady=20)
    
    btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
    btn_frame.pack(pady=10)

    
    def on_comfirm():
        update_cart(cart)
        dialog.grab_release()
        dialog.after(10,dialog.destroy)

    def on_cancel():
        dialog.grab_release()
        dialog.destroy()

    btnBk_yes = ctk.CTkButton(btn_frame,text='ใช่',fg_color="#27AE60",hover_color="#1B6E3D",text_color="#000000",command=on_comfirm,width=100)
    btnBk_no = ctk.CTkButton(btn_frame,text='ไม่',fg_color="#E74C3C",hover_color="#b73e30",text_color="#000000",command=on_cancel,width=100)

    btnBk_yes.pack(side="left", padx=10)
    btnBk_no.pack(side="right", padx=10)


def Paycon():

    selected_table = option_cb_table.get()
    bill_info = data.check_bill_user(current_user,selected_table)
    net_total = bill_info["net_total"]

    if net_total <= 0:
        show_msg_error("ไม่มีรายการที่ต้องชำระเงิน")
        return

    pay_method = varrdopay.get()
    method_text = "เงินสด" if pay_method == 'cash' else ("เงินโอน" if pay_method == 'transfer' else "บัตรเครดิต")

    dialog = ctk.CTkToplevel(app)
    dialog.title("ยืนยันการสั่งซื้อ")
    dialog.geometry('350x180')
    dialog.grab_set()

    lbl_pay = ctk.CTkLabel(
        dialog,
        text=f"รายการ: {selected_table}\nมัดจำโต๊ะ: {bill_info['table_cost']:.2f} บาท\nค่าอาหาร: {bill_info['food_total']:.2f} บาท\nยอดชำระสุทธิ: {net_total:.2f} บาท\nช่องทาง: {method_text}\n\nยืนยันการชำระเงินหรือไม่?",
        font=("Arial", 13, "bold")
    )
    lbl_pay.pack(pady=15)

    btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
    btn_frame.pack(pady=10)

    def on_confirm():
        dialog.grab_release()
        dialog.after(10, dialog.destroy)
        pay = data.pay_bill_user(current_user,selected_table)

        if pay:
            show_msg_error('ชำระเงินเรียบร้อยแล้ว ขอบคุณครับ!', "#13ba00")
            load_check_bill_data()
        else:
            show_msg_error('เกิดข้อผิดพลาดในการชำระเงิน')

    def on_cancel():
        dialog.grab_release()
        dialog.after(10, dialog.destroy)

    btn_payYes = ctk.CTkButton(btn_frame, text='ใช่', fg_color="#27AE60",hover_color="#1B6E3D", text_color="#ffffff", command=on_confirm, width=100)
    btnpayNo = ctk.CTkButton(btn_frame, text='ไม่', fg_color="#E74C3C",hover_color="#b73e30", text_color="#ffffff", command=on_cancel, width=100)

    btn_payYes.pack(side='left', padx=10)
    btnpayNo.pack(side='left', padx=10)

varrdopay =ctk.StringVar()
    
login_frame = ctk.CTkFrame(app,fg_color='transparent')
register_frame = ctk.CTkFrame(app,fg_color='transparent')
main_frame = ctk.CTkFrame(app,fg_color='transparent')
Booking = ctk.CTkFrame(app,fg_color='transparent')
Order = ctk.CTkFrame(app,fg_color='transparent')
Cart = ctk.CTkFrame(app,fg_color='transparent')
Check_Bill = ctk.CTkFrame(app,fg_color='transparent')

# ==========================================================================================================

# ============================================ login frame =================================================
lable1 = ctk.CTkLabel(login_frame,
    text="Welcome To PyRestaurant",
    text_color="#3BB758"
)
lable2 = ctk.CTkLabel(login_frame,
    text="Username"

)
lable3 = ctk.CTkLabel(login_frame,
    text="Password"
)
lable4 = ctk.CTkLabel(login_frame,
                      text="ยังไม่มีบัญชีใช่ไหม ?")
lableError = ctk.CTkLabel(login_frame,text='',text_color='#E74C3C')

enteruser = ctk.CTkEntry(login_frame,placeholder_text="ใส่ Username ของคุณ")
enterpass = ctk.CTkEntry(login_frame,show='*',placeholder_text="ใส่ Password ของคุณ")

button = ctk.CTkButton(login_frame,
    text='ล็อกอิน',
                       text_color="#fcfdfb",
                       fg_color="#27AE60",
                       hover_color="#1B6E3D",
                       command= check_pass
                       )
buttonregis = ctk.CTkButton(login_frame
                            ,text="สมัครสมาชิกเลย",
                            text_color="#42AD1B",
                            fg_color='transparent',
                            hover=False,
                            command=lambda: multi_page(register_frame)
)

buttonback = ctk.CTkButton(
    login_frame, text='ปิดแอพ',
    text_color="#f4f1f1",
    fg_color='#E74C3C',
    hover_color="#b73e30",
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
lblRgError = ctk.CTkLabel(register_frame,text='',text_color='#E74C3C')

entryrgUser = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Username ของคุณ")
entryrgPass1 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณ")
entryrgPass2 = ctk.CTkEntry(register_frame,show= '*' ,placeholder_text="ใส่ Password ของคุณอีกครั้ง")
entryrgFName = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Firstname ของคุณ")
entryrgLName = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Lastname ของคุณ")
entryrgPhone = ctk.CTkEntry(register_frame,placeholder_text="ใส่ Phone ของคุณ")
entryrgEmail = ctk.CTkEntry(register_frame,placeholder_text="ใส่ E-mail ของคุณ")

buttonRgsp1 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg1)
buttonRgsp2 = ctk.CTkButton(register_frame,text='😑',fg_color='transparent',hover=False,command=show_passwordRg2)
buttonRg = ctk.CTkButton(register_frame,text='ยืนยัน',command=register)
buttonRgback =ctk.CTkButton(register_frame,text="กลับ",command=lambda: multi_page(login_frame))

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
buttonlogout = ctk.CTkButton(header_frame,text='ออกจากระบบ',
                             fg_color = "#E74C3C",
                            hover_color="#b73e30",
                            command=logout,
                            width= 140,
                            height= 14 )

#options_main = ctk.CTkOptionMenu(main_frame,values=menu_options,command=transection_main)
segmented_botton = ctk.CTkSegmentedButton(main_frame,values=menu_options,command=segment_clike)

header_frame.pack(side="top", fill="x",padx=10, pady=(10, 15))
lblmain1.pack()
segmented_botton.pack()
segmented_botton.set("")
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
colum_no = ctk.CTkLabel(frame_available_table,text='เลขโต๊ะ')
colum_capacity = ctk.CTkLabel(frame_available_table,text='โต๊ะ/คน')
colum_cost = ctk.CTkLabel(frame_available_table,text='ราคา')
colum_status = ctk.CTkLabel(frame_available_table,text='สถานะ')

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
        ctk.CTkLabel(frame_available_table,text='ไม่มีโต๊ะว่าง', text_color="#E74C3C").grid(row = 1,column=0,columnspan = 4 ,pady = 10)


lblbk1 = ctk.CTkLabel(Booking,text='Booking Table')
lblbk2 = ctk.CTkLabel(Booking,text='โต๊ะว่าง')
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


buttonBkOk = ctk.CTkButton(Booking,text='ยืนยัน',fg_color="#005EFF",hover_color="#0041b2",command=enter_booking)
btbackMain = ctk.CTkButton(Booking,text='กลับ',fg_color = "#E74C3C",hover_color="#b73e30",command=lambda: multi_page(main_frame))

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

cart_items = []  # รายการอาหารที่ถูกเลือก
screen_count = {}  # เก็บจำนวนหน้าจอของแต่ละเมนู
qty_labels = {}  # เก็บ label ของจำนวนรายการอาหารแต่ละเมนู


frame_order = ctk.CTkScrollableFrame(Order,label_text = "เมนู")
headerOrder_frame = ctk.CTkFrame(Order)
headerOrder_frame1 = ctk.CTkFrame(frame_order)
headerOrder_frame1.pack(fill = 'x' ,pady=5)
menu = order.menu()
if not menu:
    show_msg_error("ไม่สามารถโหลดเมนูได้")
else:

    for item in menu:
        item_id = item[0]
        screen_count[item_id] = 0

        row_frame = ctk.CTkFrame(frame_order, fg_color='transparent')

        lbl_item_name = ctk.CTkLabel(row_frame, text=f"{item[1]} ({item[2]})", width=200, anchor='w')
        lbl_count = ctk.CTkLabel(row_frame, text='0', width=30)

        btn_minus = ctk.CTkButton(row_frame, text='-', width=30, command=lambda id=item_id: change_qty(id, -1))
        btn_plus = ctk.CTkButton(row_frame, text='+', width=30, command=lambda id=item_id: change_qty(id, 1))

        qty_labels[item_id] = lbl_count

        row_frame.pack(fill='x', pady=5, padx=10)
        lbl_item_name.pack(side='left', padx=5,expand=True)
        btn_minus.pack(side='left', padx=5)
        lbl_count.pack(side='left', padx=5)
        btn_plus.pack(side='left', padx=5)


option_table = ctk.CTkOptionMenu(headerOrder_frame1,values=table_user,fg_color='#8a8888',button_color="#005EFF",button_hover_color="#0041b2",)


lblod1 = ctk.CTkLabel(headerOrder_frame,text='Order')
btn_cart = ctk.CTkButton(headerOrder_frame,text="🛒",fg_color='transparent',hover_color="#8A8888",width=70,command= lambda: multi_page(Cart))
btbackMainOd = ctk.CTkButton(headerOrder_frame,text='กลับ',fg_color = "transparent",hover_color="#8a8888",command=lambda: multi_page(main_frame))

btnconfirm_order = ctk.CTkButton(frame_order,text='ยืนยันออเดอร์',fg_color="#005EFF",hover_color="#0041b2",command=confirm_to_cart)

option_table.pack(side = 'bottom',fill = 'x',padx = 10)


headerOrder_frame.pack(fill = 'x')
btbackMainOd.pack(side='left', pady = 5)
lblod1.pack(side= 'left' ,padx = 5 ,anchor = 'center',expand=True)
btn_cart.pack(side = 'right',padx  = 5)
frame_order.pack(pady = 10, padx = 10, fill='both', expand=True)
btnconfirm_order.pack(side= 'bottom',pady = 5)

# ============================================================================================================

# ============================================ cart frame ====================================================

qty_labels2 = {}  # เก็บ label ของจำนวนรายการอาหารแต่ละเมนู
screen_count2 = {}  # เก็บจำนวนหน้าจอของแต่ละเมนู


headercart_frame = ctk.CTkFrame(Cart)    
lblCart1 = ctk.CTkLabel(headercart_frame,text='Order')
btbackMainCart = ctk.CTkButton(headercart_frame,text='กลับ',fg_color = "transparent",hover_color="#8a8888",command=lambda: multi_page(Order))

btn_cart_confirm = ctk.CTkButton(Cart,text='ยืนยัน',fg_color='#005eff',hover_color='#0041b2',command=lambda: enter_cart(cart_items))

cart_frame = ctk.CTkScrollableFrame(Cart,label_text="My Cart")
btn_clear_cart = ctk.CTkButton(Cart,text='เคลียร์',fg_color='#E74C3C',hover_color="#b73e30",command=clear_cart)
lblCart_total = ctk.CTkLabel(Cart,text='0',bg_color="#918F8F",text_color="#0058A5")

def reload_cart():
    total_price = 0.0
    for widget in cart_frame.winfo_children():
        widget.destroy()
    if not cart_items:
        lblCart_total.configure(text="ราคารวมสุทธิ: 0.00 บาท")
        return

    # 1. จัดกลุ่มรายการอาหารตามเลขโต๊ะ
    grouped_cart = {}
    for item in cart_items:
        t_no = item['table']['table_no']
        if t_no not in grouped_cart:
            grouped_cart[t_no] = []
        grouped_cart[t_no].append(item)

    # 2. วนลูปวาดการ์ดของแต่ละโต๊ะพร้อมเส้นแบ่ง
    for t_no, items in grouped_cart.items():
        # กรอบการ์ดของโต๊ะ
        table_card = ctk.CTkFrame(cart_frame, fg_color="#2b2b2b", corner_radius=8)
        table_card.pack(fill='x', padx=5, pady=6)

        # หัวข้อเลขโต๊ะ
        lbl_table_header = ctk.CTkLabel(
            table_card, 
            text=f"📌 โต๊ะ {t_no}", 
            font=("Arial", 14, "bold"), 
            text_color="#F39C12"
        )
        lbl_table_header.pack(anchor='w', padx=10, pady=(8, 2))

        # เส้นแบ่งโซน (Divider)
        divider = ctk.CTkFrame(table_card, height=2, fg_color="#444444")
        divider.pack(fill='x', padx=8, pady=4)

        # รายการอาหารภายใต้โต๊ะนั้นๆ
        for order_item in items :
            id_item = order_item["id"]
            qty_item = order_item['qty']
            subtotal = order_item["price"] * qty_item
            total_price += subtotal

            rowcart_frame = ctk.CTkFrame(table_card,fg_color="transparent")

            lbl_cartName_item = ctk.CTkLabel(rowcart_frame,text=f"{order_item['name']} ({order_item['price']:.2f} ฿)",width=200,anchor='w')
            lbl_CartCount = ctk.CTkLabel(rowcart_frame,text=qty_item, width=30)

            btn_cartMinus = ctk.CTkButton(rowcart_frame,text='-' ,width=30, command=lambda id=id_item, t_code = t_no: change_qty2(id,t_code, -1))
            btn_cartPlus = ctk.CTkButton(rowcart_frame,text='+' ,width=30, command=lambda id=id_item, t_code = t_no: change_qty2(id,t_code, 1))

            qty_labels2[id_item] = lbl_CartCount

            rowcart_frame.pack(fill = 'x',padx = 5,pady = 5)
            lbl_cartName_item.pack(side = "left",padx = 5,expand = True)
            btn_cartMinus.pack(side = "left",padx = 5)
            lbl_CartCount.pack(side = "left",padx = 5)
            btn_cartPlus.pack(side = "left",padx = 5)

    lblCart_total.configure(text=f"ราคารวมสุทธิ: {total_price:.2f} บาท")

headercart_frame.pack(fill = 'x')
cart_frame.pack(fill = "both",expand =True,padx= 10,pady=10)
lblCart_total.pack(fill = "x")
btn_clear_cart.pack(side ='bottom' ,pady =  5)


btbackMainCart.pack(side= 'left' ,padx = 5)
lblCart1.pack(side= 'left' ,padx = 5 ,anchor = 'center',expand=True)
btn_cart_confirm.pack(pady= 10)

# ============================================================================================================

# ============================================ check bill frame ==============================================
# ============================================================================================================

frame_select_cb_table = ctk.CTkFrame(Check_Bill, fg_color='transparent')
lbl_select_table = ctk.CTkLabel(frame_select_cb_table, text="เลือกโต๊ะที่จะชำระเงิน:", font=("Arial", 12, "bold"))
option_cb_table = ctk.CTkOptionMenu(
    frame_select_cb_table, 
    values=["ทุกโต๊ะ"],
    command=lambda choice: load_check_bill_data()
)
frame_select_cb_table.pack(pady=5)
lbl_select_table.pack(side='left', padx=5)
option_cb_table.pack(side='left', padx=5)

haederCheckbill_freame = ctk.CTkFrame(Check_Bill)
radioframe = ctk.CTkFrame(Check_Bill,fg_color='transparent')
haederCheckbill_freame.pack(fill = 'x')
lblCb1 = ctk.CTkLabel(haederCheckbill_freame,text='Check Bill & Payment')
btbackMainCb = ctk.CTkButton(haederCheckbill_freame,text="กลับ",
                             width= 200 ,
                             fg_color = "transparent",hover_color="#8a8888",
                             command=lambda: multi_page(main_frame))


Cblist = ctk.CTkScrollableFrame(Check_Bill,label_text='ออเดอร์ทั้งหมด')
lblCbcount = ctk.CTkLabel(Check_Bill,text="ยอดรวมทั้งหมด: 0.00 บาท", font=("Arial", 16, "bold"), text_color="#005EFF")


varrdopay.set('cash')
rdopay1 = ctk.CTkRadioButton(radioframe,text='เงินสด',value='cash',variable=varrdopay,command=RadioPay)
rdopay2 = ctk.CTkRadioButton(radioframe,text='เงินโอน',value='transfer',variable=varrdopay,command=RadioPay)
rdopay3 = ctk.CTkRadioButton(radioframe,text='บัตรเครดิต',value='card',variable=varrdopay,command=RadioPay)
btnCheckbill = ctk.CTkButton(Check_Bill,text="ยืนยัน",fg_color='#005eff',hover_color='#0041b2',command=Paycon)


Cblist.pack(fill = 'both',expand = True,pady = 10 ,padx = 10)
lblCbcount.pack(pady = 10)

radioframe.pack(fill = "x",pady = 10,padx =10)

rdopay1.pack(side = 'left',pady = 10,padx = 10)
rdopay2.pack(side = 'left',pady = 10,padx = 10)
rdopay3.pack(side = 'left',pady = 10,padx = 10)

btnCheckbill.pack(pady = 10,padx = 10)

btbackMainCb.pack(side = 'left',padx = 10)
lblCb1.pack(anchor = "center",side = 'left',padx = 10)


# ============================================================================================================

app.mainloop()
