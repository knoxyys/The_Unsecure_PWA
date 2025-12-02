import sqlite3 as sql
import time
import random
import security as sec


def insertUser(username, password, DoB, salt):  # updated to include the salt
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE username = ?", (username,)
    )  # this has been added to check for duplicate users
    existing_user = cur.fetchone()
    if existing_user:
        con.close()
        return (
            False  # however it would be nice to tell the user username exists already
        )

    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth, salt) VALUES (?,?,?,?)",
        (username, password, DoB, salt),
    )
    con.commit()
    con.close()


def retrieveUsers(
    username, password
):  # login function (there was a bit of commented code here that i deleted for clarity hopefully that doesnt matter)
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT password, salt FROM users WHERE username == ?",  # this line is fixed
        (username,),
    )

    response = cur.fetchone()

    if response == None:  # if no username found
        con.close()
        return False

    else:
        stored_hashpw, stored_salt = response
        calculated_hashpw = sec.hashstr(password, stored_salt)

        if calculated_hashpw == stored_hashpw:
            # Plain text log of visitor count as requested by Unsecure PWA management
            with open("visitor_log.txt", "r") as file:
                number = int(file.read().strip())
                number += 1
            with open("visitor_log.txt", "w") as file:
                file.write(str(number))
            # Simulate response time of heavy app for testing purposes (why do we need this? who knows)
            time.sleep(random.randint(80, 90) / 1000)

            return True  # put above code under this
        else:
            return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO feedback (feedback) VALUES (?)", (feedback,)
    )  # this line was fixed from sql injection

    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
