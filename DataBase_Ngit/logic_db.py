import sqlite3

def create_db_table():
    try:
        connect = sqlite3.connect('ngit_users.db') #data basa em sarqum ngit_anunov 
        cur = connect.cursor() # anpayman petqa cursory aktivacnem teche teble chem kara sarqem

        #stexcum em ngit_users aunov table
        cur.execute("""CREATE TABLE IF NOT EXISTS ngit_users (  
            username TEXT,
            password TEXT,
            email TEXT,
            code BLOB DEFUALT 1 
            )""")
    except:
        print("ERROR WITH DATABASE TABLE")
    finally:
        connect.commit() #anpayman petqa commit anem vor stexcvi
        connect.close() # u verjum close anem vor xndir charajana
        print("OK DATABASE TABLE NO PROBLEM")


def push_one_people_info(username:str, password:str, email:str):
    connect = sqlite3.connect('ngit_users.db') #data basa em sarqum ngit_anunov 
    cur = connect.cursor() # anpayman petqa cursory aktivacnem teche teble chem kara sarqem

    user = True
    mail = True
    passw = True

    try:
        if len(username) >= 4:
            print("Username Ok")
        else:
            user = False
            print("Username SIZE don't smoll 4")
            print("Please write again")

        if len(password) >= 8:
            print("Password Ok")
        else:
            passw = False
            print("Password SIZE don't smoll 8")
        
        if "@" in email:
            print("Email Ok")
        else:
            mail = False
            print("Please add [@] -> symbol")

        if user and mail and passw:
            cur.execute("INSERT INTO ngit_users VALUES (?,?,?,?)",(username,password,email,0))
            connect.commit()
            print("INSERT OK NO PROBLEM")
        else:
            print("Qo tvyalner sxal en noric mutqagri")

    finally:
        connect.close()
        #connect close no problem
    
    

def show_all():
    connect = sqlite3.connect('ngit_users.db')

    #Create a cursor
    cur = connect.cursor()

    cur.execute("SELECT rowid, * FROM ngit_users")

    items = cur.fetchall()
    for item in items:
        print(item)

    #Commit our command
    connect.commit()

    #Close our connection
    connect.close()


def delete_all_info():
    connect = sqlite3.connect('ngit_users.db') #data basa em sarqum ngit_anunov 
    cur = connect.cursor() # anpayman petqa cursory aktivacnem teche teble chem kara sarqem

    cur.execute("DROP TABLE ngit_users") # jnjuma im stexcac table # ete eli kanches es functinan error kta
    connect.commit()                      # cani vor arden jnjel enq u cankanum enq noric jnel vor goyutyun chuni
    connect.close()

delete_all_info()