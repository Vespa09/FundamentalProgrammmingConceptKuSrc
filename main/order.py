import data
from datetime import *

def timenows()->str:
    timenow = datetime.now()
    formatted = timenow.strftime("%H:%M:%S")
    return formatted

def day_now() -> str :
    daynow = datetime.now()
    formatted = daynow.strftime("%d/%m/%Y")
    return formatted

def menu_food():
    """
    ฟังก์ชันสำหรับแสดงเมนูอาหารของโปรแกรม
    """
    return data.menu()

def menu_drink():
    """
    ฟังก์ชันสำหรับแสดงเมนูเครื่องดื่มของโปรแกรม
    """
    return data.menu_drink()

def order_food(item_id: int, quantity: int, table:str, username:str) -> bool:
    """
    ฟังก์ชันสำหรับสั่งอาหาร
    Return: bool (True หากสั่งอาหารสำเร็จ, False หากล้มเหลว)
    """
    item = data.get_menu_item(item_id)
    if item is None:
        return False
    total_price = item["price"] * quantity

    return data.add_order(item["name"], quantity, total_price,username,day_now(),timenows(),table_number=table)  # คืนค่า True หากสั่งอาหารสำเร็จ, False หากล้มเหลว


def order_drink(item_id: int, quantity: int, table_no: str,username:str) -> bool:
    """
    ฟังก์ชันสำหรับสั่งเครื่องดื่ม
    Return: bool (True หากสั่งเครื่องดื่มสำเร็จ, False หากล้มเหลว)
    """
    item = data.get_drink_item(item_id)
    if item is None:
        return False  # เมนูไม่ถูกต้อง
    
    total_price = item["price"] * quantity
    order_result = data.add_order(item["name"], quantity, total_price,username,timenows(), table_number = table_no)
    
    return order_result  # คืนค่า True หากสั่งเครื่องดื่มสำเร็จ, False หากล้มเหลว

def get_orders(username : str) -> list :
    """ฟังก์ชันสำหรับดึงข้อมูลที่ลูกค้าสั่ง"""
    orders = data.get_order_user(username)
    result = []
    for order in orders:
        if order is not None:
            order_info = {
                        "no_order": order[0],
                        "totalorder": order[1],
                        "quantity": order[2],
                        "totalprice": float(order[3]),
                        "status": order[4],
                        "table_no": order[5]
                    }
            result.append(order_info)
        else:
            result = None

    
    return  result

def show_orders(username:str):
    orders = data.group_order(username)
    sumPrice = 0
    for index,item in enumerate(orders,start=1):

        sumPrice += item[4]
        print(f"{index}. เมนู: {item[0]} | จำนวน: {item[3]} | ราคารวม: {item[4]} บาท | สถานะ: {item[2]}")
    print(f"ยอดรวมทั้งหมด : {sumPrice}")
    return sumPrice
    

def check_bill(table_number: str) -> float:
    """
    ฟังก์ชันสำหรับตรวจสอบบิลของโต๊ะ
    Return: float (ยอดรวมทั้งหมดของโต๊ะ)
    """
    return data.check_bill(table_number)

if __name__ == "__main__":
    
    show_orders('admin')
    
