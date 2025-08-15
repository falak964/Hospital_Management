import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry  # ✅ Needed for date selection
import page_after_login

def book_appointment():
    global tree
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    # Fonts
    headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
    labelfont = ('Garamond', 14)
    entryfont = ('Garamond', 12)

    # Database
    connector = sqlite3.connect('Appointment.db')  # ✅ fixed typo
    connector.execute("""
        CREATE TABLE IF NOT EXISTS APPOINTMENT_MANAGEMENT (
            PATIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            NAME TEXT,
            EMAIL TEXT,
            PHONE_NO TEXT,
            GENDER TEXT,
            DOB TEXT,
            STREAM TEXT
        )
    """)

    # Functions
    def reset_fields():
        for var in [name_strvar, email_strvar, contact_strvar, gender_strvar, stream_strvar]:
            var.set('')
        dob.set_date(datetime.datetime.now().date())

    def reset_form():
        tree.delete(*tree.get_children())
        reset_fields()

    def display_records():
        tree.delete(*tree.get_children())
        for record in connector.execute('SELECT * FROM APPOINTMENT_MANAGEMENT'):
            tree.insert('', END, values=record)

    def add_record():
        name = name_strvar.get()
        email = email_strvar.get()
        contact = contact_strvar.get()
        gender = gender_strvar.get()
        DOB = dob.get_date()
        stream = stream_strvar.get()

        if not all([name, email, contact, gender, DOB, stream]):
            mb.showerror('Error!', "Please fill all the missing fields!")
            return

        try:
            connector.execute(
                'INSERT INTO APPOINTMENT_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)',
                (name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Success', f"Appointment for {name} booked successfully!")
            reset_fields()
            display_records()
        except Exception as e:
            mb.showerror('Error', f"Failed to add record: {e}")

    def back():
        main.destroy()
        if hasattr(page_after_login, 'page_after_login'):
            page_after_login.page_after_login()

    def remove_record():
        if not tree.selection():
            mb.showerror('Error!', 'Please select a record to delete')
            return
        current_item = tree.focus()
        selection = tree.item(current_item)['values']
        connector.execute('DELETE FROM APPOINTMENT_MANAGEMENT WHERE PATIENT_ID=?', (selection[0],))
        connector.commit()
        mb.showinfo('Deleted', 'Appointment deleted successfully!')
        display_records()

    def view_record():
        if not tree.selection():
            mb.showerror('Error!', 'Please select a record to view')
            return
        selection = tree.item(tree.focus())['values']
        name_strvar.set(selection[1])
        email_strvar.set(selection[2])
        contact_strvar.set(selection[3])
        gender_strvar.set(selection[4])
        dob.set_date(datetime.datetime.strptime(selection[5], "%Y-%m-%d").date())
        stream_strvar.set(selection[6])

    # GUI
    main = Tk()
    main.title('APPOINTMENT MANAGEMENT SYSTEM')
    main.state('zoomed')

    # Variables
    name_strvar = StringVar()
    email_strvar = StringVar()
    contact_strvar = StringVar()
    gender_strvar = StringVar()
    stream_strvar = StringVar()

    # Layout
    Label(main, text="SIDDHESHWAR CLINIC MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

    left_frame = Frame(main, bg='MediumSpringGreen')
    left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

    center_frame = Frame(main, bg='PaleGreen')
    center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

    right_frame = Frame(main, bg="Gray35")
    right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

    # Left frame fields
    Label(left_frame, text="Name", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    Entry(left_frame, textvariable=name_strvar, font=entryfont).pack()

    Label(left_frame, text="Contact Number", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    Entry(left_frame, textvariable=contact_strvar, font=entryfont).pack()

    Label(left_frame, text="Doctor Name", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    Entry(left_frame, textvariable=email_strvar, font=entryfont).pack()

    Label(left_frame, text="Gender", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    OptionMenu(left_frame, gender_strvar, 'Male', 'Female').pack()

    Label(left_frame, text="Date of Appointment", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    dob = DateEntry(left_frame, width=18, font=entryfont, background='darkblue', foreground='white', borderwidth=2)
    dob.pack()

    Label(left_frame, text="Time", font=labelfont, bg='MediumSpringGreen').pack(pady=10)
    Entry(left_frame, textvariable=stream_strvar, font=entryfont).pack()

    Button(left_frame, text='Book Appointment', font=labelfont, command=add_record).pack(pady=20)

    # Center frame
    Button(center_frame, text='Cancel Appointment', font=labelfont, command=remove_record).pack(pady=10)
    Button(center_frame, text='View Appointment', font=labelfont, command=view_record).pack(pady=10)
    Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields).pack(pady=10)
    Button(center_frame, text='Delete All', font=labelfont, command=reset_form).pack(pady=10)
    Button(center_frame, text='Back', font=labelfont, command=back).pack(pady=10)

    # Right frame - Treeview
    Label(right_frame, text='Appointment Record', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

    tree = ttk.Treeview(right_frame, columns=('Patient ID', 'Name', 'Doctor Name', 'Phone No', 'Gender', 'Date', 'Time'), show='headings')
    for col in tree['columns']:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill=BOTH)

    display_records()

    main.mainloop()
