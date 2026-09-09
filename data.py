import sqlite3
def register_datauser(username:str, password:str, firstname:str, lastname:str, phone:int ,email:str = "NULL"):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    sql1 = f"""INSERT INTO User (username","password","firstname","lastname","phone","email")
    VALUES ({username},{password},{firstname},{lastname},{phone},{email})"""
    try :
        cur.execute(sql1)
    except sqlite3.IntegrityError :
        print("ชื่อผู้ใช้ถูกใช้งานไปแล้ว")
    conn.commit()


    rows = cur.rowcount

    print(rows)

    cur.close()
    conn.close()

