import data

def logic_function(input_user : dict):
    '''ฟังก์ชันล็อกอิน'''
    username = input_user['user']
    password = input_user['password']

    if username == '' and password == '':
        return False

    datausername = data.login_user(username,password)

    if datausername:
        print("Login successful!")
        return True
    elif datausername == False:
        return False
    else:
        print("Invalid username or password. Please try again.")
        return False

