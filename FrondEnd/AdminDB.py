import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
back_to_login = Main.back_to_login
show_navigation_dashboard = Main.show_navigation_dashboard
current_user = Main.current_user
BG_MAIN = Main.BG_MAIN
BG_SIDEBAR = Main.BG_SIDEBAR
BG_CONTENT = Main.BG_CONTENT
BG_CARD = Main.BG_CARD
BTN_BROWN = Main.BTN_BROWN
BTN_RED = Main.BTN_RED
BTN_GREEN = Main.BTN_GREEN
BTN_YELLOW = Main.BTN_YELLOW
TEXT_DARK = Main.TEXT_DARK
TEXT_LIGHT = Main.TEXT_LIGHT
FONT = Main.FONT
FONT_TITLE = Main.FONT_TITLE
FONT_HEADING = Main.FONT_HEADING

# ==================================================
# ADMIN DASHBOARD — Screens
# ==================================================

def show_overdue_detail():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_notifications).place(x=1130, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="OVERDUE BOOK - USER: Yuki Chan",
             font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    header = tk.Frame(box, bg="#FFF3D0", padx=10, pady=8, relief="solid", borderwidth=1)
    header.pack(fill="x", pady=(0, 1))
    
    tk.Label(header, text="Book Title", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=25, anchor="w").grid(row=0, column=0)
    tk.Label(header, text="Due Date", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=15).grid(row=0, column=1)
    tk.Label(header, text="Day Late", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=12).grid(row=0, column=2)
    tk.Label(header, text="Fine Amount", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=15).grid(row=0, column=3)
    
    row_frame = tk.Frame(box, bg="#7B2CBF", padx=2, pady=2)
    row_frame.pack(fill="x", pady=(0, 15))
    
    row_content = tk.Frame(row_frame, bg=BG_CONTENT, padx=10, pady=10)
    row_content.pack(fill="x")
    
    tk.Label(row_content, text="The atlas 3 days", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=25, anchor="w").grid(row=0, column=0)
    tk.Label(row_content, text="Oct 10, 2026", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15).grid(row=0, column=1)
    tk.Label(row_content, text="3 days", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=12).grid(row=0, column=2)
    tk.Label(row_content, text="₱15.00", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15).grid(row=0, column=3)
    
    total_frame = tk.Frame(box, bg="#FFF3D0", padx=15, pady=12, relief="solid", borderwidth=1)
    total_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(total_frame, text="TOTAL OUTSTANDING FINE: ₱15.00",
             font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w")
    
    btn_frame = tk.Frame(box, bg=BG_CONTENT)
    btn_frame.pack(anchor="w")
    
    tk.Button(btn_frame, text="Mark All Returned", bg=BTN_GREEN, fg=TEXT_DARK, width=20, font=FONT,
              relief="solid", borderwidth=1).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Send Reminder", bg=BTN_YELLOW, fg="#000", width=20, font=FONT,
              relief="solid", borderwidth=1).grid(row=0, column=1, padx=5)

def show_notifications():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1130, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="NOTIFICATIONS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    pending_frame = tk.Frame(box, bg="#FFF3D0", padx=15, pady=15, relief="solid", borderwidth=1)
    pending_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(pending_frame, text="PENDING BORROW REQUESTS:", font=FONT_TITLE,
             bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    req1 = tk.Frame(pending_frame, bg="#FFF3D0")
    req1.pack(fill="x", pady=5)
    tk.Label(req1, text="• Reyna Wants: \"Oshi Mayncrap\"", font=FONT,
             bg="#FFF3D0", fg=TEXT_DARK).pack(side="left")
    tk.Button(req1, text="APPROVE", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1).pack(side="right", padx=3)
    tk.Button(req1, text="REJECT", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1).pack(side="right", padx=3)
    
    req2 = tk.Frame(pending_frame, bg="#FFF3D0")
    req2.pack(fill="x", pady=5)
    tk.Label(req2, text="• Miks Wants: \"Earth 616\"", font=FONT,
             bg="#FFF3D0", fg=TEXT_DARK).pack(side="left")
    tk.Button(req2, text="APPROVE", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1).pack(side="right", padx=3)
    tk.Button(req2, text="REJECT", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1).pack(side="right", padx=3)
    
    overdue_frame = tk.Frame(box, bg="#FFF3D0", padx=15, pady=15, relief="solid", borderwidth=1)
    overdue_frame.pack(fill="x")
    
    tk.Label(overdue_frame, text="OVERDUE BOOKS:", font=FONT_TITLE,
             bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    overdue_item = tk.Frame(overdue_frame, bg="#FFF3D0")
    overdue_item.pack(fill="x", pady=5)
    tk.Label(overdue_item, text="• \"The atlas\" — 3 days late (yuki)", font=FONT,
             bg="#FFF3D0", fg=TEXT_DARK).pack(side="left")
    tk.Button(overdue_item, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_overdue_detail).pack(side="right", padx=3)

def show_add_user():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)

    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(side="right")

    # --- Form Container ---
    form_container = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=30, relief="solid", borderwidth=1)
    form_container.place(relx=0.5, rely=0.45, anchor="center")

    tk.Label(form_container, text="ADD NEW USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

    entries = {}

    # --- Username ---
    tk.Label(form_container, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_user = tk.Entry(form_container, width=45, font=FONT)
    e_user.pack(pady=(0, 10))
    entries["Username"] = e_user

    # --- Email ---
    tk.Label(form_container, text="Email:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_email = tk.Entry(form_container, width=45, font=FONT)
    e_email.pack(pady=(0, 10))
    entries["Email"] = e_email

    # --- Password ---
    tk.Label(form_container, text="Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_pass = tk.Entry(form_container, width=45, show="*", font=FONT)
    e_pass.pack(pady=(0, 10))
    entries["Password"] = e_pass

    # --- Confirm Password ---
    tk.Label(form_container, text="Confirm Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_confirm = tk.Entry(form_container, width=45, show="*", font=FONT)
    e_confirm.pack(pady=(0, 10))
    entries["Confirm Password"] = e_confirm

    # --- Role Dropdown ---
    tk.Label(form_container, text="Role:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    role_var = tk.StringVar(value="User")
    role_select = ttk.Combobox(form_container, textvariable=role_var, values=["User", "Admin"],
                                state="readonly", width=42, font=FONT)
    role_select.pack(pady=(0, 10))
    entries["Role"] = role_var

    # --- Security Question ---
    tk.Label(form_container, text='"What is your favorite book?"', font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_security = tk.Entry(form_container, width=45, font=FONT)
    e_security.pack(pady=(0, 20))
    entries["Security Answer"] = e_security

    # --- CREATE ACCOUNT ---
    def create_account():
        username = entries["Username"].get().strip()
        email = entries["Email"].get().strip()
        password = entries["Password"].get()
        confirm = entries["Confirm Password"].get()
        role = entries["Role"].get()
        answer = entries["Security Answer"].get().strip()

        if not username:
            messagebox.showwarning("Warning", "Username is required!")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if len(password) < 4:
            messagebox.showwarning("Warning", "Password must be at least 4 characters!")
            return
        if not answer:
            messagebox.showwarning("Warning", "Security answer is required!")
            return

        conn = get_db_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO User (Username, Email, Password, Security_Answer, User_Role)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email if email else None, password, answer, role))
            conn.commit()
            messagebox.showinfo("Success", f"User '{username}' created successfully!")
            show_admin_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Username already exists!\n{e}")
        finally:
            conn.close()


    # --- Buttons ---
    btn_frame = tk.Frame(form_container, bg=BG_CONTENT)
    btn_frame.pack(fill="x")

    tk.Button(btn_frame, text="CREATE ACCOUNT", bg=BTN_GREEN, fg=TEXT_DARK, width=20, font=FONT,
              relief="solid", borderwidth=1, command=create_account).pack(side="left", padx=5)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(side="left", padx=5)

def show_all_users():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- BACK Button at Top Right ---
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_admin_dashboard).place(x=1130, y=15)

    # --- Main Box ---
    box = tk.Frame(frame, bg="#FFF3D0", padx=30, pady=25, relief="solid", borderwidth=2)
    box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(box, text="VIEW ALL USERS", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    # --- Table Header ---
    header = tk.Frame(box, bg="#FFF3D0")
    header.pack(fill="x")

    tk.Label(header, text="USERNAME", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=18, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=0)
    tk.Label(header, text="ROLE", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=12, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=1)
    tk.Label(header, text="JOINED DATE", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=22, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=2)

    tk.Frame(box, bg="#000", height=1).pack(fill="x", pady=2)

    # --- Get Users from Database ---
    conn = get_db_connection()
    users = []
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT Username, User_Role, Created_At FROM User ORDER BY Created_At DESC")
            users = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load users:\n{e}")
        finally:
            conn.close()

    if not users:
        tk.Label(box, text="No users found.", font=FONT, bg="#FFF3D0", fg=TEXT_DARK, pady=15).pack()
        return

    # --- User Rows ---
    for username, role, date in users:
        row = tk.Frame(box, bg="#FFF3D0")
        row.pack(fill="x")

        if date:
            month = date.strftime("%b")
            day = date.day
            year = date.year
            date_str = f"Joined {month}.{day}, {year}"
        else:
            date_str = "—"

        tk.Label(row, text=username, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=18, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=0)
        tk.Label(row, text=role, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=12, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=1)
        tk.Label(row, text=date_str, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=22, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=2)
        
def show_user_detail(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1130, y=15)
    
    outer_box = tk.Frame(frame, bg="#7B2CBF", padx=3, pady=3)
    outer_box.place(relx=0.5, rely=0.5, anchor="center")
    
    box = tk.Frame(outer_box, bg=BG_CONTENT, padx=40, pady=30)
    box.pack()
    
    tk.Label(box, text="VIEW USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    profile_frame = tk.Frame(box, bg="#e5d9b6", width=100, height=100, relief="solid", borderwidth=1)
    profile_frame.pack(anchor="w", pady=(0, 20))
    profile_frame.pack_propagate(False)
    tk.Label(profile_frame, text="📷\nPROFILE\nPICTURE", font=("Arial", 9, "bold"),
             bg="#e5d9b6", fg=TEXT_DARK, justify="center").pack()
    
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT User_ID, Username, Email, Password, User_Role FROM User WHERE Username=%s", (username,))
        user = cur.fetchone()
        if user:
            uid, uname, email, password, role = user
            
            def make_display_field(label, value, mask=False):
                tk.Label(box, text=f"{label}:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
                display_val = "●●●●●●●●" if mask else (value or "Not provided")
                tk.Label(box, text=display_val, font=FONT, bg="#e5d9b6", relief="solid", borderwidth=1,
                         width=35, anchor="w", padx=8, pady=5).pack(pady=(0, 10))
            
            make_display_field("ID", str(uid))
            make_display_field("Username", uname)
            make_display_field("Email", email[:3] + "***" if email else "Not provided")
            make_display_field("Password", password, mask=True)
            make_display_field("Role", role.upper() if role else "USER")
        else:
            tk.Label(box, text="User not found.", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load user:\n{e}")
    finally:
        conn.close()

def show_edit_user(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1130, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="EDIT USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    profile_frame = tk.Frame(box, bg="#e5d9b6", width=100, height=100, relief="solid", borderwidth=1)
    profile_frame.pack(anchor="w", pady=(0, 20))
    profile_frame.pack_propagate(False)
    tk.Label(profile_frame, text="📷\nPROFILE\nPICTURE", font=("Arial", 9, "bold"),
             bg="#e5d9b6", fg=TEXT_DARK, justify="center").pack()
    
    conn = get_db_connection()
    if not conn: return
    user_data = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT User_ID, Username, Email, Password, User_Role FROM User WHERE Username=%s", (username,))
        user_data = cur.fetchone()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load user:\n{e}")
        return
    finally:
        conn.close()
    
    if not user_data:
        messagebox.showerror("Error", "User not found!")
        show_admin_dashboard()
        return
    
    uid, uname, email, password, role = user_data
    entries = {}
    
    def make_edit_field(label, value):
        tk.Label(box, text=f"{label}:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
        e = tk.Entry(box, width=35, font=FONT)
        e.insert(0, value or "")
        e.pack(pady=(0, 10))
        entries[label] = e
    
    make_edit_field("Username", uname)
    make_edit_field("Email", email or "")
    make_edit_field("Password", password)
    make_edit_field("Role", role or "User")
    
    def save_changes():
        new_user = entries["Username"].get().strip()
        new_email = entries["Email"].get().strip()
        new_password = entries["Password"].get()
        new_role = entries["Role"].get().strip()
        
        if not new_user:
            messagebox.showwarning("Warning", "Username cannot be empty!")
            return
        
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE User
                SET Username=%s, Email=%s, Password=%s, User_Role=%s
                WHERE User_ID=%s
            """, (new_user, new_email if new_email else None, new_password, new_role, uid))
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully!")
            show_admin_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed!\n{e}")
        finally:
            conn.close()
    
    tk.Button(box, text="SAVE CHANGES", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=save_changes).pack(pady=10)
    tk.Button(box, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(pady=5)

def show_delete_confirm(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1130, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=60, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="DELETE USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(0, 20))
    tk.Label(box, text=f"Are you sure you want to delete the user account?\n\nTHIS ACTION CANNOT BE UNDONE!",
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, justify="center").pack(pady=(0, 25))
    
    def do_delete():
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM User WHERE Username=%s", (username,))
            conn.commit()
            messagebox.showinfo("Deleted", "User account removed successfully!")
            show_admin_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed!\n{e}")
        finally:
            conn.close()
    
    btn_frame = tk.Frame(box, bg=BG_CONTENT)
    btn_frame.pack()
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=do_delete).grid(row=0, column=0, padx=15)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_admin_dashboard).grid(row=0, column=1, padx=15)

# ==================================================
# MAIN ADMIN DASHBOARD
# ==================================================
def show_admin_dashboard():
    clear_all()
    root.configure(bg=BG_MAIN)
    
    top_header = tk.Frame(root, bg=BG_CONTENT, height=60)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)
    
    tk.Label(top_header, text="WELCOME - ADMIN",
             font=FONT_TITLE,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)
    
    tk.Button(top_header, text="🔔", font=16, bg=BG_CONTENT, fg=TEXT_DARK,
              relief="flat", command=show_notifications).pack(side="right", padx=20)
    
    sidebar = tk.Frame(root, bg=BG_SIDEBAR, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    def open_books():
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        try:
            import books
            books.show_books_screen()
        except ModuleNotFoundError:
            messagebox.showerror("Error", "books.py not found!\nCheck filename and folder.")
    
    def open_authors():
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        try:
            import Authors
            Authors.show_authors_screen()
        except ModuleNotFoundError:
            messagebox.showerror("Error", "Authors.py not found!\nCheck filename and folder.")
    
    nav_items = [
        ("Home", show_admin_dashboard),
        ("Navigations", show_navigation_dashboard),
        ("Books", open_books),
        ("Authors", open_authors),
        ("Categories", lambda: messagebox.showinfo("Categories", "Categories screen")),
        ("Reading Records", lambda: messagebox.showinfo("Records", "Reading Records screen")),
        ("My Collection", lambda: messagebox.showinfo("Collection", "My Collection screen")),
        ("Account", lambda: messagebox.showinfo("Account", "Account screen")),
        ("Settings", lambda: messagebox.showinfo("Settings", "Settings screen")),
    ]
    
    for name, cmd in nav_items:
        is_home = (name == "Home")
        btn_bg = "#5c290c" if is_home else BG_SIDEBAR
        tk.Button(sidebar, text=name, font=FONT, bg=btn_bg, fg=TEXT_LIGHT,
                  relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
                  command=cmd).pack(pady=1)
    
    tk.Frame(sidebar, bg="#5c290c", height=2).pack(fill="x", pady=10)
    
    tk.Button(sidebar, text="Logout", font=FONT, bg=BTN_RED, fg="white",
              relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
              command=back_to_login).pack(pady=5, side="bottom")
    
    content = tk.Frame(root, bg=BG_MAIN)
    content.pack(side="right", fill="both", expand=True)
    
    conn = get_db_connection()
    b = a = c = r = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM books"); b = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM authors"); a = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM categories"); c = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM borrow_records"); r = cur.fetchone()[0]
        except Exception as e:
            print(f"Stats: {e}")
        finally:
            conn.close()
    
    stats_frame = tk.Frame(content, bg=BG_MAIN)
    stats_frame.pack(pady=25, padx=20, anchor="w")
    
    stats_data = [
        ("Books", b),
        ("Authors", a),
        ("Categories", c),
        ("Records", r)
    ]
    
    for title, count in stats_data:
        card = tk.Frame(stats_frame, bg=BG_CONTENT, padx=35, pady=20, relief="solid", borderwidth=1)
        card.pack(side="left", padx=8)
        tk.Label(card, text=title, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
        tk.Label(card, text=f"[{count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=5)
    
    tk.Label(content, text="USERS MANAGEMENT", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(20, 5), padx=20)
    
    table_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=15, relief="solid", borderwidth=1)
    table_frame.pack(padx=20, fill="x")
    
    hdr = tk.Frame(table_frame, bg=BG_CONTENT)
    hdr.pack(fill="x", pady=5)
    tk.Label(hdr, text="ID", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=6, anchor="w").grid(row=0, column=0)
    tk.Label(hdr, text="USERNAME", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=15, anchor="w").grid(row=0, column=1)
    tk.Label(hdr, text="ROLE", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=12, anchor="w").grid(row=0, column=2)
    tk.Label(hdr, text="ACTIONS", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=25, anchor="w").grid(row=0, column=3)
    
    tk.Frame(table_frame, bg="#e5cd90", height=1).pack(fill="x", pady=5)
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT User_ID, Username, User_Role FROM User ORDER BY User_ID")
            users = cur.fetchall()
            
            if not users:
                tk.Label(table_frame, text="No users found.",
                         font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
            else:
                for uid, uname, role in users:
                    row = tk.Frame(table_frame, bg=BG_CONTENT)
                    row.pack(fill="x", pady=3)
                    tk.Label(row, text=str(uid), font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=6, anchor="w").grid(row=0, column=0)
                    tk.Label(row, text=uname, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15, anchor="w").grid(row=0, column=1)
                    tk.Label(row, text=role, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=12, anchor="w").grid(row=0, column=2)
                    
                    act = tk.Frame(row, bg=BG_CONTENT)
                    act.grid(row=0, column=3)
                    tk.Button(act, text="VIEW", bg=BTN_YELLOW, fg="#000", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1,
                              command=lambda u=uname: show_user_detail(u)).grid(row=0, column=0, padx=2)
                    tk.Button(act, text="EDIT", bg=BTN_BROWN, fg="white", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1,
                              command=lambda u=uname: show_edit_user(u)).grid(row=0, column=1, padx=2)
                    tk.Button(act, text="DELETE", bg=BTN_RED, fg="white", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1,
                              command=lambda u=uname: show_delete_confirm(u)).grid(row=0, column=2, padx=2)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load users:\n{e}")
        finally:
            conn.close()
    
    tk.Label(content, text="QUICK ACTIONS", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(20, 5), padx=20)
    
    qa_frame = tk.Frame(content, bg=BG_MAIN)
    qa_frame.pack(anchor="w", padx=20)
    
    tk.Button(qa_frame, text="+ ADD NEW USER", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=show_add_user).grid(row=0, column=0, padx=5)
    tk.Button(qa_frame, text="VIEW ALL USERS", bg=BTN_BROWN, fg="white", width=18, font=FONT,
              relief="solid", borderwidth=1, command=show_all_users).grid(row=0, column=1, padx=5)