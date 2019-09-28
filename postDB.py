import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS post(
            username VARCHAR2(50),
            shortq VARCHAR2(5000),
            longq VARCHAR2(1000000000000000000),
            img VARCHAR2(500),
            vdo VARCHAR2(500)            
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS postBackUp AS SELECT * FROM post WHERE 1=1;
    """)

def createPost(username,shortq,longq,img,vdo):
    db.execute("INSERT INTO post VALUES (?,?,?,?,?)",(username,shortq,longq,img,vdo))
    db.execute("INSERT INTO postBackUp VALUES (?,?,?,?,?)",(username,shortq,longq,img,vdo))
    con.commit()

def getAllPost():
    db.execute("""
        SELECT u.image,p.username,p.shortq,p.longq,p.img,p.vdo FROM users AS u INNER JOIN post AS p ON (p.username=u.username)
    """)
    post = db.fetchall()
    return post


#createTable()