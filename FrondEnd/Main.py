import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sys
import os
import re
from datetime import datetime
import hashlib

# ========== WINDOW SETUP ==========
root = tk.Tk()
root.title("Book Library Management System")
root.geometry("1440x900")
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

# ========== EMAIL VALIDATION ==========
def validate_email(email):
    """
    Rules:
    - Optional field — BUT if typed, MUST be @gmail.com or @email.com only
    - No typos like .cam, .con, etc.
    - No spaces
    """
    if not email or email.strip() == "":
        return True, "Empty — optional field"
    
    email = email.strip()

    if "@" not in email:
        return False, "Email MUST contain @\nExample: name@gmail.com"
    
    # Allowed domains — ONLY these two
    allowed_domains = ["gmail.com", "email.com"]
    
    before_at, after_at = email.split("@", 1)

    if not before_at:
        return False, "Missing text before @"
    
    if after_at not in allowed_domains:
        return False, f"Only these domains allowed:\n✅ @gmail.com\n✅ @email.com\n\nYou typed: @{after_at}"
    
    if " " in email:
        return False, "No spaces allowed"
    
    return True, "Valid"

# ========== PASSWORD VALIDATION ==========
def validate_password(password):
    """
    Rules:
    - At least 8 characters long
    - Only letters (a-z, A-Z) and numbers (0-9)
    - NO special characters allowed
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long!"
    
    if not re.fullmatch(r'[A-Za-z0-9]+', password):
        return False, "Password can only contain letters and numbers!\nNo special characters allowed."
    
    return True, "Valid"

# ========== PASSWORD STRENGTH CHECKER ==========
def check_password_strength(password):
    """Return strength label and color based on password"""
    if len(password) < 8:
        return "Weak — Need 8+ characters", "#b91c1c"
    
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'[0-9]', password): score += 1
    
    if score <= 2:
        return "Weak", "#b91c1c"
    elif score <= 4:
        return "Medium", "#f59e0b"
    else:
        return "Strong", "#c1ff72"
    
# ========== PASSWORD SHOW/HIDE TOGGLE ==========
def create_password_field(parent, label_text, width=45, show_strength_label=True):
    """Create password entry with eye button and strength indicator"""
    strength_label = None
    
    if label_text:
        tk.Label(parent, text=label_text, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    
    row = tk.Frame(parent, bg=BG_CONTENT)
    row.pack(fill="x", pady=3)
    
    entry = tk.Entry(row, width=width, show="*", font=FONT)
    entry.pack(side="left", fill="x", expand=True)
    
    def toggle():
        if entry.cget("show") == "*":
            entry.config(show="")
            eye_btn.config(text="🙈")
        else:
            entry.config(show="*")
            eye_btn.config(text="👁")
    
    def update_strength(*args):
        if strength_label:
            pw = entry.get()
            text, color = check_password_strength(pw)
            strength_label.config(text=f"Strength: {text}", fg=color)
    
    eye_btn = tk.Button(row, text="👁", command=toggle,
                        bg=BG_CONTENT, relief="flat", cursor="hand2",
                        font=("Arial", 12), padx=5)
    eye_btn.pack(side="right")
    
    if show_strength_label:
        strength_label = tk.Label(parent, text="", font=("Arial", 10, "bold"),
                                   bg=BG_CONTENT, anchor="w")
        strength_label.pack(fill="x", pady=(0, 5))
        entry.bind("<KeyRelease>", update_strength)
    
    return entry

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

# ========== USER SESSION — PROTECTED ==========
current_user = {
    "username": None,
    "user_id": None,
    "role": None,
    "email": None,
    "is_admin": False,
    "status": "Offline"
}

def set_user_status(status):
    """Update status in DB + local — Online / Offline"""
    if not current_user["username"]:
        return
    current_user["status"] = status
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE User SET Status=%s WHERE User_ID=%s",
                       (status, current_user["user_id"]))
            conn.commit()
        except Exception as e:
            print(f"Status update: {e}")
        finally:
            conn.close()

def clear_all():
    """Fully clear screen - used for switching between screens"""
    for w in root.winfo_children():
        w.destroy()

def back_to_login():
    confirm = messagebox.askyesno(
        "LOGOUT",
        "ARE YOU SURE YOU WANT TO\nLOGOUT YOUR ACCOUNT?",
        icon="question"
    )
    if confirm:
        set_user_status("Offline")
        current_user["username"] = None
        current_user["user_id"] = None
        current_user["role"] = None
        current_user["email"] = None
        current_user["is_admin"] = False
        current_user["status"] = "Offline"
        clear_all()
        show_login()


def show_exit():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=35)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="Are you sure you want to Exit?",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(5, 20))
    
    btn_frame = tk.Frame(box, bg=BG_CONTENT)
    btn_frame.pack()
    
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=10,
              relief="solid", borderwidth=1, command=lambda: [set_user_status("Offline"), root.quit()]).grid(row=0, column=0, padx=12)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_login).grid(row=0, column=1, padx=12)
    
# ========== FORGOT PASSWORD ==========
def show_forgot_password():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="FORGOT PASSWORD", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    
    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_user = tk.Entry(box, width=45); e_user.pack(pady=3)
    
    tk.Label(box, text="Security Question: What is your favorite book?",
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_answer = tk.Entry(box, width=45); e_answer.pack(pady=3)
    
    e_new = create_password_field(box, "New Password:", width=40, show_strength_label=False)
    e_conf = create_password_field(box, "Confirm Password:", width=40, show_strength_label=False)
    
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
        
        is_valid, msg = validate_password(new_pass)
        if not is_valid:
            messagebox.showerror("Invalid Password", msg)
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT User_ID FROM User WHERE Username=%s AND Security_Answer=%s", (user, ans))
            if cur.fetchone():
                hashed_new = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
                cur.execute("UPDATE User SET Password=%s WHERE Username=%s", (hashed_new, user))
                conn.commit()
                messagebox.showinfo("Success", "Password reset successfully!\nYou can now Login.")
                show_login()
            else:
                messagebox.showerror("Error", "Username or answer incorrect!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
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
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="SIGN UP", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    
    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_user = tk.Entry(box, width=45)
    e_user.pack(pady=3)
    
    tk.Label(box, text="Email:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_email = tk.Entry(box, width=45)
    e_email.pack(pady=3)
    
    tk.Label(box, text="Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    tk.Label(box, text="(8+ characters, letters & numbers only)", 
             font=("Arial", 9), bg=BG_CONTENT, fg="#666", anchor="w").pack(fill="x")
    e_pass = create_password_field(box, "", width=40)
    
    tk.Label(box, text="Security Answer: Favorite Book", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 0))
    e_ans = tk.Entry(box, width=45)
    e_ans.pack(pady=3)

    # ==============================================
    # CREATE ACCOUNT — VALIDATION FIRST
    # ==============================================
    def create_account():
        user = e_user.get().strip()
        email = e_email.get().strip()
        pwd = e_pass.get()
        ans = e_ans.get().strip()
        
        if not all([user, pwd]):
            messagebox.showwarning("Warning", "Username and Password required!")
            return
        
        # Email validation
        if email:
            valid_email, email_msg = validate_email(email)
            if not valid_email:
                messagebox.showerror("Invalid Email", email_msg)
                return
        
        # Password validation
        is_valid, pwd_msg = validate_password(pwd)
        if not is_valid:
            messagebox.showerror("Invalid Password", pwd_msg)
            return
        
        # Security Answer — no special characters
        if not re.fullmatch(r'[A-Za-z0-9\s]+', ans):
            messagebox.showerror(
                "Invalid Security Answer",
                "Can only contain letters, numbers, and spaces!\nNo special characters allowed."
            )
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            if email:
                cur.execute("SELECT User_ID FROM User WHERE Email=%s", (email,))
                if cur.fetchone():
                    messagebox.showerror("Error", "This email is already registered!")
                    return
            hashed_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            cur.execute("""
                INSERT INTO User (Username, Email, Password, Security_Question, Security_Answer, User_Role, Status)
                VALUES (%s, %s, %s, 'What is your favorite book?', %s, 'User', 'Offline')
                """, (user, email if email else None, hashed_pwd, ans))

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
        if current_user["is_admin"]:
            import books
            books.show_books_screen()
        else:
            import user_books
            user_books.show_user_books_screen()
    except ModuleNotFoundError:
        messagebox.showerror(
            "File Missing",
            f"Looking in: {main_dir}\n\nCheck:\n• books.py (Admin)\n• user_books.py (User)\n• Filenames are correct"
        )

# ========== OPEN AUTHORS ==========
def open_authors():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    try:
        if current_user["is_admin"]:
            import Authors
            Authors.show_authors_screen()
        else:
            import user_Authors
            user_Authors.show_user_authors_screen()
    except ModuleNotFoundError as e:
        messagebox.showerror(
            "File Missing",
            f"Looking in: {main_dir}\n\nError: {e}\n\nCheck:\n• Authors.py (Admin)\n• user_Authors.py (User)\n• Filenames are correct"
        )

# ========== OPEN CATEGORIES ==========
def open_categories():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    try:
        if current_user["is_admin"]:
            import Category
            Category.show_categories_screen()
        else:
            import user_Category
            user_Category.show_user_categories_screen()
    except ModuleNotFoundError as e:
        messagebox.showerror(
            "File Missing",
            f"Looking in: {main_dir}\n\nError: {e}\n\nCheck:\n• Category.py (Admin)\n• user_Category.py (User)\n• Filenames are correct"
        )

# ========== OPEN READING RECORDS ==========
def open_reading_records():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    role = current_user.get("role", "")
    is_admin = (role == "Admin")
    
    if is_admin:
        try:
            import AdminBorrow
            AdminBorrow.show_admin_borrow_screen()
        except ModuleNotFoundError as e:
            messagebox.showerror(
                "File Missing",
                f"Looking in: {main_dir}\n\n"
                f"Cannot find AdminBorrow.py\n"
                f"Check filename and folder!\n\nError: {e}"
            )
    else:
        try:
            import UserBorrow
            UserBorrow.show_user_borrow_screen()
        except ModuleNotFoundError as e:
            messagebox.showerror(
                "File Missing",
                f"Looking in: {main_dir}\n\n"
                f"Cannot find UserBorrow.py\n"
                f"Make sure UserBorrow.py is in the same folder!\n\nError: {e}"
            )

# ========== NAVIGATION DASHBOARD ==========
def show_navigation_dashboard():
    clear_all()

    top_header = tk.Frame(root, bg=BG_CONTENT, height=60, relief="solid", borderwidth=1)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)
    
    role = current_user.get("role", "")
    is_admin = (role == "Admin")
    role_label = "ADMIN" if is_admin else "USER"
    tk.Label(top_header, text=f"NAVIGATION DASHBOARD — {role_label}",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)

    search_entry = tk.Entry(top_header, width=35, font=FONT)
    search_entry.pack(side="right", padx=10, pady=12)
    tk.Label(top_header, text="SEARCH:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="right", pady=12)

    def open_notifications():
        if is_admin:
            from AdminDB import show_notifications
            show_notifications()
        else:
            from UserDB import show_notifications
            show_notifications()
    
    tk.Button(top_header, text="🔔", font=("Arial", 16), bg=BG_CONTENT, fg=TEXT_DARK,
              relief="flat", command=open_notifications).pack(side="right", padx=5)

    sidebar = tk.Frame(root, bg=BG_SIDEBAR, width=200, relief="solid", borderwidth=1)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    def go_home():
        if is_admin:
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
        ("Categories", open_categories),
        ("Reading Records", open_reading_records),
        ("My Collection", open_collection),
        ("Account", open_account),
        ("Settings", open_settings),
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
    
    main_content = tk.Frame(content, bg=BG_CONTENT, padx=20, pady=30, relief="solid", borderwidth=1)
    main_content.pack(fill="both", expand=True, padx=10, pady=10)

    # uses single is_admin check
    if is_admin:
        tk.Label(main_content, text="📋 ADMIN NAVIGATION CENTER", font=FONT_HEADING,
                 bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(40, 10))
        tk.Label(main_content, text="Full Access — Manage Books, Users, Records & Collection", 
                 font=FONT, bg=BG_CONTENT, fg="#555").pack()
    else:
        tk.Label(main_content, text="📋 USER NAVIGATION CENTER", font=FONT_HEADING,
                 bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(40, 10))
        tk.Label(main_content, text="Borrow Books, Track Reading Progress & View My Collection", 
                 font=FONT, bg=BG_CONTENT, fg="#555").pack()

    conn = get_db_connection()
    book_count = user_count = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM books")
            book_count = cur.fetchone()[0]
            if is_admin:
                cur.execute("SELECT COUNT(*) FROM User")
                user_count = cur.fetchone()[0]
        except: pass
        finally: conn.close()
    
    status_color = "#22c55e" if current_user["status"] == "Online" else "#ef4444"
    
    status_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    status_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    tk.Label(status_frame, text=f"Status: ", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    tk.Label(status_frame, text=current_user["status"], font=FONT, bg=BG_CONTENT, fg=status_color).pack(side="left")
    tk.Label(status_frame, text=f" | Total Books: {book_count}",
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    if is_admin:
        tk.Label(status_frame, text=f" | Total Users: {user_count}",
                 font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")

# ========== OPEN COLLECTION ==========
def open_collection():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
        
    role = current_user.get("role", "")
    is_admin = (role == "Admin")
    
    try:
        if is_admin:
            import Collection
            Collection.show_admin_collection_screen()
        else:
            import user_Collection
            user_Collection.show_user_collection_screen()
    except ModuleNotFoundError as e:
        messagebox.showerror("File Missing", f"Cannot open My Collection\nError: {e}")


# ========== OPEN ACCOUNT — Works for Admin & User ==========
def open_account():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    try:
        import Account
        Account.show_account_screen()
    except ModuleNotFoundError as e:
        messagebox.showerror(
            "File Missing",
            f"Cannot find Account.py!\n\nError: {e}\n\nMake sure Account.py is in the same folder."
        )

# ========== OPEN SETTINGS ==========
def open_settings():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    
    role = current_user.get("role", "")
    is_admin = (role == "Admin") or current_user.get("is_admin", False)
    
    if is_admin:
        try:
            import Settings  # Admin - Password & System Settings
            Settings.show_settings_screen()
        except ModuleNotFoundError as e:
            messagebox.showerror(
                "File Missing",
                f"Cannot find Settings.py (Admin)\n\nError: {e}"
            )
    else:
        try:
            import User_Settings  # User - password only
            User_Settings.show_user_settings_screen()
        except ModuleNotFoundError as e:
            messagebox.showerror(
                "File Missing",
                f"Cannot find User_Settings.py\n\nError: {e}"
            )


# ========== LOGIN ==========
def show_login():
    for w in root.winfo_children():
        w.destroy()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="EXIT", bg=BTN_RED, fg="white", width=8,
              relief="solid", borderwidth=1, command=show_exit).place(x=1325, y=15)
    
    tk.Label(frame, text="BOOK LIBRARY MANAGEMENT SYSTEM",
             font=("Arial", 18, "bold"), bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(40, 10))
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=60, pady=25)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="LOGIN", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(0, 20))

    tk.Label(box, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_user = tk.Entry(box, width=35)
    e_user.pack(pady=(3, 10))

    tk.Label(box, text="Email:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_email = tk.Entry(box, width=35)
    e_email.pack(pady=(3, 10))

    e_pass = create_password_field(box, "Password:", width=32)
    
    def do_login():
        user = e_user.get().strip()
        pwd = e_pass.get()

        if not all([user, pwd]):
            messagebox.showwarning("Warning", "Username and Password are required!")
            return

        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            hashed_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            cur.execute("SELECT User_ID, User_Role, Email FROM User WHERE Username=%s AND Password=%s", (user, hashed_pwd))
            result = cur.fetchone()

            if result:
                user_id, role, email = result
                is_admin = (role == "Admin")

                current_user["username"] = user
                current_user["user_id"] = user_id
                current_user["role"] = role
                current_user["email"] = email or "—"
                current_user["is_admin"] = (role == "Admin")
                current_user["status"] = "Online"

                set_user_status("Online")
                
                clear_all()
                if is_admin:
                    from AdminDB import show_admin_dashboard
                    show_admin_dashboard()
                else:
                    from UserDB import show_user_dashboard
                    show_user_dashboard()
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password!\n\nPlease try again.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
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

show_login()
root.mainloop()