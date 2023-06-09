import conf
import mysql.connector


# Connect to the database
def connect():
    db_user, db_pass, db_host, db_name = conf.db_creds()
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            auth_plugin='mysql_native_password'
        )
        return mydb
    except Exception as e:
        print(e)
        return None


def connectfirsttime():
    db_user, db_pass, db_host, db_name = conf.db_creds()
    try:
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            auth_plugin='mysql_native_password'
        )
        construct(mydb)
        fill(mydb)
        return "Database cleaned, created and filled !"
    except Exception as e:
        print(e)
        return "Error while cleaning, creating and filling the database !"


def construct(db):
    # Create a db with a name lecamarade
    mycursor = db.cursor()
    # Delete the database if it exists
    mycursor.execute("DROP DATABASE IF EXISTS lecamarade")
    mycursor.execute("CREATE DATABASE IF NOT EXISTS lecamarade")
    mycursor.execute("USE lecamarade")

    # Create a table users with id, pseudo
    mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, pseudo VARCHAR(255), score INT DEFAULT 0)")
    db.commit()


def fill(db):
    camarades = conf.camarades()
    # Insert some users
    mycursor = db.cursor()
    sql = "INSERT INTO users (pseudo) VALUES (%s)"
    val = [
        camarades[0],
        camarades[1],
        camarades[2],
        camarades[3],
        camarades[4]
    ]
    for v in val:
        mycursor.execute(sql, (v,))
    db.commit()


def check_all_users_score():
    db = connect()
    mycursor = db.cursor()
    mycursor.execute("SELECT score FROM users")
    myresult = mycursor.fetchall()
    # check if all users have a score = 0
    for x in myresult:
        if x[0] != 0:
            return True
    return False
