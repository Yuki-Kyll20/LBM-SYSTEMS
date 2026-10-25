import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys
import os

# ========== DATABASE CONNECTOR ==========
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="library_db"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error",
            f"Cannot connect to MySQL:\n{err}\n\nMake sure XAMPP MySQL is running!")
        return None

# ========== WINDOW SETUP ==========
root = tk.Tk()
root.title("Book Library Management System")
root.geometry("1280x720")
root.resizable(False, False)

# ========== COLORS & STYLES ==========
BG_MAIN = "#fef3c7"
BG_SIDEBAR = "#78350f"
BG_CONTENT = "#FFFBEB"
BG_CARD = "#FFF3D0"
BTN_BROWN = "#78350f"
BTN_RED = "#b91c1c"
BTN_GREEN = "#c1ff72"
BTN_YELLOW = "#f59E0B"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#FFFFFF"
LINK_COLOR = "#43acd2"
FONT = ("Arial", 12, "bold")
FONT_TITLE = ("Arial", 14, "bold")
FONT_HEADING = ("Arial", 16, "bold")

# Track logged in user
current_user = None

# ========== HELPER: CLEAR SCREEN ==========
def clear_all():
    for w in root.winfo_children():
        w.destroy()

def back_to_login():
    confirm = messagebox.askyesno(
        "LOGOUT",
        "ARE YOU SURE YOU WANT TO\nLOGOUT YOUR ACCOUNT?",
        icon="question"
    )
    if confirm:
        global current_user
        current_user = None
        clear_all()
        show_login()

# ========== EXIT CONFIRMATION ==========
def show_exit():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=35)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="Are you sure you want to Exit?",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(5, 20))
    
    btn_frame = tk.Frame(box, bg=BG_CONTENT)
    btn_frame.pack()
    
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=10,
              relief="solid", borderwidth=1, command=root.quit).grid(row=0, column=0, padx=12)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_login).grid(row=0, column=1, padx=12)

# ========== FORGOT PASSWORD ==========
def show_forgot_password():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="FORGOT PASSWORD", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    
    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_user = tk.Entry(box, width=45); e_user.pack(pady=3)
    
    tk.Label(box, text="Security Question: What is your favorite book?",
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_answer = tk.Entry(box, width=45); e_answer.pack(pady=3)
    
    tk.Label(box, text="New Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_new = tk.Entry(box, width=45, show="*"); e_new.pack(pady=3)
    
    tk.Label(box, text="Confirm Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_conf = tk.Entry(box, width=45, show="*"); e_conf.pack(pady=3)
    
    def reset_pass():
        user = e_user.get().strip()
        ans = e_answer.get().strip()
        new_pass = e_new.get()
        conf_pass = e_conf.get()
        
        if not all([user, ans, new_pass, conf_pass]):
            messagebox.showwarning("Warning", "Fill in all fields!")
            return
        if new_pass != conf_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT User_ID FROM User WHERE Username=%s AND Security_Answer=%s", (user, ans))
            if cur.fetchone():
                cur.execute("UPDATE User SET Password=%s WHERE Username=%s", (new_pass, user))
                conn.commit()
                messagebox.showinfo("Success", "Password reset successfully!\nYou can now Login.")
                show_login()
            else:
                messagebox.showerror("Error", "Username or answer incorrect!")
        finally:
            conn.close()
    
    tk.Button(box, text="RESET PASSWORD", bg=BTN_BROWN, fg="white", width=20, command=reset_pass).pack(pady=15)
    
    link_frame = tk.Frame(box, bg=BG_CONTENT)
    link_frame.pack()
    tk.Label(link_frame, text="Already have an account? ", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    lbl_login = tk.Label(link_frame, text="Login here", fg=LINK_COLOR, cursor="hand2", font=FONT)
    lbl_login.pack(side="left")
    lbl_login.bind("<Button-1>", lambda e: show_login())

# ========== CREATE ACCOUNT / SIGNUP ==========
def show_signup():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="SIGN UP", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    
    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_user = tk.Entry(box, width=45); e_user.pack(pady=3)
    
    tk.Label(box, text="Email:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_email = tk.Entry(box, width=45); e_email.pack(pady=3)
    
    tk.Label(box, text="Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_pass = tk.Entry(box, width=45, show="*"); e_pass.pack(pady=3)
    
    tk.Label(box, text="Security Answer: Favorite Book", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_ans = tk.Entry(box, width=45); e_ans.pack(pady=3)
    
    def create_account():
        user = e_user.get().strip()
        email = e_email.get().strip()
        pwd = e_pass.get()
        ans = e_ans.get().strip()
        
        if not all([user, pwd]):
            messagebox.showwarning("Warning", "Username and Password required!")
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO User (Username, Email, Password, Security_Answer, User_Role)
                VALUES (%s, %s, %s, %s, 'User')
            """, (user, email if email else None, pwd, ans))
            conn.commit()
            messagebox.showinfo("Account Created", "Account created successfully!\nPlease Login.")
            show_login()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()
    
    tk.Button(box, text="CREATE ACCOUNT", bg=BTN_BROWN, fg="white", width=20, command=create_account).pack(pady=15)
    
    link_frame = tk.Frame(box, bg=BG_CONTENT)
    link_frame.pack()
    tk.Label(link_frame, text="Already have an account? ", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    lbl_login = tk.Label(link_frame, text="Login here", fg=LINK_COLOR, cursor="hand2", font=FONT)
    lbl_login.pack(side="left")
    lbl_login.bind("<Button-1>", lambda e: show_login())

# ========== OPEN BOOKS ==========
def open_books():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    try:
        if current_user and current_user.get('is_admin'):
            import books
            books.show_books_screen()
        else:
            messagebox.showinfo(
                "Coming Soon",
                "User Books List is being set up.\n\nAdmin Books List is ready now!"
            )
    except ModuleNotFoundError:
        messagebox.showerror(
            "File Missing",
            f"Looking in: {main_dir}\n\nCheck:\n• books.py is in this folder\n• Filename: books.py"
        )

# ========== OPEN AUTHORS ==========
def open_authors():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    try:
        if current_user and current_user.get('is_admin'):
            import Authors
            Authors.show_authors_screen()
        else:
            messagebox.showinfo(
                "Coming Soon",
                "User Authors List is being set up.\n\nAdmin Authors List is ready now!"
            )
    except ModuleNotFoundError:
        messagebox.showerror(
            "File Missing",
            f"Looking in: {main_dir}\n\nCheck:\n• Authors.py is in this folder\n• Filename: Authors.py"
        )

# ========== NAVIGATION DASHBOARD ==========
def show_navigation_dashboard():
    clear_all()
    root.configure(bg=BG_MAIN)
    
    top_header = tk.Frame(root, bg=BG_CONTENT, height=60, relief="solid", borderwidth=1)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)
    tk.Label(top_header, text="WELCOME TO NAVIGATION",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)
    
    def open_notifications():
        if current_user and current_user.get('is_admin'):
            from AdminDB import show_notifications
            show_notifications()
        else:
            from UserDB import show_notifications
            show_notifications()
    
    tk.Button(top_header, text="🔔", font=16, bg=BG_CONTENT, fg=TEXT_DARK,
              relief="flat", command=open_notifications).pack(side="right", padx=20)
    
    sidebar = tk.Frame(root, bg=BG_SIDEBAR, width=200, relief="solid", borderwidth=1)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    def go_home():
        if current_user and current_user.get('is_admin'):
            from AdminDB import show_admin_dashboard
            show_admin_dashboard()
        else:
            from UserDB import show_user_dashboard
            show_user_dashboard()
    
    nav_items = [
        ("Home", go_home),
        ("Navigations", show_navigation_dashboard),
        ("Books", open_books),
        ("Authors", open_authors),
        ("Categories", lambda: messagebox.showinfo("Categories", "Categories screen")),
        ("Reading Records", lambda: messagebox.showinfo("Reading Records", "Reading Records screen")),
        ("My Collection", lambda: messagebox.showinfo("My Collection", "My Collection screen")),
        ("Account", lambda: messagebox.showinfo("Account", "Account screen")),
        ("Settings", lambda: messagebox.showinfo("Settings", "Settings screen")),
    ]
    
    for name, cmd in nav_items:
        is_active = (name == "Navigations")
        btn_bg = "#6b3a10" if is_active else BG_SIDEBAR
        tk.Button(sidebar, text=name, font=FONT, bg=btn_bg, fg=TEXT_LIGHT,
                  relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
                  command=cmd).pack(pady=1)
    
    tk.Frame(sidebar, bg="#6b3a10", height=2).pack(fill="x", pady=10)
    
    tk.Button(sidebar, text="Logout", font=FONT, bg=BTN_RED, fg="white",
              relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
              command=back_to_login).pack(pady=5, side="bottom")
    
    content = tk.Frame(root, bg=BG_MAIN)
    content.pack(side="right", fill="both", expand=True)
    
    search_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=12, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(search_frame, text="SEARCH:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=60, font=FONT)
    search_entry.pack(side="left")
    
    main_content = tk.Frame(content, bg=BG_CONTENT, padx=20, pady=30, relief="solid", borderwidth=1)
    main_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    tk.Label(main_content, text="MAIN CONTENT AREA", font=FONT_TITLE,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(60, 10))
    tk.Label(main_content, text="(Tables / Lists / Forms)", font=FONT,
             bg=BG_CONTENT, fg="#555").pack()
    
    conn = get_db_connection()
    book_count = user_count = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM books")
            book_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM User")
            user_count = cur.fetchone()[0]
        except: pass
        finally: conn.close()
    
    status_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    status_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    tk.Label(status_frame, text=f"Status: Ready  |  Total Books: {book_count}  |  Users: {user_count}",
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")

# ========== LOGIN ==========
def show_login():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="EXIT", bg=BTN_RED, fg="white", width=8,
              relief="solid", borderwidth=1, command=show_exit).place(x=1165, y=15)
    
    tk.Label(frame, text="BOOK LIBRARY MANAGEMENT SYSTEM",
             font=("Arial", 18, "bold"), bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(50, 35))
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=60, pady=25)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="LOGIN", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(0, 20))
    
    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_user = tk.Entry(box, width=35)
    e_user.pack(pady=(3, 10))
    
    tk.Label(box, text="Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_pass = tk.Entry(box, width=35, show="*")
    e_pass.pack(pady=(3, 15))
    
    def do_login():
        global current_user
        user = e_user.get().strip()
        pwd = e_pass.get()
        
        if not all([user, pwd]):
            messagebox.showwarning("Warning", "Username and Password are required!")
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT User_ID, User_Role FROM User WHERE Username=%s AND Password=%s", (user, pwd))
            result = cur.fetchone()
            
            if result:
                user_id, role = result
                is_admin = (role == "Admin")
                current_user = {"username": user, "user_id": user_id, "is_admin": is_admin, "role": role}
                clear_all()
                if is_admin:
                    from AdminDB import show_admin_dashboard
                    show_admin_dashboard()
                else:
                    from UserDB import show_user_dashboard
                    show_user_dashboard()
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password!")
        finally:
            conn.close()
    
    tk.Button(box, text="LOGIN", bg="white", fg=TEXT_DARK, width=15,
              relief="solid", borderwidth=1, command=do_login).pack(pady=(0, 20))
    
    lnk_frame = tk.Frame(box, bg=BG_CONTENT)
    lnk_frame.pack()
    
    tk.Label(lnk_frame, text="Don't have an Account? ", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).grid(row=0, column=0)
    lbl_signup = tk.Label(lnk_frame, text="[ Create Account ]", fg=LINK_COLOR, cursor="hand2", font=FONT)
    lbl_signup.grid(row=0, column=1, padx=(5, 0))
    lbl_signup.bind("<Button-1>", lambda e: show_signup())
    
    lbl_forgot = tk.Label(lnk_frame, text="Forgot Password?", fg=LINK_COLOR, cursor="hand2", font=FONT)
    lbl_forgot.grid(row=1, column=0, columnspan=2, pady=(10, 0))
    lbl_forgot.bind("<Button-1>", lambda e: show_forgot_password())

# ========== START APP ==========
show_login()
root.mainloop()