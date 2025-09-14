import os
from tkinter import *
from tkinter import messagebox as ms
from PIL import ImageTk, Image
import sqlite3
import page_after_login

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
DB_PATH = os.path.join(BASE_DIR, "database1.db")

#load images
def load_image(filename):
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        ms.showerror("Missing Image", f"Image file not found:\n{path}")
        return None
    return Image.open(path)
#Function
def init_db():
    with sqlite3.connect(DB_PATH) as db:
        c = db.cursor()
        # Create table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL ) ''')
        # Insert default admin if table is empty
        c.execute("SELECT COUNT(*) FROM user")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("admin", "admin123"))
        db.commit()

class LoginPage:
    def __init__(self, window):
        init_db() 

        def validate():
            username1 = self.username_entry.get().strip()
            password1 = self.password_entry.get().strip()

            if not username1 or not password1:
                ms.showerror("Error", "Please enter both username and password.")
                return

            with sqlite3.connect(DB_PATH) as db:
                c = db.cursor()
                c.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username1, password1))
                result = c.fetchall()

            if result:
                window.destroy()
                page_after_login.page_after_login()
            else:
                ms.showerror('Oops!', 'Invalid credentials.')

        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        #background image
        bg_img = load_image('background1.png')
        if bg_img:
            self.bg_frame = bg_img
            photo = ImageTk.PhotoImage(self.bg_frame)
            self.bg_panel = Label(self.window, image=photo)
            self.bg_panel.image = photo
            self.bg_panel.pack(fill='both', expand='yes')

        # Login
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)

        #heading
        self.heading = Label(self.lgn_frame, text="WELCOME", font=('yu gothic ui', 25, "bold"), bg="#040405", fg='white', bd=5, relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)
        #Side image
        side_img = load_image('vector.png')
        if side_img:
            photo = ImageTk.PhotoImage(side_img)
            self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')self.side_image_label.image = photo
            self.side_image_label.place(x=5, y=100)

        # Sign in image
        signin_img = load_image('hyy.png')
        if signin_img:
            photo = ImageTk.PhotoImage(signin_img)
            self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
            self.sign_in_image_label.image = photo
            self.sign_in_image_label.place(x=620, y=130)

        # Sign in label
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                   font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # Username label
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405",fg="#6b6a69", font=("yu gothic ui ", 12, "bold"),
                                    insertbackground='#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0,
                                    bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)

        #username icon
        username_icon = load_image('username_icon.png')
        if username_icon:
            photo = ImageTk.PhotoImage(username_icon)
            self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
            self.username_icon_label.image = photo
            self.username_icon_label.place(x=550, y=332)

        # Login button image
        lgn_btn_img = load_image('btn1.png')
        if lgn_btn_img:
            photo = ImageTk.PhotoImage(lgn_btn_img)
            self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
            self.lgn_button_label.image = photo
            self.lgn_button_label.place(x=550, y=450)
            self.login = Button(self.lgn_button_label, text='LOGIN',
                                font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                                bg='#3047ff', cursor='hand2', activebackground='#3047ff',
                                fg='white', command=validate)
            self.login.place(x=20, y=10)

        #Forgot password
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                                    activebackground="#040405", borderwidth=0, background="#040405", cursor="hand2")
        self.forgot_button.place(x=630, y=510)

        # Sign up label
        self.sign_label = Label(self.lgn_frame, text='No account yet?',
                                font=("yu gothic ui", 11, "bold"), relief=FLAT,
                                borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        signup_img = load_image('register.png')
        if signup_img:
            signup_photo = ImageTk.PhotoImage(signup_img)
            self.signup_button_label = Button(self.lgn_frame, image=signup_photo, bg='#98a65d',
                                              cursor="hand2", borderwidth=0, background="#040405",
                                              activebackground="#040405")
            self.signup_button_label.image = signup_photo
            self.signup_button_label.place(x=670, y=555, width=111, height=35)

        # Password label + entry
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405",
                                    fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*",
                                    insertbackground='#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0,
                                    bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        # Password icon
        password_icon = load_image('password_icon.png')
        if password_icon:
            photo = ImageTk.PhotoImage(password_icon)
            self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
            self.password_icon_label.image = photo
            self.password_icon_label.place(x=550, y=414)

        # Show/hide password icons
        show_img = load_image('show.png')
        hide_img = load_image('hide.png')
        if show_img and hide_img:
            self.show_image = ImageTk.PhotoImage(show_img)
            self.hide_image = ImageTk.PhotoImage(hide_img)

            self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                      activebackground="white", borderwidth=0, background="white", cursor="hand2")
            self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')


def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()

