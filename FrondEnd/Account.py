import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import Main
import os

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
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

profile_photo = None
profile_label = None

# ==================================================
# ACCOUNT — Works for Admin & User
# ==================================================
def show_account_screen():
    global profile_photo, profile_label
    clear_all()
    
    # ========= MAIN LAYOUT =========
    main_frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    main_frame.pack(fill="both", expand=True)
    
    # ---------- HEADER — MATCHES DASHBOARD EXACTLY ----------
    header_frame = tk.Frame(main_frame, bg="#f7e797", padx=15, pady=12, relief="solid", borderwidth=2)
    header_frame.pack(fill="x", padx=20, pady=20)
    
    role_label = "ADMIN" if current_user.get("role") == "Admin" else "USER"
    tk.Label(header_frame, text=f"WELCOME — {role_label}", 
             font=FONT_HEADING, bg="#f7e797", fg=TEXT_DARK).pack(side="left")
    
    # ---------- SIDEBAR — MATCHES DASHBOARD EXACTLY ----------
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
        ("Account", show_account_screen),
        ("Settings", go_settings),
    ]
    
    for label, cmd in nav_buttons:
        btn_color = BTN_YELLOW if label == "Account" else BTN_BROWN
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

    tk.Label(content, text="PERSONAL INFORMATION", font=FONT_HEADING,
             bg="#f9f0c5", fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))

    info_card = tk.Frame(content, bg="#f7e797", padx=30, pady=25, relief="solid", borderwidth=2)
    info_card.pack(fill="x", padx=10)
    
    # --- PROFILE PICTURE SECTION ---
    pic_frame = tk.Frame(info_card, bg="#f7e797")
    pic_frame.pack(anchor="w", pady=(0, 20))
    
    profile_label = tk.Label(pic_frame, text="PROFILE\nPICTURE",
                             bg="#e8d5b0", fg=TEXT_DARK, font=FONT,
                             width=12, height=5, relief="solid", borderwidth=1)
    profile_label.pack(side="left", padx=(0, 15))
    
    pic_btn_frame = tk.Frame(pic_frame, bg="#f7e797")
    pic_btn_frame.pack(side="left")
    
    tk.Button(pic_btn_frame, text="UPLOAD", bg=BTN_GREEN, fg=TEXT_DARK,
              width=10, font=FONT, relief="solid", borderwidth=1,
              command=upload_profile_pic).pack(pady=2)
    tk.Button(pic_btn_frame, text="REMOVE", bg=BTN_RED, fg="white",
              width=10, font=FONT, relief="solid", borderwidth=1,
              command=remove_profile_pic).pack(pady=2)
    
    load_saved_profile_picture()
    
    # --- USER INFO FIELDS ---
    user_id = current_user.get("user_id", "—")
    username = current_user.get("username", "—")
    email = current_user.get("email", "—")
    role = current_user.get("role", "—")

    print(f"Account Debug → user_id={user_id}, username={username}")
    
    def make_info_field(label_text, value):
        tk.Label(info_card, text=label_text, font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
        entry = tk.Entry(info_card, font=FONT, width=50)
        entry.pack(fill="x")
        entry.insert(0, value)
        entry.configure(state="readonly", bg="#e9e9e9")
        return entry
    
    make_info_field("ID:", str(user_id))
    make_info_field("Username:", username)
    make_info_field("Email:", email)
    
    tk.Label(info_card, text="Password:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    pass_frame = tk.Frame(info_card, bg="#f7e797")
    pass_frame.pack(fill="x")
    
    pass_entry = tk.Entry(pass_frame, font=FONT, width=40)
    pass_entry.pack(side="left")
    pass_entry.insert(0, "************")
    pass_entry.configure(state="readonly")
    
    tk.Button(pass_frame, text="CHANGE", bg=BTN_GREEN, fg=TEXT_DARK,
              width=10, font=FONT, relief="solid", borderwidth=1,
              command=go_settings).pack(side="left", padx=10)
    
    make_info_field("Role:", role)

# ==================================================
# PROFILE PICTURE FUNCTIONS
# ==================================================
def load_saved_profile_picture():
    global profile_photo, profile_label
    user_id = current_user.get("user_id")
    if not user_id:
        return
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT Profile_Picture FROM User WHERE User_ID=%s", (user_id,))
        result = cur.fetchone()
        
        if result and result[0] and result[0] != "":
            file_path = result[0]
            if os.path.exists(file_path):
                display_image(file_path)
            else:
                reset_picture_placeholder()
        else:
            reset_picture_placeholder()
    except Exception as e:
        print(f"Load profile pic: {e}")
    finally:
        conn.close()

def display_image(file_path):
    global profile_photo, profile_label
    try:
        img = Image.open(file_path)
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        profile_photo = ImageTk.PhotoImage(img)
        profile_label.config(image=profile_photo, text="", width=100, height=100)
        profile_label.image = profile_photo
    except Exception as e:
        print(f"Display image error: {e}")
        reset_picture_placeholder()

def reset_picture_placeholder():
    global profile_photo, profile_label
    profile_photo = None
    profile_label.config(image="", text="PROFILE\nPICTURE",
                         width=12, height=5, bg="#e8d5b0")
    profile_label.image = None

def upload_profile_pic():
    global profile_photo, profile_label
    
    file_path = filedialog.askopenfilename(
        title="Select Profile Picture",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg"),
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg *.jpeg")
        ]
    )
    
    if not file_path:
        return
    
    user_id = current_user.get("user_id")
    if not user_id:
        messagebox.showwarning("Warning", "No user logged in!")
        return
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(script_dir, "profile_pics")
    os.makedirs(upload_folder, exist_ok=True)
    
    ext = os.path.splitext(file_path)[1].lower()
    new_filename = f"user_{user_id}{ext}"
    save_path = os.path.join(upload_folder, new_filename)
    
    try:
        from shutil import copyfile
        copyfile(file_path, save_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image:\n{e}")
        return
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE User SET Profile_Picture=%s WHERE User_ID=%s",
                    (save_path, user_id))
        conn.commit()
        messagebox.showinfo("Success", "Profile picture updated!")
        display_image(save_path)
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not save:\n{e}")
    finally:
        conn.close()

def remove_profile_pic():
    global profile_photo, profile_label
    
    user_id = current_user.get("user_id")
    if not user_id:
        return
    
    confirm = messagebox.askyesno("Remove Picture", "Remove your profile picture?")
    if not confirm:
        return
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT Profile_Picture FROM User WHERE User_ID=%s", (user_id,))
            result = cur.fetchone()
            old_path = result[0] if result else None
            
            cur.execute("UPDATE User SET Profile_Picture=NULL WHERE User_ID=%s", (user_id,))
            conn.commit()
            
            if old_path and os.path.exists(old_path):
                try: os.remove(old_path)
                except: pass
            
            reset_picture_placeholder()
            messagebox.showinfo("Removed", "Profile picture removed!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

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

def go_navigation():
    if current_user.get("role") == "Admin":
        import AdminDB
        AdminDB.show_navigation_dashboard()
    else:
        import UserDB
        UserDB.show_navigation_dashboard()

def go_settings():
    if current_user.get("role") == "Admin":
        import Settings
        Settings.show_settings_screen()
    else:
        import User_Settings
        User_Settings.show_user_settings_screen()
