from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode


def setup_db():
    DB_NAME = 'warehouse'
    TABLES = {}
    TABLES['users'] = (
        "CREATE TABLE `users` ("
        "  `id` varchar(100) NOT NULL,"
        "  `firstName` varchar(50) NOT NULL,"
        "  `lastName` varchar(50) NOT NULL,"
        "  `picture` varchar(100),"
        "  `gender` varchar(20),"
        "  `email` varchar(100),"
        "  `dateOfBirth` varchar(100),"
        "  `phone` varchar(100),"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['posts'] = (
        "CREATE TABLE `posts` ("
        "  `id` varchar(100) NOT NULL,"
        "  `userid` varchar(100) NOT NULL,"
        "  `text` varchar(1000) NOT NULL,"
        "  `image` varchar(200),"
        "  `likes` int,"
        "  `link` varchar(100),"
        "  `publishDate` varchar(100),"
        "  PRIMARY KEY (`id`),"
        "FOREIGN KEY (userid)"
        "REFERENCES users(id)"
        "ON DELETE CASCADE"
        ") ENGINE=InnoDB")

    TABLES['comments'] = (
        "CREATE TABLE `comments` ("
        "  `id` varchar(100) NOT NULL,"
        "  `userid` varchar(100) NOT NULL,"
        "  `postid` varchar(100) NOT NULL,"
        "  `message` varchar(500) NOT NULL,"
        "  `publishDate` varchar(200),"
        "  PRIMARY KEY (`id`),"
        "  FOREIGN KEY (userid)"
            "REFERENCES users(id)"
            "ON DELETE CASCADE,"
        "  FOREIGN KEY (postid)"
            "REFERENCES posts(id)"
            "ON DELETE CASCADE"
        ") ENGINE=InnoDB")

    cnx = mysql.connector.connect(user='dimitris', password='123456')
    cursor = cnx.cursor()

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

def connect_to_db():
    mydb = mysql.connector.connect(user='dimitris', password='123456', database='warehouse')
    return mydb

def close_db(mydb):
    mydb.close()

def insert_user_to_db(mydb, user):
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (id, firstName, lastName) VALUES (%s, %s, %s)"
    val = (user.id, user.firstName, user.lastName)
    try:
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted. - name: ", user.firstName)
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))

    mydb.commit()
    mycursor.close()
    
def insert_post_to_db(mydb, post):
    mycursor = mydb.cursor()
    sql = "INSERT INTO posts (id, userid, text) VALUES (%s, %s, %s)"
    val = (post.id, post.owner, post.text)
    try:
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted. - id: ", post.id)
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    mydb.commit()
    mycursor.close()

def insert_comment_to_db(mydb, comment):
    mycursor = mydb.cursor()
    sql = "INSERT INTO comments (id, userid, postid, message) VALUES (%s, %s, %s, %s)"
    val = (comment.id, comment.owner, comment.post, comment.message)
    try:
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record inserted. - id: ", comment.id)
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
    mydb.commit()
    mycursor.close()