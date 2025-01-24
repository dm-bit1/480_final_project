import sys
import mysql.connector
import MySQLdb.cursors, re, hashlib
import gui
import customtkinter as ctk 
import tkinter.messagebox as tkmb

print(sys.executable)

try:
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='password',
                                   database='Hospital'
                                   )
    

    if conn.is_connected():
        print("Successfully connected to MySQL database")
        
        
    myCursor = conn.cursor()
    
    myCursor.execute("""select * from Login;""")
    
    rows = myCursor.fetchall()
    
    print("Logins available", rows)

    gui.doGui(conn)

except mysql.connector.Error as e :
    print("Error while connecting to MySQL", e)
    
finally:
    if conn.is_connected():
        conn.close()
        print("MySQL connection is closed")