import data
import order
import os

def clear_screen():
    '''ฟังก์ชันล้างหน้าจอ'''
    os.system('cls' if os.name == 'nt' else 'clear')

def logic_function():
    '''ฟังก์ชันล็อกอิน'''
    while True:
        global username
        username = input()
        print("password: ")
        password = input()
        login_result = data.login_user(username, password)
        if login_result:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password. Please try again.")

def register_function():
    '''ฟังก์ชันลงทะเบียน'''
    print("username: ")
    username = input()
    print("password: ")
    password = input()
    while True:
            password_confirm = input("Confirm password: ")
            if password != password_confirm:
                print("Passwords do not match. Please try again.")
            else:
                break
    print("firstname: ")
    firstname = input()
    print("lastname: ")
    lastname = input()
    print("phone: ")
    phone = input()
    print("email: ")
    email = input()
    if email == "":
        email = None
    regis = data.register_user(username, password, firstname, lastname, phone, email)
    if regis:
        print("Registration successful!")
        return True
    else:
        print("Registration failed. Username already exists.")

def get_table_data():
    '''ฟังก์ชันดึงข้อมูลจากตาราง table เพื่อแสดงโต๊ะว่าง'''
    
    return data.get_table_available()

def book_table(table_number: str, customer: str) -> bool:
    """
    ฟังก์ชันสำหรับจองโต๊ะ
    Return: bool (True หากจองสำเร็จ, False หากล้มเหลว)
    """
    
    # ตรวจสอบว่าตารางว่างหรือไม่
    
    table = data.get_table(table_number)
    for tables in data.get_table_available():
        if tables[0] == table_number:
            break
    
    if table is None:
        return False  # โต๊ะไม่ว่าง
    
    # อัปเดตสถานะโต๊ะเป็น "จองแล้ว"
    data.update_table_status(table_number, "จองแล้ว", customer)
    
    return True  # จองสำเร็จ



def calculate_payment(total_amount: float) -> bool:
    """
    ฟังก์ชันสำหรับคำนวณการชำระเงิน
    Return: bool (True หากชำระเงินสำเร็จ, False หากล้มเหลว)
    """
    print("Enter your amount :")
    amount = float(input())
    return total_amount - amount

def get_firstname():
    '''ฟังก์ชันที่ดึงเอาชื่อต้นของลูกค้ามา'''
    name = data.get_user_info(username)
    firstname = name['firstname']
    return firstname

def main():
    '''ฟังก์ชันหลัก'''
    while True:
        clear_screen()
        print("Welcome to the restaurant !")
        print("\nPlease select an option:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice: \n")
        clear_screen()

        if choice == "1":
            login = logic_function()
            while login:
                        clear_screen()
                        print("\nPlease select an option:")
                        print("1. Get table available")
                        print("2. Logout")
                        choice = input("Enter your choice: \n")
                        clear_screen()
                        if choice == "1":
                            print("Available tables:")
                            available_tables = get_table_data()
                            for table in available_tables:
                                if table != []:
                                    print(f"Table Number: {table[0]}, Capacity: {table[1]}")
                                else:
                                    print("No available tables.")

                            while True:
                                print("\nPlease select an option: \n 1. Book a table \n 2. Back")
                                choose_choice = input()
            
                                if choose_choice == "2":
                                    break
                                elif choose_choice == "1":
                                    table_number = input("Enter the table number you want to book: ")
                                    book_result = book_table(table_number, get_firstname())
                                    if book_result:
                                        print("Table booked successfully!")
                                        print("\nYou can now proceed to order .")
                                        order_choice = input("Do you want to order now? (y/n): ")
                                        while order_choice.lower() == "y":
                                            clear_screen()
                                            print("List of menu :")
                                            menu_items = order.menu_food() + order.menu_drink()
                                            for item in menu_items:
                                                print(f"ID: {item[0]}, Name: {item[1]}, Description: {item[3]}, Price: {item[2]}")
                                            
                                            print("\nPlease select an option: \n 1. Order food \n 2. Order drink \n 3.check bill\n 4. Back")
                                            order_choice = input()
                                            if order_choice == "4":
                                                break
                                            elif order_choice == "1":
                                                item_id = input("Enter the food item ID you want to order: ")
                                                quantity = int(input("Enter the quantity: "))
                                                order_result = order.order_food(item_id, quantity,table_number,username)
                                                if order_result:
                                                    print("Food ordered successfully!")
                                                else:
                                                    print("Failed to order food.")
                                            elif order_choice == "2":
                                                item_id = input("Enter the drink item ID you want to order: ")
                                                quantity = int(input("Enter the quantity: "))
                                                order_result = order.order_drink(item_id, quantity,table_number)
                                                if order_result:
                                                    print("Drink ordered successfully!")
                                                else:
                                                    print("Failed to order drink.")
                                            elif order_choice == "3":
                                                order.check_bill(table_number)
                                                print("Choose your payment method: \n 1. Cash \n 2. Credit card \n 3.cancel")
                                                choose_payment = input()
                                                if choose_payment == "1":
                                                    print("Payment successful. Thank you for dining with us!")
                                                elif choose_payment == "2":
                                                    print("Payment successful. Thank you for dining with us!")
                                                elif choose_payment == "3":
                                                    print("Payment canceled.")

                                                else:
                                                    print("Invalid choice. Please try again.")
                                            # Add your ordering logic here
                                            order_choice = input("Do you want to order again? (y/n): ")
                                            if order_choice.lower() != "n":
                                                clear_screen()
                                                break
                                    else:
                                        print("Failed to book table.")
                                else:
                                    print("Invalid choice. Please try again.")
                        elif choice == "2":
                            clear_screen()
                            login = False
                            print("Logged out successfully.")
                            return login
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == "2":
            regis = register_function()
            if regis:
                continue
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        



if __name__ == "__main__":
    main()