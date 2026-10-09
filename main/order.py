import data
from datetime import *

def timenows()->str:
    timenow = datetime.now()
    formatted = timenow.strftime("%H:%M:%S")
    return formatted

def day_now() -> str :
    daynow = datetime.now()
    formatted = daynow.strftime("%Y/%m/%d")
    return formatted

def menu():
    """
    ฟังก์ชันสำหรับแสดงเมนูเครื่องดื่มของโปรแกรม
    """
    menu_items = data.menu() + data.menu_drink()
    return menu_items

def add_order(list_order:list[dict],username:str,tables:dict) -> bool:
    """
    ฟังก์ชันสำหรับสั่งอาหาร
    Return: bool (True หากสั่งอาหารสำเร็จ, False หากล้มเหลว)
    """
    sucess = False
    total_price = 0
    item = ''
    quantity = 0

    
    table = tables["table_no"]
    day = tables["day"]
    times = tables['time']

    for items in list_order :
        quantity = items['qty']
        item = items['name']
        total_price = items["price"] * quantity
        save = data.add_order(item, quantity, total_price,username,day,times,table_number=table)
        if save:
            sucess = True

    return sucess  # คืนค่า True หากสั่งอาหารสำเร็จ, False หากล้มเหลว


def get_orders(username : str) -> list :
    """ฟังก์ชันสำหรับดึงข้อมูลที่ลูกค้าสั่ง"""
    orders = data.get_order_user(username)
    result = []
    for order in orders:
        if order is not None:
            order_info = {
                        "no_order": order[0],
                        "menu": order[1],
                        "quantity": order[2],
                        "totalprice": float(order[3]),
                        "status": order[4],
                        "table_no": order[5],
                        'date': f"{order[7]} | {order[8]}"
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
    
    print(menu())
    
