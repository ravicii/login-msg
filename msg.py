import sqlite3
conn=sqlite3.connect('login_msg.sqlite')
cur=conn.cursor()
cur.executescript(
    '''
    CREATE TABLE IF NOT EXISTS Login
    (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Name TEXT NOT NULL,
        Password TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Messages
    (
        id INTEGER NOT NULL,
        from_id INTEGER NOT NULL,
        file_text TEXT NOT NULL
    )
    '''
)
exist=input('Are you an existing user? (y/n): ')
if exist == 'y'or exist == 'Y':
    u_id=int(input('Enter USER ID: '))
    u_pass=input('Enter Password: ')
    try:
        cur.execute('SELECT Name FROM Login WHERE id=?',(u_id,))
        name=cur.fetchone()[0]
        cur.execute('SELECT Password FROM Login WHERE id=?',(u_id,))
        password=cur.fetchone()[0]
    except:
        print('Incorrect User ID!')
        exit(0)
    if u_pass==password:
        print('Welcome',name)
        print('***********************************')
        print('Enter\n1 to Send Messages\n2 to View Messages')
        act=int(input())
        if act==1:
            cur.execute('SELECT id,Name FROM Login')
            all=cur.fetchall()
            print('ID','\t','Name')
            for i,n in all:
                if i==u_id:
                    continue
                print(i,'\t',n)
            rec=int(input('To whom do you want to send message(Enter ID): '))
            cur.execute('SELECT Name FROM Login WHERE id=?',(rec,))
            print('ENTER THE MESSAGE WHICH YOU WANT TO SEND TO',cur.fetchone()[0])
            msg=input()
            cur.execute('INSERT INTO Messages(id,from_id,file_text) VALUES(?,?,?)',(rec,u_id,msg))
        elif act==2:
            cur.execute('SELECT file_text,from_id FROM Messages WHERE id=?',(u_id,))
            rows=cur.fetchall()
            for row in rows:
                cur.execute('SELECT Name FROM Login WHERE id=?',(row[1],))
                fn=cur.fetchone()[0]
                print(row[0],'-',fn)
    else:
        print('Incorrect Password!')
        exit(0)
elif exist=='n' or exist=='N':
    u_n=input('Enter your name: ')
    pas=input('Enter Password: ')
    cur.execute('INSERT INTO Login(Name,Password) VALUES(?,?)',(u_n,pas))
    cur.execute('SELECT id FROM Login WHERE Name=? AND Password=?',(u_n,pas))
    nu_id=cur.fetchone()[0]
    print('YOUR USER ID is:',nu_id)
else:
    print('Invalid Input!')
conn.commit()