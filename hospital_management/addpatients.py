# pip install pymysql
import os
import pymysql
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import page_after_login


def add_patient():
    # --- Database connection function ---
    def connection():
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',       # Change if needed
                password='',       # Change if you have a MySQL password
                database='PATIENTS_DB',
                port=3306
            )
            return conn
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Connection failed:\n{e}")
            raise

    # --- Ensure DB & table exist ---
    def init_db():
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                port=3306
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS PATIENTS_DB")
            cursor.execute("USE PATIENTS_DB")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    MOBILE VARCHAR(15) PRIMARY KEY,
                    NAME VARCHAR(50),
                    DOB DATE,
                    HISTORY TEXT,
                    MEDICINES TEXT
                )
            """)
            conn.commit()
            conn.close()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Init Error", f"Could not initialize DB:\n{e}")
            raise

    # --- Refresh table data ---
    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)
        for array in read():
            my_tree.insert('', 'end', values=array, tag="orow")
        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

    # --- Read all patients ---
    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        results = cursor.fetchall()
        conn.close()
        return results

    # --- Set placeholder ---
    def setph(word, num):
        vars_list = [ph1, ph2, ph3, ph4, ph5]
        vars_list[num-1].set(word)

    # --- Add patient ---
    def add():
        data = (MOBILEEntry.get(), NAMEEntry.get(), DOBEntry.get(), HISTORYEntry.get(), MEDICINESEntry.get())
        if any(x.strip() == "" for x in data):
            messagebox.showwarning("Error", "Please fill all fields")
            return
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patients (MOBILE, NAME, DOB, HISTORY, MEDICINES)
                VALUES (%s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            conn.close()
        except pymysql.IntegrityError:
            messagebox.showerror("Error", "Patient already exists")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))
        refreshTable()

    # --- Reset all data ---
    def reset():
        if messagebox.askyesno("Warning", "Delete all data?"):
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM patients")
                conn.commit()
                conn.close()
                refreshTable()
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", str(e))

    # --- Delete selected ---
    def delete():
        try:
            selected_item = my_tree.selection()[0]
            deleteData = my_tree.item(selected_item)['values'][0]
            if messagebox.askyesno("Warning", "Delete selected data?"):
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM patients WHERE MOBILE=%s", (deleteData,))
                conn.commit()
                conn.close()
                refreshTable()
        except IndexError:
            messagebox.showwarning("Error", "Please select a row")

    # --- Select row ---
    def select():
        try:
            selected_item = my_tree.selection()[0]
            for i, val in enumerate(my_tree.item(selected_item)['values']):
                setph(val, i+1)
        except IndexError:
            messagebox.showwarning("Error", "Please select a row")

    # --- Search patient ---
    def search():
        data = (MOBILEEntry.get(), NAMEEntry.get(), DOBEntry.get(), HISTORYEntry.get(), MEDICINESEntry.get())
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM patients
            WHERE MOBILE=%s OR NAME=%s OR DOB=%s OR HISTORY=%s OR MEDICINES=%s
        """, data)
        result = cursor.fetchall()
        conn.close()
        if result:
            for i, val in enumerate(result[0]):
                setph(val, i+1)
        else:
            messagebox.showinfo("Info", "No data found")

    # --- Update selected ---
    def update():
        try:
            selected_item = my_tree.selection()[0]
            selectedMOBILE = my_tree.item(selected_item)['values'][0]
        except IndexError:
            messagebox.showwarning("Error", "Please select a row")
            return
        data = (MOBILEEntry.get(), NAMEEntry.get(), DOBEntry.get(), HISTORYEntry.get(), MEDICINESEntry.get(), selectedMOBILE)
        if any(x.strip() == "" for x in data[:-1]):
            messagebox.showwarning("Error", "Please fill all fields")
            return
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patients
                SET MOBILE=%s, NAME=%s, DOB=%s, HISTORY=%s, MEDICINES=%s
                WHERE MOBILE=%s
            """, data)
            conn.commit()
            conn.close()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))
        refreshTable()

    # --- Back button ---
    def back():
        root.destroy()
        page_after_login.page_after_login()

    # --- Initialize DB before launching ---
    init_db()

    # --- Main Window ---
    root = Tk()
    root.title("SIDDHESHWAR CLINIC MANAGEMENT SYSTEM")
    root.state('zoomed')
    my_tree = ttk.Treeview(root)

    # --- Placeholders ---
    ph1, ph2, ph3, ph4, ph5 = (tk.StringVar() for _ in range(5))

    Label(root, text="PATIENT DATA MANAGEMENT", font=('Arial Bold', 30)).grid(row=0, column=0, columnspan=8, pady=20)

    labels = ["MOBILE No", "Firstname", "DOB", "Med History", "Medicines"]
    entries = []
    for i, (lbl, var) in enumerate(zip(labels, (ph1, ph2, ph3, ph4, ph5)), start=3):
        Label(root, text=lbl, font=('Arial', 15)).grid(row=i, column=0, padx=20, pady=5)
        entry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=var)
        entry.grid(row=i, column=1, columnspan=4, padx=5)
        entries.append(entry)

    MOBILEEntry, NAMEEntry, DOBEntry, HISTORYEntry, MEDICINESEntry = entries

    # --- Buttons ---
    btns = [
        ("Add", add, "#84F894"),
        ("Update", update, "#84E8F8"),
        ("Delete", delete, "#FF9999"),
        ("Search", search, "#F4FE82"),
        ("Reset", reset, "#F398FF"),
        ("Select", select, "#EEEEEE"),
        ("Back", back, "#94A1FF")
    ]
    for i, (txt, cmd, color) in enumerate(btns, start=3):
        Button(root, text=txt, width=10, bd=5, font=('Arial', 15), bg=color, command=cmd).grid(row=i*2-3, column=10, rowspan=2, pady=5)

    # --- Treeview setup ---
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))
    my_tree['columns'] = ("Mobile", "Firstname", "Date_of_Birth", "HISTORY", "MEDICINES")
    my_tree.column("#0", width=0, stretch=NO)
    for col, w in zip(my_tree['columns'], (170, 150, 150, 165, 150)):
        my_tree.column(col, anchor=W, width=w)
        my_tree.heading(col, text=col, anchor=W)
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

    refreshTable()
    root.mainloop()


if __name__ == "__main__":
    add_patient()
