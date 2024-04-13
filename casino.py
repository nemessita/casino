#     login
#     password
#     cash
# Proqram soruşur :
#        Secim edin  (1) Qeydiyyatdan kecin (2) Oyuna basla (3) İstifadəçini bazadan silin (4) Balansi yoxla (5) Cixish
# Qeyd:
#     Qazandıqda pulun üzərinə 10 azn gəlsin
#     Uduzduqda puldan 5 azn çıxsın
#     Loginin bazada olub olmamağını yoxlayın
#     Balansın mənfiyə getməyinin qarşısını alın
#     Əgər kifayət qədər balans yoxdursa -  (2) oyuna başla düyməsi basıldıqda error qaytarsın

import sqlite3
from random import randint

db = sqlite3.connect("casino.db")
sql = db.cursor()


# sql.execute("""CREATE TABLE IF NOT EXISTS users(
            
#             id INTEGER PRIMARY KEY AUTOINCREMENT, 
#             username VARCHAR(50) NOT NULL, 
#             password VARCHAR(50) NOT NULL,
#             cash INTEGER NOT NULL CHECK (cash >= 0)
#             )""")

def register_user():
    username = input("login: ")
    password = input("password: ")
    cash = int(input("cash: "))
    
    sql.execute("SELECT * FROM users WHERE username=?", (username,))
    if sql.fetchone():
        print("qeydiyyayin artiq var!")
    else:
        sql.execute(f"INSERT INTO users (username, password, cash) VALUES ('{username}', '{password}', '{cash}')")
        db.commit()
        print("qeseng!!")

def play_game():
    username = input("Username: ")
    password = input("Password: ")
    
  
    sql.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = sql.fetchone()
    
    if user:
        sql.execute("SELECT cash FROM users WHERE username = ?", (username,))
        balance = sql.fetchone()[0]
        if balance <= 0:
            print("yeterince mebleg yoxdur")
            return
        choose_num = randint(1, 15)
        if choose_num in [1, 2, 3, 4, 5, 6, 7]:
            sql.execute("UPDATE users SET cash = cash + ? WHERE username = ?", (10, username))
            print("win!")
        elif choose_num in [8, 9, 10, 11, 12, 13, 14, 15]:
            sql.execute("UPDATE users SET cash = cash - ? WHERE username = ?", (5, username))
            print("lose!")
        db.commit()

        sql.execute("SELECT cash FROM users WHERE username = ?", (username,))
        balance = sql.fetchone()[0]
        print(f"Your balance: {balance}")
    else:
        print("sehv login ya parol.")

def delete_user():

    username = input("Enter username to delete: ")
    sql.execute("DELETE FROM users WHERE username=?", (username,))
    db.commit()
    print(f"User '{username}' deleted.")

def check_balance():
    username = input("balansin yoxla : ")
    sql.execute("SELECT cash FROM users WHERE username=?", (username,))
    result = sql.fetchone()
    if result:
        print(f"Balance for {username}: {result[0]}")
    else:
        print("bele login yoxdur.")

def main():
    while True:
        choice = input("Select an option: (1) Qeydiyyatdan kecin (2) Oyuna basla  (3) İstifadəçini bazadan silin (4) Balansi yoxla (5) Cixish1: ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            play_game()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("error_yeniden cehd ele.")

if __name__ == "__main__":
    main()
db.close()

        