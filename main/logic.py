import data

def logic_function(input_user : dict):
    '''ฟังก์ชันล็อกอิน'''
    username = input_user['user']
    password = input_user['password']

    datausername = data.login_user(username,password)

    if datausername:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

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