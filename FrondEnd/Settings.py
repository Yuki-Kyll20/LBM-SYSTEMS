import tkinter as tk
from tkinter import messagebox
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
validate_password = Main.validate_password
back_to_login = Main.back_to_login
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

def show_settings_screen():
    clear_all()
    
    main_frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    main_frame.pack(fill="both", expand=True)
    
    header_frame = tk.Frame(main_frame, bg="#f7e797", padx=15, pady=12, relief="solid", borderwidth=2)
    header_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Label(header_frame, text="WELCOME — ADMIN", 
             font=FONT_HEADING, bg="#f7e797", fg=TEXT_DARK).pack(side="left")
    
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
        tk.Button(sidebar, text=label, bg=btn_color, fg=TEXT_LIGHT,
                  width=22, font=FONT, relief="flat", command=cmd).pack(pady=1)
    
    tk.Button(sidebar, text="Logout", bg=BTN_RED, fg="white", width=22, font=FONT,
              relief="flat", command=Main.back_to_login).pack(pady=(20, 5))
    
    content = tk.Frame(main_frame, bg="#f9f0c5", padx=20, pady=0)
    content.pack(side="right", fill="both", expand=True)

    settings_canvas = tk.Canvas(content, bg="#f9f0c5", highlightthickness=0)
    settings_scrollbar = tk.Scrollbar(content, orient="vertical", command=settings_canvas.yview)
    settings_body = tk.Frame(settings_canvas, bg="#f9f0c5")
    settings_window = settings_canvas.create_window((0, 0), window=settings_body, anchor="nw")
    settings_body.bind(
        "<Configure>",
        lambda event: settings_canvas.configure(scrollregion=settings_canvas.bbox("all")),
    )
    settings_canvas.bind(
        "<Configure>",
        lambda event: settings_canvas.itemconfigure(settings_window, width=event.width),
    )
    settings_canvas.configure(yscrollcommand=settings_scrollbar.set)
    settings_canvas.pack(side="left", fill="both", expand=True)
    settings_scrollbar.pack(side="right", fill="y")

    # ========== CHANGE PASSWORD ==========
    tk.Label(settings_body, text="CHANGE PASSWORD", font=FONT_HEADING,
             bg="#f9f0c5", fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))

    pass_card = tk.Frame(settings_body, bg="#f7e797", padx=30, pady=25, relief="solid", borderwidth=2)
    pass_card.pack(fill="x", padx=10, pady=(0, 20))

    # Current Password
    tk.Label(pass_card, text="Current Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    curr_frame = tk.Frame(pass_card, bg="#f7e797")
    curr_frame.pack(fill="x", pady=(3, 12))
    e_current = tk.Entry(curr_frame, font=FONT, width=32, show="*", bg="white")
    e_current.pack(side="left")
    show_curr = tk.BooleanVar(value=False)
    def toggle_curr():
        show_curr.set(not show_curr.get())
        e_current.configure(show="" if show_curr.get() else "*")
    tk.Button(curr_frame, text="👁", width=3, command=toggle_curr,
              relief="flat", bg="#ddd").pack(side="right", padx=(5, 0))

    # New Password
    tk.Label(pass_card, text="New Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    new_frame = tk.Frame(pass_card, bg="#f7e797")
    new_frame.pack(fill="x", pady=(3, 12))
    e_new = tk.Entry(new_frame, font=FONT, width=32, show="*", bg="white")
    e_new.pack(side="left")
    show_new = tk.BooleanVar(value=False)
    def toggle_new():
        show_new.set(not show_new.get())
        e_new.configure(show="" if show_new.get() else "*")
    tk.Button(new_frame, text="👁", width=3, command=toggle_new,
              relief="flat", bg="#ddd").pack(side="right", padx=(5, 0))

    # Confirm Password
    tk.Label(pass_card, text="Confirm Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    conf_frame = tk.Frame(pass_card, bg="#f7e797")
    conf_frame.pack(fill="x", pady=(3, 12))
    e_confirm = tk.Entry(conf_frame, font=FONT, width=32, show="*", bg="white")
    e_confirm.pack(side="left")
    show_conf = tk.BooleanVar(value=False)
    def toggle_conf():
        show_conf.set(not show_conf.get())
        e_confirm.configure(show="" if show_conf.get() else "*")
    tk.Button(conf_frame, text="👁", width=3, command=toggle_conf,
              relief="flat", bg="#ddd").pack(side="right", padx=(5, 0))
    
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
            
            want_relogin = messagebox.askyesno(
                "Password Updated",
                "Password updated successfully!\n\nDO YOU WANT TO RE-LOGIN NOW?\n\n• YES → Login Page\n• NO → Stay logged in"
            )
            if want_relogin:
                Main.set_user_status("Offline")
                back_to_login()
            else:
                messagebox.showinfo("Saved", "Password changed — still logged in.")
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
    tk.Label(settings_body, text="SYSTEM SETTINGS", font=FONT_HEADING,
             bg="#f9f0c5", fg=TEXT_DARK).pack(anchor="w", pady=(10, 15))
    
    sys_card = tk.Frame(settings_body, bg="#f7e797", padx=30, pady=25, relief="solid", borderwidth=2)
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
            if days <= 0 or rate < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid values!")
            return
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE system_settings SET Default_Loan_Days=%s, Fine_Rate_Per_Day=%s", (days, rate))
            conn.commit()
            messagebox.showinfo("Saved", "Settings saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    tk.Button(sys_card, text="SAVE ALL SETTINGS", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, command=save_system_settings).pack(pady=10)

def go_home(): import AdminDB; AdminDB.show_admin_dashboard()
def go_books(): import books; books.show_books_screen()
def go_authors(): import Authors; Authors.show_authors_screen()
def go_categories(): import Category; Category.show_categories_screen()
def go_reading(): import AdminBorrow; AdminBorrow.show_admin_borrow_screen()
def go_collection(): import admin_Collection; admin_Collection.show_admin_collection_screen()
def go_account(): import Account; Account.show_account_screen()
