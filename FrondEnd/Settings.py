import tkinter as tk
from tkinter import messagebox
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
validate_password = Main.validate_password
create_password_field = Main.create_password_field
BG_MAIN = Main.BG_MAIN
BG_CONTENT = Main.BG_CONTENT
BG_CARD = Main.BG_CARD
BG_SIDEBAR = Main.BG_SIDEBAR
BTN_BROWN = Main.BTN_BROWN
BTN_RED = Main.BTN_RED
BTN_GREEN = Main.BTN_GREEN
BTN_YELLOW = Main.BTN_YELLOW
TEXT_DARK = Main.TEXT_DARK
TEXT_LIGHT = Main.TEXT_LIGHT
FONT = Main.FONT
FONT_TITLE = Main.FONT_TITLE
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
    
    # ---------- HEADER ----------
    header = tk.Frame(main_frame, bg="#f5e9c8", padx=15, pady=12)
    header.pack(fill="x")
    role_label = "ADMIN" if current_user["is_admin"] else "USER"
    tk.Label(header, text=f"{role_label} (SETTINGS SCREEN)",
             font=FONT_TITLE, bg="#f5e9c8", fg=TEXT_DARK).pack(side="left")
    
    # ---------- SIDEBAR ----------
    sidebar = tk.Frame(main_frame, bg=BG_SIDEBAR, width=220, padx=10, pady=15)
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
        tk.Button(sidebar, text=label, bg=btn_color,
                  fg=TEXT_DARK, width=22, font=FONT, relief="solid", borderwidth=1,
                  command=cmd).pack(pady=2)
    
    tk.Button(sidebar, text="Logout", bg=BTN_RED, fg="white", width=22, font=FONT,
              relief="solid", borderwidth=1, command=Main.back_to_login).pack(pady=(30, 5))
    
    # ---------- MAIN CONTENT AREA ----------
    content = tk.Frame(main_frame, bg=BG_CONTENT, padx=20, pady=20)
    content.pack(side="right", fill="both", expand=True)
    
    # ========== CHANGE PASSWORD SECTION ==========
    tk.Label(content, text="CHANGE PASSWORD", font=FONT_HEADING,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    pass_card = tk.Frame(content, bg=BG_CARD, padx=30, pady=20, relief="solid", borderwidth=1)
    pass_card.pack(fill="x", padx=10, pady=(0, 20))
    
    tk.Label(pass_card, text="Current Password:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_current = tk.Entry(pass_card, font=FONT, width=40, show="*")
    e_current.pack(pady=(3, 10))
    
    tk.Label(pass_card, text="New Password:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_new = create_password_field(pass_card, "", width=40)
    
    tk.Label(pass_card, text="Confirm Password:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_confirm = tk.Entry(pass_card, font=FONT, width=40, show="*")
    e_confirm.pack(pady=(3, 10))
    
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
        
        # Use Main's password validation
        is_valid, msg = validate_password(new_p)
        if not is_valid:
            messagebox.showerror("Invalid Password", msg)
            return
        
        user_id = current_user.get("user_id")
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            # Verify current password (hash it)
            curr_hashed = hashlib.sha256(curr.encode('utf-8')).hexdigest()
            cur.execute("SELECT Password FROM User WHERE User_ID=%s", (user_id,))
            result = cur.fetchone()
            if not result or result[0] != curr_hashed:
                messagebox.showerror("Error", "Current password is incorrect!")
                return
            
            # Update to new hashed password
            new_hashed = hashlib.sha256(new_p.encode('utf-8')).hexdigest()
            cur.execute("UPDATE User SET Password=%s WHERE User_ID=%s", (new_hashed, user_id))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            # Clear fields
            e_current.delete(0, tk.END)
            e_new.delete(0, tk.END)
            e_confirm.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    tk.Button(pass_card, text="UPDATE PASSWORD", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, command=change_password).pack(pady=5)
    
    # ========== SYSTEM SETTINGS — ADMIN ONLY ==========
    if current_user["is_admin"]:
        tk.Label(content, text="SYSTEM SETTINGS", font=FONT_HEADING,
                 bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(10, 10))
        
        sys_card = tk.Frame(content, bg=BG_CARD, padx=30, pady=20, relief="solid", borderwidth=1)
        sys_card.pack(fill="x", padx=10)
        
        # Load current settings
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
        
        tk.Label(sys_card, text="Default Loan Days:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
        e_loan_days = tk.Entry(sys_card, font=FONT, width=15)
        e_loan_days.insert(0, str(settings["loan_days"]))
        e_loan_days.pack(pady=(3, 10))
        
        tk.Label(sys_card, text="Fine Rate Per Day:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
        e_fine = tk.Entry(sys_card, font=FONT, width=15)
        e_fine.insert(0, str(settings["fine_rate"]))
        e_fine.pack(pady=(3, 10))
        
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
                  font=FONT, relief="solid", borderwidth=1, command=save_system_settings).pack(pady=5)
    
    else:
        tk.Label(content, text="System Settings — Admin Only",
                 font=FONT, bg=BG_CONTENT, fg="#888").pack(pady=30)

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
        import FrondEnd.user_Collection as user_Collection
        user_Collection.show_user_collection_screen()

def go_account():
    import Account
    Account.show_account_screen()
