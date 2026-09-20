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
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user is not None:
        return True
    else:
        return False 

def register_user(username: str, password: str, firstname: str, lastname: str, phone: str, email: str = None, role: str = "customer") -> bool:
    """
    ฟังก์ชันสำหรับลงทะเบียนผู้ใช้ใหม่
    Return: bool (True หากลงทะเบียนสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # ตรวจสอบว่าผู้ใช้มีอยู่แล้วหรือไม่
    cursor.execute("SELECT * FROM User WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user is not None:
        conn.close()
        return False  # ผู้ใช้มีอยู่แล้ว
    
    # เพิ่มผู้ใช้ใหม่
    cursor.execute("INSERT INTO User (username, password, firstname, lastname, phone, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, firstname, lastname, phone, email, role))
    conn.commit()
    conn.close()
    
    return True  # ลงทะเบียนสำเร็จ

def get_user_info(username: str) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลผู้ใช้จากฐานข้อมูล
    Return: dict (ข้อมูลผู้ใช้) หรือ None หากไม่พบผู้ใช้
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user is not None:
        user_info = {
            "id": user[0],
            "username": user[1],
            "firstname": user[3],
            "lastname": user[4],
            "phone": user[5],
            "email": user[6],
            "role": user[7]
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

def add_order(totalOrder: str,quantity: int,totalPrice: float,status: str = "สั่งอาหารแล้ว",table_number: int = 1) -> bool:
    """
    ฟังก์ชันสำหรับเพิ่มคำสั่งซื้อของผู้ใช้
    Return: bool (True หากเพิ่มคำสั่งซื้อสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # เพิ่มคำสั่งซื้อในตาราง orders
    cursor.execute("INSERT INTO orders (menu, quantity, totalprice, status, table_no) VALUES (?, ?, ?, ?, ?)", (str(totalOrder), quantity, totalPrice, status, table_number))
    conn.commit()
    conn.close()
    
    return True

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
    order = cursor.fetchone()
    
    conn.close()
    
    if order is not None:
        order_info = {
            "no_order": order[0],
            "totalorder": order[1],
            "quantity": order[2],
            "totalprice": order[3],
            "status": order[4],
            "table_no": order[5]
        }
        return order_info
    else:
        return None

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

def get_table(table_number: str) -> dict | None:
    """
    ฟังก์ชันสำหรับดึงข้อมูลโต๊ะที่กำหนด
    Return: dict (ข้อมูลโต๊ะ) หรือ None หากไม่พบโต๊ะ
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dining_tables WHERE table_no=?", (table_number,))
    table = cursor.fetchone()
    
    conn.close()
    
    if table is not None:
        table_info = {
            "table_no": table[0],
            "capacity": table[1],
            "status": table[2]
        }
        return table_info
    else:
        return None

def update_table_status(table_number: str, new_status: str,customer: str) -> bool:    
    """
    ฟังก์ชันสำหรับอัปเดตสถานะโต๊ะ
    Return: bool (True หากอัปเดตสำเร็จ, False หากล้มเหลว)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE dining_tables SET status=? , customer=? WHERE table_no=?", (new_status, customer, table_number))
    conn.commit()
    conn.close()
    
    return True
def get_table_available() -> list:
    """
    ฟังก์ชันสำหรับดึงข้อมูลโต๊ะที่ว่าง
    Return: list (รายการโต๊ะที่ว่าง)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dining_tables WHERE status='ว่าง'")
    available_tables = cursor.fetchall()
    
    conn.close()
    
    return available_tables


def check_bill(table_number: str) -> float:
    """
    ฟังก์ชันสำหรับตรวจสอบบิลของโต๊ะ
    Return: float (ยอดรวมทั้งหมดของโต๊ะ)
    """
    total_bill = 0.0
    orders = get_order(table_number)
    
    if orders is not None:
        for order in orders:
            total_bill += order[3]
    
    return total_bill

if __name__ == "__main__":
    print(get_table_available())

