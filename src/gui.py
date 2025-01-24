# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:38:06 2023

@author: David Miszczyk U.I. Chicago, CS 480, Fall 2023
The link to GUI code is below
https://www.geeksforgeeks.org/create-a-modern-login-ui-using-customtkinter-module-in-python/
"""
import MySQLdb.cursors, re, hashlib
import customtkinter as ctk 
import tkinter.messagebox as tkmb
import mysql.connector
import MySQLdb.cursors, re, hashlib
import tkinter as tk
# The link below shows documention about CustomTkinter
# https://customtkinter.tomschimansky.com/documentation/


# This function is used to check inputs after the inputs get submitted for every command or functionality that is required.
# Note, adding to any table does not allow for an empty input. E.g. MI field in nurse can not be empty.
def check_inputs_and_submit(dbConn, entries, command, app):
    if any(not entry.get() for entry in entries):
        raise Exception("Invalid input to check_inputs_and_submit")

    if command == 1:
        submitA1(dbConn, [entry.get() for entry in entries], app)

    elif command == 2:
        submitA2(dbConn, [entry.get() for entry in entries], app)

    elif command == 3:
        submitA3(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 4:
        submitA4(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 5:
        submitA5(dbConn, [entry.get() for entry in entries], app)
    
    elif command == 6:
        submitA6(dbConn, [entry.get() for entry in entries], app)

    elif command == 7:
        submitA7(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 8:
        submitN8(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 9:
        submitN8(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 10:
        submitN8(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 11:
        submitN8(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 12:
        submitN8(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 13:
        submitP13(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 14:
        submitP14(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 15:
        submitP15(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 16:
        submitP16(dbConn, [entry.get() for entry in entries], app)
        
    elif command == 17:
        submitP17(dbConn, [entry.get() for entry in entries], app)

# Handles patient command #13, i.e. 13. Register: Patients can register their information. In addition to what described
# above, a patient needs to pick a username and a password.
def submitP13(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [values[0], values[1], values[2]]

        sql = """
            INSERT INTO hospital.login (username, password, user_type)
            VALUES (%s, %s, %s);
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        print("Successfully updated login;", params)
        
        sql = """
            INSERT INTO hospital.patient (SSN, Fname, MI, Lname, Age, Gender, Race, OccupationClass, MedicalHistory, Phone, Address, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        params = [values[3], values[4], values[5], values[6], int(values[7]), values[8], values[9], values[10], values[11], values[12], values[13], values[0]] # convert values

        myCursor.execute(sql, params)
        
        dbConn.commit()
        
        print("Successfully updated patient;", params)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitP13 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()


# Handles submit button press for patient command #14
def submitP14(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [values[0], values[1], values[2], values[3], int(values[4]), values[5], values[6], values[7], values[8], values[9], values[10], values[0]]

        sql = """
            UPDATE hospital.patient 
            SET SSN = %s, Fname = %s, MI = %s, Lname = %s, Age = %s, Gender = %s, Race = %s, OccupationClass = %s, MedicalHistory = %s, Phone = %s, Address = %s
            WHERE SSN = %s;
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()

        print("Successfully updated with", params)

        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitP14 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()


# Handles submit button press for patient command #15
# values contains TimeSlotID, SSN
def submitP15(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)
        # VaccineId is the only necessary column
        # selects the first available vaccine.
        sql = """
            SELECT * FROM vaccine WHERE (Availability - OnHold) >= 1 LIMIT 1;
        """
        
        myCursor.execute(sql)
        
        ls1 = myCursor.fetchall()
        
        if not len(ls1):
            raise ValueError("Invalid Vaccine.ID")
        
        print("ls1", ls1)
        # get ScheduleID
        sql = """
            SELECT MAX(ScheduleID) FROM VaccinationScheduling;
        """

        myCursor.execute(sql)
        
        ls2 = myCursor.fetchall()
        
        if not len(ls2):
            raise ValueError("Invalid ScheduleID")
        
        # check if MaxPatients is at capacity before adding to the schedule
        sql = """
            SELECT COUNT(*) FROM timeslot WHERE TimeSlotID = %s;
        """
        
        param = [int(values[0])]
        
        myCursor.execute(sql, param)
        
        count = myCursor.fetchall()
        
        print("count", count)

        sql = """
            INSERT INTO vaccinationscheduling (ScheduleID, SSN, VaccineID, TimeSlotID)
            VALUES (%s, %s, %s, %s);
        """
        
        # prepare for insertion, the ScheduleID
        if ls2 and ls2[0]:
            n = int(ls2[0][0]) + 1
        
        # note, do the conversion first
        # should contain ScheduleID;int, SSN;string, VaccineID;int, TimeSlotID;int
        params = [n, values[1], int(ls1[0][0]), int(values[0])]
        
        print("params", params) # debug

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        sql = """
            UPDATE vaccine set OnHold = OnHold + 1 WHERE VaccineID = %s;
        """
        
        params2 = [params[2]]
        
        myCursor.execute(sql, params2)
        
        dbConn.commit()
        
        print("Successfully added to vaccine schedule values", params, "and put vaccine on hold")

        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitP15 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()
        
# Handles patient command #16 Cancel schedule
# Takes only ScheduleID
def submitP16(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [int(values[0])]

        sql = """
            DELETE FROM vaccinationscheduling WHERE ScheduleID = %s;
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        rows = myCursor.fetchall()
        
        if not len(rows):
            raise ValueError("Invalid ScheduleID")
        
        dbConn.commit()

        print("Successfully deleted from vaccinationscheduling", params)

        app.destroy()

    except Exception as er:
        # print the contents of Login and Nurse
        print("submitP14 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# Helper for command 17 option 1; patients can see their information
# params contains SSN only
def helper1(params, dbConn):
    sql = """
        SELECT * FROM patient WHERE SSN = %s;
    """

    myCursor = dbConn.cursor()
    
    myCursor.execute(sql, params)
    
    rows = myCursor.fetchall()
    
    
        
# Handles patient command #17 view information
# Takes only SSN and option; 1 or 2 or 3
def submitP17(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [values[0]]
        
        if values[1] == '1':
            helper1(params, dbConn)
            
        elif values[1] == '2':
            helper2(params, dbConn)
            
        elif values[1] == '3':
            helper3(params, dbConn)
            
        else:
            raise ValueError("Invalid option")

        sql = """
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        rows = myCursor.fetchall()
        
        if not len(rows):
            raise ValueError("Invalid ScheduleID")
        
        dbConn.commit()

        print("Successfully deleted from vaccinationscheduling", params)

        app.destroy()

    except Exception as er:
        # print the contents of Login and Nurse
        print("submitP17 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# Handles nurse command #8 Update Information
def submitN8(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [values[1], values[2], int(values[0])]

        sql = """
            UPDATE hospital.Nurse
            SET nurse.Phone = %s, nurse.Address = %s
            WHERE nurse.EmployeeID = %s;
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        print("Successfully updated with", params)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("X submitN8 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# Handles nurse command #10 cancel a time
def submitN10(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        params = [int(values[0])]
        
        sql = """
            DELETE FROM vaccinationrecord WHERE TimeSlotID = %s;
        """
        
        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()

        sql = """
            DELETE FROM nursescheduling WHERE TimeSlotID = %s;
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        sql = """
            DELETE FROM vaccinationscheduling WHERE TimeSlotID = %s;
        """

        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        sql = """
            DELETE FROM timeslot WHERE TimeSlotID = %s;
        """
        
        myCursor.execute(sql, params) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        
        print("Successfully deleted", params)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitN10 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# Handles insertion to Hospital.Login of a nurse type.
def submitA1(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        login_values = [values[0], values[1], values[2]] # Login table
        # note, do the conversion first
        nurse_values = [int(values[3]), values[4], values[5], values[6], int(values[7]), values[8], values[9], values[10], values[0]] # Nurse table
        
        sql = """insert into hospital.Login (username,password,user_type) values (%s,%s,%s);"""

        myCursor.execute(sql, login_values)
        
        dbConn.commit()
        
        sql = """insert into hospital.Nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address, username) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        myCursor.execute(sql, nurse_values)
        
        dbConn.commit()
        
        print("Successfully added", nurse_values)

        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA1 failed:", er)
        app.destroy()

    finally:
        myCursor.close()

# Handles update of hospital.Nurse. Note, the employee does not change, only the 5 fields do.
def submitA2(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        nurse_values = [values[1], values[2], values[3], int(values[4]), values[5], int(values[0])]
        
        sql = """
            UPDATE hospital.Nurse
            SET Fname = %s, MI = %s, Lname = %s, Age = %s, Gender = %s
            WHERE EmployeeID = %s;
        """

        myCursor.execute(sql, nurse_values) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        print("Successfully updated with", nurse_values)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA2 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()
        
# Handles update of hospital.Nurse. Note, the employee does not change, only the 5 fields do.
def submitA3(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        nurse_values = [int(values[0])]
        
        sql = """
            DELETE FROM hospital.nurse
            WHERE EmployeeID = %s;
        """

        myCursor.execute(sql, nurse_values) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        print("Successfully deleted EmployeeID", nurse_values)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA3 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# handles the submit action for admin command #4
def submitA4(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        vaccine_values = [int(values[0]), values[1], values[2], int(values[3]), values[4], int(values[5]), int(values[6])]
        
        sql = """
            INSERT INTO hospital.vaccine (VaccineID, Name, Company, DosesRequired, Description, Availability, OnHold)
            VALUES (%s, %s, %s, %s, %s, %s, %s);            
        """

        myCursor.execute(sql, vaccine_values) # note, check Workbench to see changes at this point.
        
        dbConn.commit()
        
        print("Successfully added vaccine", vaccine_values)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA4 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()

# handles the submit action for admin command #5
def submitA5(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        vaccine_values = [int(values[0])]
        
        sql = """DELETE FROM hospital.vaccine WHERE VaccineID = %s and OnHold = 0;"""

        count = myCursor.rowcount

        myCursor.execute(sql, vaccine_values) # note, check Workbench to see changes at this point.
 
        dbConn.commit()
        
        count2 = myCursor.rowcount
        
        if count2 == count:
            print("Error, invalid VaccineID")
            return
        
        print("Successfully removed vaccine", vaccine_values)
        
        app.destroy()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA5 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()



# Helper used to print info for admin command #6.
def printNurseInfo(n_rows, ns_rows):
    if not len(n_rows): # should be 1 nurse
        raise Exception("invalid nurse")

    res = "EmployeeID " + str(n_rows[0][0]) + "\n" + "Fname " + str(n_rows[0][1]) + "\n" + "MI " + str(n_rows[0][2]) + "\n" + "Lname " + str(n_rows[0][3]) + "\n" +  "Age " + str(n_rows[0][4]) + "\n" + "Gender " + str(n_rows[0][5]) + "\n" + "Phone " + str(n_rows[0][6]) + "\n" + "Address " + str(n_rows[0][7])
    res += "\n"
    if len(ns_rows): # nurse can have an empty schedule
        res += "ScheduleID " + str(ns_rows[0][0]) + "\n" + "EmployeeID " + str(ns_rows[0][1]) + "\n" + "TimeSlotID " + str(ns_rows[0][2])
    else:
        res += "The table nursescheduling is empty\n"
    return res
    
# handles the submit action for admin command #6
def submitA6(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        employee_id = [int(values[0])]
        
        sql = """
            SELECT *
            FROM hospital.nurse
            WHERE nurse.EmployeeID = %s;
        """
        
        myCursor.execute(sql, employee_id)
        
        n_rows = myCursor.fetchall()
        
        
        sql = """
            SELECT *
            FROM hospital.nursescheduling
            WHERE nursescheduling.EmployeeID = %s;
        """
        
        myCursor.execute(sql, employee_id)
        
        ns_rows = myCursor.fetchall()
        
        print("nurse", n_rows)
        
        print("scheduling", ns_rows)

        print("Successfully displayed for", employee_id)
        
        app.destroy()
        
        new_window = ctk.CTk()
        
        new_window.title("admin command #6")
        
        new_window.geometry("800x800")
        
        lab = ctk.CTkLabel(new_window, text= "View nurse info")
        
        lab.pack(pady=20)
        
        frame = ctk.CTkFrame(master=new_window)
        
        frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        label_font = ("Arial", 24)
        
        lab = ctk.CTkLabel(master=frame, text= printNurseInfo(n_rows, ns_rows), font=label_font)
        
        lab.pack(pady=20)
        
        new_window.mainloop()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA6 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()
       
        
       
# Helper used to print patient info for admin command #7.
def printPatientInfo(p_rows, vr_rows, vs_rows):
    if not len(p_rows):
        raise Exception("invalid patient") # should be 1 patient

    res = "SSN " + str(p_rows[0][0]) + "\n" + "Fname " + str(p_rows[0][1]) + "\n" + "MI " + str(p_rows[0][2]) + "\n" + "Lname " + str(p_rows[0][3]) + "\n" +  "Age " + str(p_rows[0][4]) + "\n" + "Gender " + str(p_rows[0][5]) + "\n" + "Race " + str(p_rows[0][6]) + "\n" + "OccupationClass " + str(p_rows[0][7]) + "\n" + "MedicalHistory " + str(p_rows[0][8]) + "\n" + "Phone " + str(p_rows[0][9]) + "\n" + "Address " + str(p_rows[0][10])
    res += "\n"
    if len(vr_rows):
        res += "RecordID " + str(vr_rows[0][0]) + "\n" + "SSN " + str(vr_rows[0][1]) + "\n" + "EmployeeID " + str(vr_rows[0][2]) + "\n" + "VaccineID " + str(vr_rows[0][3]) + "\n" + "Dose " + str(vr_rows[0][4]) + "\n" + "TimeSlotID " + str(vr_rows[0][5]) 
    else:
        res += "The table vaccinationrecord is empty\n"
    
    if len(vs_rows):
        res += "ScheduleID " + str(vs_rows[0][0]) + "\n" + "SSN " + str(vs_rows[0][1]) + "\n" + "VaccineID " + str(vs_rows[0][2]) + "\n" + "TimeSlotID " + str(vs_rows[0][3])
    else:
        res += "The table vaccinationscheduling is empty\n"
    return res       
        
# handles the submit action for admin command #7
def submitA7(dbConn, values, app):
    try:
        myCursor = dbConn.cursor()
    
        print("input values", values)

        # note, do the conversion first
        ssn = [values[0]]

        sql = """
            SELECT *
            FROM hospital.patient
            WHERE patient.SSN = %s;
        """
        
        myCursor.execute(sql, ssn)
        
        p_rows = myCursor.fetchall()
        
        sql = """
            SELECT *
            FROM hospital.vaccinationrecord
            WHERE vaccinationrecord.SSN = %s;
        """
        
        myCursor.execute(sql, ssn)
        
        vr_rows = myCursor.fetchall()
        
        sql = """
            SELECT * 
            FROM hospital.vaccinationscheduling
            WHERE vaccinationscheduling.SSN = %s;
        """
        
        myCursor.execute(sql, ssn)
        
        vs_rows = myCursor.fetchall()
        
        print("patient", p_rows)
        
        print("vaccination record", vr_rows)
        
        print("vaccination scheduling", vs_rows)

        print("Successfully displayed for SSN", ssn)
        
        new_window = ctk.CTk()
        
        new_window.title("admin command #7")
        
        new_window.geometry("800x800")
        
        lab = ctk.CTkLabel(new_window, text= "View patient info")
        
        lab.pack(pady=20)
        
        frame = ctk.CTkFrame(master=new_window)
        
        frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        label_font = ("Arial", 24)
        
        lab = ctk.CTkLabel(master=frame, text= printPatientInfo(p_rows, vr_rows, vs_rows), font=label_font)
        
        lab.pack(pady=20)
        
        new_window.mainloop()
        
    except Exception as er:
        # print the contents of Login and Nurse
        print("submitA7 failed:", er)
        app.destroy()
 
    finally:
        myCursor.close()
        

# handles command 1 for Admin, tables modified; 1. Login table 2. Nurse.
def comA1(dbConn):
    try:
        myCursor = dbConn.cursor()

        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #1")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Register a nurse with; <username> <password> <user type> <EmployeeID>\n<Fname> <MI> <Lname> <Age> <Gender> <Phone> <Adress>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Register a nurse UI')
        label.pack(pady=12, padx=10)
    
        user_entry = ctk.CTkEntry(master=frame, placeholder_text="username")
        user_entry.pack(pady=12, padx=10)

        user_pass = ctk.CTkEntry(master=frame, placeholder_text="password")
        user_pass.pack(pady=12, padx=10)
        
        
        user_type = ctk.CTkEntry(master=frame, placeholder_text="user type")
        user_type.pack(pady=12, padx=10)
        
        
        user_id = ctk.CTkEntry(master=frame, placeholder_text="employeeID")
        user_id.pack(pady=12, padx=10)
        
        
        user_fname = ctk.CTkEntry(master=frame, placeholder_text="first name")
        user_fname.pack(pady=12, padx=10)
        
        
        user_mi = ctk.CTkEntry(master=frame, placeholder_text="middle initial")
        user_mi.pack(pady=12, padx=10)
        
        
        user_lname = ctk.CTkEntry(master=frame, placeholder_text="last name")
        user_lname.pack(pady=12, padx=10)

        
        user_age = ctk.CTkEntry(master=frame, placeholder_text="age")
        user_age.pack(pady=12, padx=10)
        
        
        user_gender = ctk.CTkEntry(master=frame, placeholder_text="gender")
        user_gender.pack(pady=12, padx=10)
        

        user_phone = ctk.CTkEntry(master=frame, placeholder_text="phone")
        user_phone.pack(pady=12, padx=10)

        user_address = ctk.CTkEntry(master=frame, placeholder_text="address")
        user_address.pack(pady=12, padx=10)
        
        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [user_entry, user_pass, user_type, user_id, user_fname, user_mi, user_lname, user_age, user_gender, user_phone, user_address], 1, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA1 failed:", er)

    finally:
        myCursor.close()
        
# handles command 2 for Admin, tables modified; nurse.
def comA2(dbConn):
    try:
        myCursor = dbConn.cursor()

        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #2")

        label = ctk.CTkLabel(app, text="Set the nurse's EmployeeID to modify; <Fname>, <MI>, <Lname>, <Age>, <Gender>\nUse 0 for empty MI")
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Update nurse info UI')
        label.pack(pady=12, padx=10)

        user_id = ctk.CTkEntry(master=frame, placeholder_text="employeeID")
        user_id.pack(pady=12, padx=10)
        
        
        user_fname = ctk.CTkEntry(master=frame, placeholder_text="first name")
        user_fname.pack(pady=12, padx=10)
        
        
        user_mi = ctk.CTkEntry(master=frame, placeholder_text="middle initial")
        user_mi.pack(pady=12, padx=10)
        
        
        user_lname = ctk.CTkEntry(master=frame, placeholder_text="last name")
        user_lname.pack(pady=12, padx=10)

        
        user_age = ctk.CTkEntry(master=frame, placeholder_text="age")
        user_age.pack(pady=12, padx=10)
        
        
        user_gender = ctk.CTkEntry(master=frame, placeholder_text="gender")
        user_gender.pack(pady=12, padx=10)
        
        
        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [user_id, user_fname, user_mi, user_lname, user_age, user_gender], 2, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA2 failed:", er)

    finally:
        myCursor.close()
    
# handles command 3 for admin, tables modified; nurse.
def comA3(dbConn):
    try:
        myCursor = dbConn.cursor()

        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #3")

        label = ctk.CTkLabel(app, text="Set the correct EmployeeID to remove the nurse from Hospital database")
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Delete a nurse UI')
        label.pack(pady=12, padx=10)

        user_id = ctk.CTkEntry(master=frame, placeholder_text="EmployeeID")
        user_id.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [user_id], 3, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA3 failed:", er)

    finally:
        myCursor.close()

# handles command 4 for admin, tables modified; vaccine.
def comA4(dbConn):
    try:
        myCursor = dbConn.cursor()

        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #4")

        label = ctk.CTkLabel(app, text="Type the fields for vaccine: <VaccineID>, <Name>, <Company>, <DosesRequired>, <Description>, <Availability>, <OnHold>\nUse 1 for yes and 0 for no to Availability, OnHold")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Add Vaccine UI')
        label.pack(pady=12, padx=10)

        vaccine_id = ctk.CTkEntry(master=frame, placeholder_text="VaccineID")
        vaccine_id.pack(pady=12, padx=10)
        
        vaccine_name = ctk.CTkEntry(master=frame, placeholder_text="Name")
        vaccine_name.pack(pady=12, padx=10)
        
        vaccine_co = ctk.CTkEntry(master=frame, placeholder_text="Company")
        vaccine_co.pack(pady=12, padx=10)
        
        vaccine_dose = ctk.CTkEntry(master=frame, placeholder_text="DosesRequired")
        vaccine_dose.pack(pady=12, padx=10)
        
        vaccine_des = ctk.CTkEntry(master=frame, placeholder_text="Description")
        vaccine_des.pack(pady=12, padx=10)
        
        vaccine_av = ctk.CTkEntry(master=frame, placeholder_text="Availability")
        vaccine_av.pack(pady=12, padx=10)
        
        vaccine_oh = ctk.CTkEntry(master=frame, placeholder_text="OnHold")
        vaccine_oh.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [vaccine_id, vaccine_name, vaccine_co, vaccine_dose, vaccine_des, vaccine_av, vaccine_oh], 4, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA4 failed:", er)

    finally:
        myCursor.close()
        
# handles command 4 for admin, tables modified; vaccine.
def comA5(dbConn):
    try:
        myCursor = dbConn.cursor()

        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #5")

        label = ctk.CTkLabel(app, text="Type the field to remove a vaccine not on-hold: <VaccineID>")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Update Vaccine UI')
        label.pack(pady=12, padx=10)

        vaccine_id = ctk.CTkEntry(master=frame, placeholder_text="VaccineID")
        vaccine_id.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [vaccine_id], 5, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA5 failed:", er)

    finally:
        myCursor.close()

# handles command 6 for admin
def comA6(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #6")

        label = ctk.CTkLabel(app, text="Type the field to view nurse info and schedule: <EmployeeID>")
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='View nurse info UI')
        label.pack(pady=12, padx=10)
        
        employee_id = ctk.CTkEntry(master=frame, placeholder_text="EmployeeID")
        employee_id.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [employee_id], 6, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        

    except Exception as er:
        print("comA6 failed:", er)

# handles command 7 for admin
def comA7(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("admin command #7")

        label = ctk.CTkLabel(app, text="Type the field to view the patient info and vaccination history: <SSN>")
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='View patient info UI')
        label.pack(pady=12, padx=10)
        
        ssn = ctk.CTkEntry(master=frame, placeholder_text="SSN")
        ssn.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [ssn], 7, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comA7 failed:", er)
        


# handles command 8 for nurse, i.e. Update information: Nurses can update their address and phone#
def comN8(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("nurse command #8")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Type these fields to update nurse info: <EmployeeID> <Phone> <Address>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Nurse update information')
        label.pack(pady=12, padx=10)
        
        emp = ctk.CTkEntry(master=frame, placeholder_text="EmployeeID")
        emp.pack(pady=12, padx=10)
        
        phone = ctk.CTkEntry(master=frame, placeholder_text="Phone")
        phone.pack(pady=12, padx=10)
        
        address = ctk.CTkEntry(master=frame, placeholder_text="Address")
        address.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [emp, phone, address], 8, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comN8 failed:", er)


# handles command 9 for nurse, i.e. 9. Schedule time: nurses can schedule for time slots that have less than 12 nurses
# scheduled for them.
def comN9(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("nurse command #9")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Enter: <TimeSlotId> already in the Hospital database", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Nurse Schedule time')
        label.pack(pady=12, padx=10)
        
        emp = ctk.CTkEntry(master=frame, placeholder_text="TimeSlotId")
        emp.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [], 9, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comN9 failed:", er)



# handles command 10 for nurse, i.e. 10. Cancel a time: nurses should be able to delete a time they have scheduled for.
def comN10(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("nurse command #10")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Type the field: <TimeSlotID>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Nurse cancel a time UI')
        label.pack(pady=12, padx=10)
        
        my_id = ctk.CTkEntry(master=frame, placeholder_text="TimeSlotID")
        my_id.pack(pady=12, padx=10)
    
        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [my_id], 10, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        
    except Exception as er:
        print("comN10 failed:", er)


# handles command 11 for nurse, i.e. 11. View Information: Nurses can view their information, including the times they
# have scheduled for.
def comN11(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("nurse command #11")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Message: <>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Functionality 11')
        label.pack(pady=12, padx=10)
        
        emp = ctk.CTkEntry(master=frame, placeholder_text="Input 1")
        emp.pack(pady=12, padx=10)
    

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [], 11, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        
    except Exception as er:
        print("comN11 failed:", er)


# handles command 12 for nurse, i.e. 12. Vaccination: upon delivering a vaccine, nurses should record the vaccination
def comN12(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("nurse command #12")
        
        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="Message: <>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Functionality 12')
        label.pack(pady=12, padx=10)
        
        emp = ctk.CTkEntry(master=frame, placeholder_text="Input 1")
        emp.pack(pady=12, padx=10)
    

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [], 12, app))
        button.pack(pady=12, padx=10)

        app.mainloop()
        
    except Exception as er:
        print("comN12 failed:", er)



# handles command 13 for patient, i.e. 13. Register: Patients can register their information. In addition to what described
# above, a patient needs to pick a username and a password.
def comP13(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("patient command #13")
        
        # Create a canvas and a scrollbar
        canvas = tk.Canvas(app)
        scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Place your widgets inside scrollable_frame
        label_font = ("Arial", 24)
        label = ctk.CTkLabel(scrollable_frame, text="Type these fields to add a patient: <username> <password> <user_type>\n<SSN> <Fname> <MI> <Lname> <Age> <Gender>\n<Race> <OccupationClass> <MedicalHistory> <Phone> <Address>", font=label_font)
        label.pack(pady=20)

        # Create input fields and pack them inside scrollable_frame
        user = ctk.CTkEntry(scrollable_frame, placeholder_text="username")
        user.pack(pady=12, padx=10)

        pw = ctk.CTkEntry(scrollable_frame, placeholder_text="password")
        pw.pack(pady=12, padx=10)
        
        myType = ctk.CTkEntry(scrollable_frame, placeholder_text="user type")
        myType.pack(pady=12, padx=10)
        
        ssn = ctk.CTkEntry(scrollable_frame, placeholder_text="SSN")
        ssn.pack(pady=12, padx=10)
        
        first = ctk.CTkEntry(scrollable_frame, placeholder_text="Fname")
        first.pack(pady=12, padx=10)
        
        m = ctk.CTkEntry(scrollable_frame, placeholder_text="MI")
        m.pack(pady=12, padx=10)
        
        last = ctk.CTkEntry(scrollable_frame, placeholder_text="Lname")
        last.pack(pady=12, padx=10)
        
        age = ctk.CTkEntry(scrollable_frame, placeholder_text="Age")
        age.pack(pady=12, padx=10)
        
        gender = ctk.CTkEntry(scrollable_frame, placeholder_text="Gender")
        gender.pack(pady=12, padx=10)
        
        race = ctk.CTkEntry(scrollable_frame, placeholder_text="Race")
        race.pack(pady=12, padx=10)
        
        oc = ctk.CTkEntry(scrollable_frame, placeholder_text="Occupation class")
        oc.pack(pady=12, padx=10)
        
        mh = ctk.CTkEntry(scrollable_frame, placeholder_text="Medical history")
        mh.pack(pady=12, padx=10)
        
        phone = ctk.CTkEntry(scrollable_frame, placeholder_text="Phone")
        phone.pack(pady=12, padx=10)
        
        add = ctk.CTkEntry(scrollable_frame, placeholder_text="Address")
        add.pack(pady=12, padx=10)
        
        button = ctk.CTkButton(scrollable_frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [user, pw, myType, ssn, first, m, last, age, gender, race, oc, mh, phone, add], 13, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comP13 failed:", er)


# handles command 14 for patient, i.e. 14. Update Info: patients can update their information.
def comP14(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("patient command #14")
        
        # Create a canvas and a scrollbar
        canvas = tk.Canvas(app)
        scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Place your widgets inside scrollable_frame
        label_font = ("Arial", 24)
        label = ctk.CTkLabel(scrollable_frame, text="Type these fields to update a patient:\n<SSN> <Fname> <MI> <Lname> <Age> <Gender>\n<Race> <OccupationClass> <MedicalHistory> <Phone> <Address>", font=label_font)
        label.pack(pady=20)

        # Create input fields and pack them inside scrollable_frame
        ssn = ctk.CTkEntry(scrollable_frame, placeholder_text="SSN")
        ssn.pack(pady=12, padx=10)
        
        first = ctk.CTkEntry(scrollable_frame, placeholder_text="Fname")
        first.pack(pady=12, padx=10)
        
        m = ctk.CTkEntry(scrollable_frame, placeholder_text="MI")
        m.pack(pady=12, padx=10)
        
        last = ctk.CTkEntry(scrollable_frame, placeholder_text="Lname")
        last.pack(pady=12, padx=10)
        
        age = ctk.CTkEntry(scrollable_frame, placeholder_text="Age")
        age.pack(pady=12, padx=10)
        
        gender = ctk.CTkEntry(scrollable_frame, placeholder_text="Gender")
        gender.pack(pady=12, padx=10)
        
        race = ctk.CTkEntry(scrollable_frame, placeholder_text="Race")
        race.pack(pady=12, padx=10)
        
        oc = ctk.CTkEntry(scrollable_frame, placeholder_text="Occupation class")
        oc.pack(pady=12, padx=10)
        
        mh = ctk.CTkEntry(scrollable_frame, placeholder_text="Medical history")
        mh.pack(pady=12, padx=10)
        
        phone = ctk.CTkEntry(scrollable_frame, placeholder_text="Phone")
        phone.pack(pady=12, padx=10)
        
        add = ctk.CTkEntry(scrollable_frame, placeholder_text="Address")
        add.pack(pady=12, padx=10)
        
        button = ctk.CTkButton(scrollable_frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [ssn, first, m, last, age, gender, race, oc, mh, phone, add], 14, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comP14 failed:", er)




# Helper that prints the data rows object which has timeslot data.
def printTime(rows):
    text = "<TimeSlotID> <StartTime> <EndTime> <MaxPatients>" 
    text += "\n"
    for r in rows:
        text += str(r)
        text += "\n"
    return text

# handles command 15 for patient, i.e. 15. Schedule a vaccination time: Patients should see the available time slot and be
# able to select one as their schedule.
def comP15(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")
        app.title("Patient command #15")

        label_font = ("Arial", 24)
        
        sql = """SELECT * FROM timeslot;"""
        
        myCursor = dbConn.cursor()
        
        myCursor.execute(sql)
        
        rows = myCursor.fetchall()
        
        printTime(rows)

        label = ctk.CTkLabel(app, text="Type which vaccination time with <TimeSlotID> only\n and <SSN>", font=label_font)
        label.pack(pady=20)
        
        label = ctk.CTkLabel(app, text=printTime(rows), font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Schedule a vaccination time')
        label.pack(pady=12, padx=10)
        
        t = ctk.CTkEntry(master=frame, placeholder_text="TimeSlotID")
        t.pack(pady=12, padx=10)
        
        s = ctk.CTkEntry(master=frame, placeholder_text="SSN")
        s.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [t,s], 15, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comP15 failed:", er)
        

    
# handles command 16 for patient, i.e. 16. Cancel Schedule: Patients can delete their scheduled time (which will also
# release one on-hold vaccine).
def comP16(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")

        app.title("Patient command #16")

        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="To cancel in vaccine scheduling type: <ScheduleID>", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='Cancel Schedule')
        label.pack(pady=12, padx=10)
        
        t = ctk.CTkEntry(master=frame, placeholder_text="ScheduleID")
        t.pack(pady=12, padx=10)     

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [t], 16, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comP16 failed:", er)

# handles command 17 for patient, i.e. 17. View information: Patients can see their information, the times they have
# scheduled for vaccination, and their vaccination history.
def comP17(dbConn):
    try:
        app = ctk.CTk()

        app.geometry("800x800")

        app.title("Patient command #17")

        label_font = ("Arial", 24)

        label = ctk.CTkLabel(app, text="To view patient info type: <SSN>\nType a number only for viewing\n1;patient info 2; times scheduled for vaccination 3; vaccination history", font=label_font)
        label.pack(pady=20)
    
        frame = ctk.CTkFrame(master=app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)
    
        label = ctk.CTkLabel(master=frame, text='view information')
        label.pack(pady=12, padx=10)
        
        s = ctk.CTkEntry(master=frame, placeholder_text="SSN")
        s.pack(pady=12, padx=10)
        
        n = ctk.CTkEntry(master=frame, placeholder_text="Option")
        n.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='submit', command=lambda: check_inputs_and_submit(dbConn, [s, n], 17, app))
        button.pack(pady=12, padx=10)

        app.mainloop()

    except Exception as er:
        print("comP17 failed:", er)


# handles the commands for type of Admin. Maybe it should open a new ctk window and get inputs.
def doAdmin(dbConn):
    label_font = ("Arial", 24)
    dialog = ctk.CTkInputDialog(text="Type in an admin command number only.\n1. Register nurse\n 2. Update nurse info\n 3. Delete nurse\n 4. Add vaccine\n 5. Update vaccine\n 6. View nurse info\n 7. View patient info", title="admin commands",font=label_font)
  
    dialog.geometry("800x800")
  
    text = dialog.get_input()  # waits for input
    
    if text == "1":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected admin functionality #1")
        comA1(dbConn) # add to the database tables Login and Nurse
        
    elif text == "2":
        print("selected admin functionality #2")
        comA2(dbConn)
        
    elif text == "3":
        print("selected admin functionality #3")
        comA3(dbConn)
        
    elif text == "4":
        print("selected admin functionality #4")
        comA4(dbConn)
        
    elif text == "5":
        print("selected admin functionality #5")
        comA5(dbConn)
        
    elif text == "6":
        print("selected admin functionality #6")
        comA6(dbConn)

    elif text == "7":
        print("selected admin functionality #7")
        comA7(dbConn)

    else:
        print("invalid command")
        return


# handles the commands for type of nurse.
def doNurse(dbConn):
    label_font = ("Arial", 24)
    dialog = ctk.CTkInputDialog(text="Type in a nurse command number only.\n8. Update information\n9. Schedule time\n10. Cancel a time\n11. View information\n12. Vaccination", title="nurse commands", font=label_font)
  
    dialog.geometry("800x800")
  
    text = dialog.get_input()  # waits for input
    
    if text == "8":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected nurse functionality #8")
        comN8(dbConn)
        
    elif text == "9":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected nurse functionality #9")
        comN9(dbConn)
        
    elif text == "10":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected nurse functionality #10")
        comN10(dbConn)
        
    elif text == "11":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected nurse functionality #11")
        comN11(dbConn)
        
    elif text == "12":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected nurse functionality #12")
        comN12(dbConn)

    else:
        print("invalid command")
        return
    
# handles the commands for type of patient.
def doPatient(dbConn):
    label_font = ("Arial", 24)
    dialog = ctk.CTkInputDialog(text="Type in a patient command number only.\n13. Register\n14. Update info\n15. Schedule a vaccination time\n16. Cancel schedule\n17. View information", title="patient commands", font=label_font)
  
    dialog.geometry("800x800")
  
    text = dialog.get_input()  # waits for input
    
    if text == "13":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected patient functionality #13")
        comP13(dbConn)
        
    elif text == "14":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected patient functionality #14")
        comP14(dbConn)
        
    elif text == "15":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected patient functionality #15")
        comP15(dbConn)
        
    elif text == "16":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected patient functionality #16")
        comP16(dbConn)
        
    elif text == "17":
        #dialog1 = ctk.CTkInputDialog(text="Enter; username password employeeID ")
        #text1 = dialog1.get_input()
        print("selected patient functionality #17")
        comP17(dbConn)

    else:
        print("invalid command")
        return
    

# Queries the database for login credentials to validate the login. 
# Calls doNurse or doPatient or doAdmin based on user_type in login table.
def login(app, login_values, dbConn):
    	#username = "Geeks"
    	#password = "12345"

        new_window = ctk.CTkToplevel(app) 

        new_window.title("Login info") 

        new_window.geometry("600x400")
        
        dbCursor = dbConn.cursor()
        
        sql = """select * from hospital.Login where login.username = %s and login.password = %s;"""
        
        params = [login_values[0], login_values[1]]
        
        dbCursor.execute(sql, params)
        
        values = dbCursor.fetchall()
        
        # allow patient to self-register

        if not len(values): # check if the query returned for username, password
            print("Login info not found in the Hospital database")
            tkmb.showerror(title="Login Failed",message="Invalid username or password")
            return
        else:
            print("Login info",values)
            
        if values[0][2] == 'admin': # size 1 should be true
            tkmb.showinfo(title="Login Successful",message="Logged in successfully")
            ctk.CTkLabel(new_window, text="Logged in with (username, password, user_type): " + str(values)).pack()
            doAdmin(dbConn)
            
        elif values[0][2] == 'nurse':
            tkmb.showinfo(title="Login Successful",message="Logged in successfully")
            ctk.CTkLabel(new_window, text="Logged in with (username, password, user_type): " + str(values)).pack()
            doNurse(dbConn)
            
        elif values[0][2] == 'patient':
            tkmb.showinfo(title="Login Successful",message="Logged in successfully")
            ctk.CTkLabel(new_window, text="Logged in with (username, password, user_type): " + str(values)).pack()
            doPatient(dbConn)
    
        else: 
            tkmb.showerror(title="Login Failed",message="Invalid username or password")
            


# Handles adding an admin type to the database
def registerAdmin(dbConn):
    print("To do, get <username> <password> <user_type> and add an admin to the database")

# Runs the GUI. This is intended to be run after the DB connection is established in main.
# Return a list with database values if successful, i.e. [username, password, type].
# The list may need to be used in main for operations, e.g. if admin, then provide the 7 different functionalities.
def doGui(dbConn):
    # set up the GUI, Selecting GUI theme - dark, light , system (for system default) 
    ctk.set_appearance_mode("dark") 
    
    # Selecting color theme - blue, green, dark-blue 
    ctk.set_default_color_theme("blue") 
    
    app = ctk.CTk()

    app.geometry("800x800")

    app.title("Main UI using Customtkinter")

    label_font = ("Arial", 24)
    
    label = ctk.CTkLabel(app,text="This is the main UI window.\nClose this window to close the Hospital database connection.", font=label_font) 
    
    label.pack(pady=20) 
    
    frame = ctk.CTkFrame(master=app) 
    frame.pack(pady=20,padx=40,fill='both',expand=True) 
    
    label = ctk.CTkLabel(master=frame,text='Modern Login System UI') 
    label.pack(pady=12,padx=10) 
    
    user_entry = ctk.CTkEntry(master=frame,placeholder_text="Username") 
    user_entry.pack(pady=12,padx=10) 
    
    user_pass = ctk.CTkEntry(master=frame,placeholder_text="Password",show="*") 
    user_pass.pack(pady=12,padx=10)
    
    #user_type = ctk.CTkEntry(master=frame,placeholder_text="User type") 
    #user_type.pack(pady=12,padx=10)

    button = ctk.CTkButton(master=frame,text='Login',command=lambda:login(app, [user_entry.get(), user_pass.get()], dbConn)) 
    button.pack(pady=12,padx=10)
    
    pb = ctk.CTkButton(master=frame,text='Register patient',command=lambda:doPatient(dbConn)) 
    pb.pack(pady=12,padx=10) 
    
    ab = ctk.CTkButton(master=frame,text='Register admin', command=lambda:registerAdmin(dbConn))
    ab.pack(pady=12,padx=10)
    
    checkbox = ctk.CTkCheckBox(master=frame,text='Remember Me') 
    checkbox.pack(pady=12,padx=10) 

    app.mainloop()
