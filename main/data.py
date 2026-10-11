import sqlite3


def connect_db():
    """
    ฟังก์ชันสำหรับเชื่อมต่อฐานข้อมูล SQLite
    Return: connection object
    """
    conn = sqlite3.connect("database/database.db")
    return conn



def login_user(username: str, password: str)-> bool:
    """
    ฟังก์ชันสำหรับตรวจสอบการเข้าสู่ระบบของผู้ใช้
    Return: bool (True หากเข้าสู่ระบบสำเร็จ, False หากล้มเหลว)
    """
    try:
        result = False
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
        user = cursor.fetchall()

        if user != []:
            result = True
        else:
            result = False 

    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error : {e}")
    finally:
        conn.close()
    return result

def check_phone(phone:str)->int:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE phone = ?",(phone,))
    if cursor.fetchall() != []:
        conn.close()
        return 0
    else:
        conn.close()
        return 1

def check_email(email:str)-> int:
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE email = ?",(email,))
        ce = cursor.fetchall()
        if ce != [] :
            conn.close()
            return 0
        else:
            conn.close()
            return 1
    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error : {e}")
        conn.close()

def register_user(username: str, password: str, firstname: str, lastname: str, phone: str, email: str = None, role: str = "customer") -> bool|int:
    """
    ฟังก์ชันสำหรับลงทะเบียนผู้ใช้ใหม่
    Return: bool (True หากลงทะเบียนสำเร็จ, False หากล้มเหลว)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # ตรวจสอบว่าผู้ใช้มีอยู่แล้วหรือไม่
        cursor.execute("SELECT * FROM User WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        cphone = check_phone(phone)
        cemail = check_email(email)

        if existing_user is not None:
            conn.close()
            return 1  # ผู้ใช้มีอยู่แล้ว
        elif cphone == 0:
            conn.close()
            return 2
        elif cemail == 0:
            conn.close()
            return 3

              

        
        cursor.execute("INSERT INTO User (username, password, firstname, lastname, phone, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, firstname, lastname, phone, email, role))
        conn.commit()
        
        # เพิ่มผู้ใช้ใหม่
    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error : {e}")
        return False
    finally:
        conn.close()
    
    return True  # ลงทะเบียนสำเร็จ

def get_user_info(username: str) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลผู้ใช้จากฐานข้อมูล
    Return: dict (ข้อมูลผู้ใช้) หรือ None หากไม่พบผู้ใช้
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM User WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user is not None:
        user_info = {
            "username": user[0],
            "firstname": user[2],
            "lastname": user[3],
            "phone": user[4],
            "email": user[5],
            "role": user[6]
        }
        return user_info
    else:
        return None


def menu():
    """
    ฟังก์ชันสำหรับแสดงเมนูอาหารของโปรแกรม
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu_food")
    menu_items = cursor.fetchall()
    
    conn.close()
    
    return menu_items

def menu_drink():
    """
    ฟังก์ชันสำหรับแสดงเมนูเครื่องดื่มของโปรแกรม
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu_drink")
    menu_items = cursor.fetchall()
    
    conn.close()
    
    return menu_items

def get_menu_item(item_id: int) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลเมนูอาหารตามรหัสเมนู
    Return: dict (ข้อมูลเมนูอาหาร) หรือ None หากไม่พบเมนู
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM menu_food WHERE id=?", (item_id,))
    item = cursor.fetchone()
    
    conn.close()
    
    if item is not None:
        menu_item = {
            "id": item[0],
            "name": item[1],
            "description": item[3],
            "price": item[2]
        }
        return menu_item
    else:
        return None

def get_drink_item(item_id: int) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลเมนูเครื่องดื่มตามรหัสเมนู
    Return: dict (ข้อมูลเมนูเครื่องดื่ม) หรือ None หากไม่พบเมนู
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM menu_drink WHERE id=?", (item_id,))
    item = cursor.fetchone()
    
    conn.close()
    
    if item is not None:
        drink_item = {
            "id": item[0],
            "name": item[1],
            "description": item[3],
            "price": item[2]
        }
        return drink_item
    else:
        return None

def add_order(totalOrder: str,
              quantity: int,
              totalPrice: float, 
              username:str,
              day,
              time:str,
              status: str = "สั่งอาหารแล้ว",table_number: int = 1,status_pay : str = 'ยังไม่จ่าย') -> bool:
    """
    ฟังก์ชันสำหรับเพิ่มคำสั่งซื้อของผู้ใช้
    Return: bool (True หากเพิ่มคำสั่งซื้อสำเร็จ, False หากล้มเหลว)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # เพิ่มคำสั่งซื้อในตาราง orders
        cursor.execute("INSERT INTO orders (menu, quantity, totalprice, status, table_no,customer,day,time,status_pay) VALUES (?, ?, ?, ?, ?,?,?,?,?)", 
                    (str(totalOrder), quantity, totalPrice, status, table_number,username,day,time,status_pay))
        conn.commit()
        result = True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"SQL Error : {e}")
        result = False
    finally:
        conn.close()
    
    return result

def update_order_status(order_id: int, new_status: str) -> bool:
    """
    ฟังก์ชันสำหรับอัปเดตสถานะคำสั่งซื้อ
    Return: bool (True หากอัปเดตสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE orders SET status=? WHERE no_order=?", (new_status, order_id))
    conn.commit()
    conn.close()
    
    return True

def get_order(table_number: str) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลคำสั่งซื้อของโต๊ะที่กำหนด
    Return: dict (ข้อมูลคำสั่งซื้อ) หรือ None หากไม่พบคำสั่งซื้อ
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE table_no=?", (table_number,))
    order = cursor.fetchall()
    
    conn.close()
    
    if order is not None:
        order_info = {
            "no_order": order[0],
            "totalorder": order[1],
            "quantity": order[2],
            "totalprice": float(order[3]),
            "status": order[4],
            "table_no": order[5]
        }
        return order_info
    else:
        return None
    
def get_order_user(username: str) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลคำสั่งซื้อของโต๊ะที่กำหนด
    Return: dict (ข้อมูลคำสั่งซื้อ) หรือ None หากไม่พบคำสั่งซื้อ
    """
    order = []
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE customer=? AND status_pay = 'ยังไม่จ่าย' ", (username,))
        order = cursor.fetchall()

        
    except sqlite3.Error as e :
        print(f"Database error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()
    return order

def group_order(username:str, target_table: str = "ทุกโต๊ะ")-> list[dict]:
    """รวมกลุ่มของ order ที่ลูกค้าสั่ง"""

    try:
        conn = connect_db()
        cursor = conn.cursor()

        if target_table == "ไม่มีโต๊ะที่ต้องชำระ":
            return []
        elif target_table == "ทุกโต๊ะ" or not target_table:
            cursor.execute("""
                SELECT menu, customer, status, SUM(quantity), SUM(totalprice) 
                FROM orders 
                WHERE customer = ? AND status_pay = 'ยังไม่จ่าย' 
                GROUP BY menu, customer
            """, (username,))
        else:
            cursor.execute("""
                SELECT menu, customer, status, SUM(quantity), SUM(totalprice) 
                FROM orders 
                WHERE customer = ? AND table_no = ? AND status_pay = 'ยังไม่จ่าย' 
                GROUP BY menu, customer
            """, (username, target_table))

        order = cursor.fetchall()

    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error : {e}")
        order = []
    finally:
        conn.close()

    return order

def add_menu_item(name: str, description: str, price: float) -> bool:
    """
    ฟังก์ชันสำหรับเพิ่มเมนูอาหารใหม่
    Return: bool (True หากเพิ่มเมนูสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO menu_food (name, price,description) VALUES (?, ?, ?)", (name, price, description))

    conn.commit()
    conn.close()
    
    return True

def add_drink_item(name: str, description: str, price: float) -> bool:
    """
    ฟังก์ชันสำหรับเพิ่มเมนูเครื่องดื่มใหม่
    Return: bool (True หากเพิ่มเมนูสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO menu_drink (name, price,description) VALUES (?, ?, ?)", (name, price, description))

    conn.commit()
    conn.close()
    
    return True

def add_table(table_number: str ,capacity : int , status : str = "ว่าง") -> bool:
    """
    ฟังก์ชันสำหรับเพิ่มโต๊ะใหม่
    Return: bool (True หากเพิ่มโต๊ะสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO dining_tables (table_no, capacity, status) VALUES (?, ?, ?)", (table_number, capacity, status))

    conn.commit()
    conn.close()
    
    return True

def get_table(username: str) -> list[dict] | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลโต๊ะที่กำหนด
    Return: dict (ข้อมูลโต๊ะ) หรือ None หากไม่พบโต๊ะ
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reservations WHERE customer=? AND date(booking_date) >= date('now','localtime')", (username,))
    rows = cursor.fetchall()
    
    conn.close()
    table_info = []
    if rows is not None:
        for table in rows:
            table_info.append({
            "table_no": table[1],
            "customer": table[2],
            "day":table[3],
            "timestart":table[4],
            "timeend":table[5],
            "status": table[6]
        })
        return table_info
    else:
        return None

def update_table_status(table_number: str, new_status: str,customer: str) -> bool:    
    """
    ฟังก์ชันสำหรับอัปเดตสถานะโต๊ะ
    Return: bool (True หากอัปเดตสำเร็จ, False หากล้มเหลว)
    """

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE dining_tables SET status=? , customer=? WHERE table_no=?", (new_status, customer, table_number))
        conn.commit()
        result = True
    except sqlite3.Error as e :
        print(f"Database error occurred: {e}")
        conn.rollback()
        result = False
    finally:
        conn.close()
    
    return result
    
def get_table_available(table_number,booking_date, time_start,time_end) -> list:
    """
    ฟังก์ชันสำหรับดึงข้อมูลโต๊ะที่ว่าง
    Return: list (รายการโต๊ะที่ว่าง)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute( """
            SELECT * FROM reservations WHERE table_no = ? AND booking_date = ? AND( timestart < ? AND timeend > ?)AND status = 'confirmed'
        """, (table_number,booking_date,time_end, time_start))
        available_tables = cursor.fetchall()
        
        conn.close()

        avb_tables = [{"table_no":table[1],"date":table[3],"time_slot":table[4],"status":table[5]} for table in available_tables]
        
        return avb_tables

    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error is : {e}")
        return None

def get_available_tables(booking_date: str, time_slot: str) -> list:
    """ดึงรายการโต๊ะที่ว่างในวันที่และรอบเวลาที่เลือก"""

    timestart, timeend = time_slot.split(" - ")

    try :
        conn = connect_db()
        cursor = conn.cursor()
        
        query = """
            SELECT table_no, capacity, cost 
            FROM dining_tables 
            WHERE table_no NOT IN (
                SELECT table_no 
                FROM reservations 
                WHERE booking_date = ? 
                AND (timestart < ? AND timeend > ?)
                AND status = 'confirmed'
            )
        """
        cursor.execute(query, (booking_date, timeend, timestart))
        rows = cursor.fetchall()
        conn.close()

        return [{"table_no": r[0], "capacity": r[1], "cost": r[2], "status": "ว่าง"} for r in rows]
    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error is : {e}")
        return None


def create_reservation(table_no: str, customer: str, booking_date: str, time_slot: str,cost:float,status_pay:str = 'ยังไม่จ่าย') -> bool:
    """บันทึกข้อมูลการจองลงตาราง reservations"""

    timestart,timeend = time_slot.split(" - ")
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Double check ว่าโต๊ะยังว่างอยู่จริงก่อนบันทึก
        cursor.execute("""
            SELECT COUNT(*) FROM reservations 
            WHERE table_no = ? AND booking_date = ? AND (timestart < ? AND timeend > ?) AND status = 'confirmed'
        """, (table_no, booking_date,timeend, timestart))
        
        if cursor.fetchone()[0] > 0:
            conn.close()
            return False  # โต๊ะถูกจองไปแล้วในรอบนี้

        cursor.execute("""
            INSERT INTO reservations (table_no, customer, booking_date, timestart,timeend,cost,status_pay,status)
            VALUES (?, ?, ?, ?, ?, ?, ?,'confirmed')
        """, (table_no, customer, booking_date,timestart, timeend,cost,status_pay))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[DB Error create_reservation]: {e}")
        return False

def check_bill(table_number: str) -> float:
    """
    ฟังก์ชันสำหรับตรวจสอบบิลของโต๊ะ
    Return: float (ยอดรวมทั้งหมดของโต๊ะ)
    """
    total_bill = 0.0
    orders = get_order(table_number)
    
    if orders is not None:
        for _ in orders: 
            total_bill += orders["totalprice"]
    
    return total_bill

def get_user_unpaid_tables(username: str) -> list[str]:
    """ดึงรายชื่อโต๊ะที่ผู้ใช้นี้จองไว้และยังไม่ได้ชำระเงิน"""
    tables = []
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT table_no 
            FROM reservations 
            WHERE customer = ? AND status_pay = 'ยังไม่จ่าย' AND status = 'confirmed'
        """, (username,))
        rows = cursor.fetchall()
        tables = [r[0] for r in rows]
    except Exception as e:
        print(f"[DB Error get_user_unpaid_tables]: {e}")
    finally:
        if conn:
            conn.close()
    return tables

def check_bill_user(username:str, target_table: str = "ทุกโต๊ะ") -> dict:
    """
        ฟังก์ชันสำหรับตรวจสอบบิลของผู้ใช้
        Return: float (ยอดรวมทั้งหมดของโต๊ะ)
        """
    food_total = 0.0
    table_cost = 0.0
    net_total = 0.0
    tables_to_check = []

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # ดักจับข้อความกรณีไม่มีโต๊ะ
        if target_table == "ไม่มีโต๊ะที่ต้องชำระ":
            tables_to_check = []
        # 1. กำหนดรายการโต๊ะที่จะนำมาคำนวณ
        elif target_table == "ทุกโต๊ะ" or not target_table:
            cursor.execute("""
                SELECT DISTINCT table_no 
                FROM reservations 
                WHERE customer = ? AND status_pay = 'ยังไม่จ่าย' AND status = 'confirmed'
            """, (username,))
            tables_to_check = [r[0] for r in cursor.fetchall()]
        else:
            tables_to_check = [target_table]

        # 2. วนลูปคิดเงินทีละโต๊ะ
        for t_no in tables_to_check:
            t_cost = check_bill_table(t_no)
            table_cost += t_cost

            cursor.execute("""
                SELECT SUM(totalprice) 
                FROM orders 
                WHERE customer = ? AND table_no = ? AND status_pay = 'ยังไม่จ่าย'
            """, (username, t_no))
            price_row = cursor.fetchone()
            t_food = float(price_row[0]) if price_row and price_row[0] is not None else 0.0

            food_total += t_food

            # สั่งอาหาร >= มัดจำ -> คิดตามค่าอาหาร / สั่งน้อยกว่ามัดจำ (หรือไม่สั่ง) -> คิดขั้นต่ำเป็นมัดจำ
            if t_food >= t_cost:
                net_total += t_food
            else:
                net_total += t_cost

    except Exception as e:
        print(f"[DB Error check_bill_user]: {e}")
    finally:
        if conn:
            conn.close()

    return {
        "food_total": food_total,
        "table_cost": table_cost,
        "net_total": net_total,
        "tables": tables_to_check
    }

def check_bill_table(table_no:str):

    "use to get cost table at user selected"

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cost FROM dining_tables WHERE table_no = ?",(table_no,))
    
        cost = cursor.fetchone()
        conn.close()

        
        return float(cost[0]) if cost and cost[0] is not None else 0.0

    except sqlite3.Error as e :
        conn.rollback()
        print(f"SQL Error is : {e}")
        return 0.0
    except Exception as e:
        print(f"[Unexpected Error check_bill_table]: {e}")
        return 0.0
    finally:
        if conn:
            conn.close()

def pay_bill_user(username: str,target_table: str = "ทุกโต๊ะ") -> bool:
    """
    ฟังก์ชันสำหรับอัปเดตสถานะชำระเงินของผู้ใช้จาก 'ยังไม่จ่าย' เป็น 'จ่ายแล้ว'
    Return: bool (True หากอัปเดตสำเร็จ, False หากล้มเหลว)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if target_table == "ทุกโต๊ะ" or not target_table:
            cursor.execute(
                "UPDATE orders SET status_pay = 'จ่ายแล้ว', status = 'ชำระเงินแล้ว' WHERE customer = ? AND status_pay = 'ยังไม่จ่าย'",
                (username,)
            )
            cursor.execute(
                "UPDATE reservations SET status_pay = 'จ่ายแล้ว' WHERE customer = ? AND status_pay = 'ยังไม่จ่าย'",
                (username,)
            )
        else:
            cursor.execute(
                "UPDATE orders SET status_pay = 'จ่ายแล้ว', status = 'ชำระเงินแล้ว' WHERE customer = ? AND table_no = ? AND status_pay = 'ยังไม่จ่าย'",
                (username, target_table)
            )
            cursor.execute(
                "UPDATE reservations SET status_pay = 'จ่ายแล้ว' WHERE customer = ? AND table_no = ? AND status_pay = 'ยังไม่จ่าย'",
                (username, target_table)
            )
        conn.commit()
        result = True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[SQL Error pay_bill_user]: {e}")
        result = False
    finally:
        conn.close()
    
    return result

if __name__ == "__main__":
    '''update_table_status("A1",'ว่าง', None)
    update_table_status("A2",'ว่าง', None)
    update_table_status("A3",'ว่าง', None)
    update_table_status("A4",'ว่าง', None)
    update_table_status("B1",'ว่าง', None)
    update_table_status("B3",'ว่าง', None)
    update_table_status("B2",'ว่าง',None)
    update_table_status("B4",'ว่าง',None)'''



