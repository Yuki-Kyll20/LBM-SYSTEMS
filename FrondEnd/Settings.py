import tkinter as tk
from tkinter import messagebox
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
validate_password = Main.validate_password
BG_MAIN = Main.BG_MAIN
BG_SIDEBAR = Main.BG_SIDEBAR
BTN_BROWN = Main.BTN_BROWN
BTN_RED = Main.BTN_RED
BTN_GREEN = Main.BTN_GREEN
BTN_YELLOW = Main.BTN_YELLOW
TEXT_DARK = Main.TEXT_DARK
TEXT_LIGHT = Main.TEXT_LIGHT
FONT = Main.FONT
FONT_HEADING = Main.FONT_HEADING
current_user = Main.current_user

# ==================================================
# SETTINGS — Password Change + System Settings
# ==================================================
def show_settings_screen():
    clear_all()
    
    # ========= MAIN LAYOUT =========
    main_frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    main_frame.pack(fill="both", expand=True)
    
    # ---------- HEADER — MATCH YOUR DESIGN EXACTLY ----------
    header_frame = tk.Frame(main_frame, bg="#f7e797", padx=15, pady=12, relief="solid", borderwidth=2)
    header_frame.pack(fill="x", padx=20, pady=20)
    
    role_label = "ADMIN" if current_user.get("role") == "Admin" else "USER"
    tk.Label(header_frame, text=f"WELCOME — {role_label}", 
             font=FONT_HEADING, bg="#f7e797", fg=TEXT_DARK).pack(side="left")
    
    # ---------- SIDEBAR — MATCH YOUR DESIGN EXACTLY ----------
    sidebar = tk.Frame(main_frame, bg=BG_SIDEBAR, width=220, padx=5, pady=15)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    nav_buttons = [
        ("Home", go_home),
        ("Navigations", Main.show_navigation_dashboard),
        ("Books", go_books),
        ("Authors", go_authors),
        ("Categories", go_categories),
        ("Reading Records", go_reading),
        ("My Collection", go_collection),
        ("Account", go_account),
        ("Settings", show_settings_screen),
    ]
    
    for label, cmd in nav_buttons:
        btn_color = BTN_YELLOW if label == "Settings" else BTN_BROWN
        tk.Button(sidebar, text=label, 
                  bg=btn_color,
                  fg=TEXT_LIGHT,
                  width=22, 
                  font=FONT, 
                  relief="flat",
                  command=cmd).pack(pady=1)
    
    tk.Button(sidebar, text="Logout", bg=BTN_RED, fg="white", width=22, font=FONT,
              relief="flat", command=Main.back_to_login).pack(pady=(20, 5))
    
    # ---------- MAIN CONTENT AREA ----------
    content = tk.Frame(main_frame, bg="#f9f0c5", padx=20, pady=0)
    content.pack(side="right", fill="both", expand=True)
    
    # ========== CHANGE PASSWORD — SHOWN TO ALL ==========
    tk.Label(content, text="CHANGE PASSWORD", font=FONT_HEADING,
             bg="#f9f0c5", fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))

    pass_card = tk.Frame(content, bg="#f7e797", padx=30, pady=25, relief="solid", borderwidth=2)
    pass_card.pack(fill="x", padx=10, pady=(0, 20))

    tk.Label(pass_card, text="Current Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_current = tk.Entry(pass_card, font=FONT, width=40, show="*", bg="white")
    e_current.pack(pady=(3, 12))

    tk.Label(pass_card, text="New Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_new = tk.Entry(pass_card, font=FONT, width=40, show="*", bg="white")
    e_new.pack(pady=(3, 12))

    tk.Label(pass_card, text="Confirm Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_confirm = tk.Entry(pass_card, font=FONT, width=40, show="*", bg="white")
    e_confirm.pack(pady=(3, 12))
    
    def change_password():
        import hashlib
        curr = e_current.get()
        new_p = e_new.get()
        conf = e_confirm.get()
        
        if not all([curr, new_p, conf]):
            messagebox.showwarning("Warning", "Fill in all fields!")
            return
        
        if new_p != conf:
            messagebox.showerror("Error", "New passwords do not match!")
            return
        
        is_valid, msg = validate_password(new_p)
        if not is_valid:
            messagebox.showerror("Invalid Password", msg)
            return
        
        user_id = current_user.get("user_id")
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            curr_hashed = hashlib.sha256(curr.encode('utf-8')).hexdigest()
            cur.execute("SELECT Password FROM User WHERE User_ID=%s", (user_id,))
            result = cur.fetchone()
            if not result or result[0] != curr_hashed:
                messagebox.showerror("Error", "Current password is incorrect!")
                return
            
            new_hashed = hashlib.sha256(new_p.encode('utf-8')).hexdigest()
            cur.execute("UPDATE User SET Password=%s WHERE User_ID=%s", (new_hashed, user_id))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            e_current.delete(0, tk.END)
            e_new.delete(0, tk.END)
            e_confirm.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    tk.Button(pass_card, text="UPDATE PASSWORD", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, command=change_password).pack(pady=10)
    
    # ========== SYSTEM SETTINGS — ADMIN ONLY ==========
    if current_user.get("role") == "Admin":
        tk.Label(content, text="SYSTEM SETTINGS", font=FONT_HEADING,
                 bg="#f9f0c5", fg=TEXT_DARK).pack(anchor="w", pady=(10, 15))
        
        sys_card = tk.Frame(content, bg="#f7e797", padx=30, pady=25, relief="solid", borderwidth=2)
        sys_card.pack(fill="x", padx=10)
        
        settings = {"loan_days": 14, "fine_rate": 5.00}
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT Default_Loan_Days, Fine_Rate_Per_Day FROM system_settings LIMIT 1")
                res = cur.fetchone()
                if res:
                    settings["loan_days"] = res[0]
                    settings["fine_rate"] = float(res[1])
            except Exception as e:
                print(f"Load settings: {e}")
            finally:
                conn.close()
        
        tk.Label(sys_card, text="Default Loan Days:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        e_loan_days = tk.Entry(sys_card, font=FONT, width=15, bg="white")
        e_loan_days.insert(0, str(settings["loan_days"]))
        e_loan_days.pack(pady=(3, 12))
        
        tk.Label(sys_card, text="Fine Rate Per Day:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        e_fine = tk.Entry(sys_card, font=FONT, width=15, bg="white")
        e_fine.insert(0, str(settings["fine_rate"]))
        e_fine.pack(pady=(3, 12))
        
        def save_system_settings():
            try:
                days = int(e_loan_days.get().strip())
                rate = float(e_fine.get().strip())
                if days <= 0 or rate < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Loan Days must be a positive number\nFine Rate must be a valid number!")
                return
            
            conn = get_db_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE system_settings
                    SET Default_Loan_Days=%s, Fine_Rate_Per_Day=%s
                """, (days, rate))
                conn.commit()
                messagebox.showinfo("Saved", "Settings saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        
        tk.Button(sys_card, text="SAVE ALL SETTINGS", bg=BTN_GREEN, fg=TEXT_DARK,
                  font=FONT, relief="solid", borderwidth=1, command=save_system_settings).pack(pady=10)
    
    # ✅ User sees NOTHING extra — only Change Password

# ==================================================
# NAVIGATION HELPERS
# ==================================================
def go_home():
    if current_user.get("role") == "Admin":
        import AdminDB
        AdminDB.show_admin_dashboard()
    else:
        import UserDB
        UserDB.show_user_dashboard()

def go_books():
    if current_user.get("role") == "Admin":
        import Books
        Books.show_books_screen()
    else:
        import user_books
        user_books.show_user_books_screen()

def go_authors():
    if current_user.get("role") == "Admin":
        import Authors
        Authors.show_authors_screen()
    else:
        import user_Authors
        user_Authors.show_user_authors_screen()

def go_categories():
    if current_user.get("role") == "Admin":
        import Category
        Category.show_categories_screen()
    else:
        import user_Category
        user_Category.show_user_categories_screen()

def go_reading():
    if current_user.get("role") == "Admin":
        import AdminBorrow
        AdminBorrow.show_admin_borrow_screen()
    else:
        import UserBorrow
        UserBorrow.show_user_borrow_screen()

def go_collection():
    if current_user.get("role") == "Admin":
        import admin_Collection
        admin_Collection.show_admin_collection_screen()
    else:
        import user_Collection
        user_Collection.show_user_collection_screen()

def go_account():
    import Account
    Account.show_account_screen()