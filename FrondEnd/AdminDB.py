import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import Main
from Main import set_user_status
import hashlib
import mysql.connector
from datetime import date, datetime
from PIL import Image, ImageTk
import os
import shutil
import uuid

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

PROFILE_PICTURE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "profile_pics"
)

def display_user_picture(label, image_path, size=(100, 100)):
    if not image_path or not os.path.isfile(image_path):
        label.config(
            image="", text="PROFILE\nPICTURE", width=12, height=5,
            bg="#e5d9b6",
        )
        label.image = None
        return

    try:
        with Image.open(image_path) as source:
            image = source.convert("RGB")
            image.thumbnail(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo, text="", width=size[0], height=size[1])
        label.image = photo
    except (OSError, tk.TclError) as err:
        messagebox.showerror("Picture Error", f"Could not display profile picture:\n{err}")

def remove_managed_profile_picture(image_path):
    if not image_path:
        return
    try:
        picture_path = os.path.realpath(image_path)
        picture_dir = os.path.realpath(PROFILE_PICTURE_DIR)
        if os.path.commonpath((picture_path, picture_dir)) == picture_dir:
            if os.path.isfile(picture_path):
                os.remove(picture_path)
    except (OSError, ValueError) as err:
        messagebox.showwarning("Picture Cleanup", f"Could not remove old profile picture:\n{err}")

def normalize_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    return None

# ========== PASSWORD HASHING ==========
def hash_password(password):
    """Hash password before storing — SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password_strength(password):
    """Return strength label and color"""
    if len(password) < 8:
        return "Weak — Need 8+ chars", "#b91c1c"
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if score <= 2:
        return "Weak", "#b91c1c"
    elif score <= 4:
        return "Medium", "#f59e0b"
    else:
        return "Strong", "#c1ff72"

# ==================================================
# ADMIN DASHBOARD - NOTIFICATIONS
# ==================================================
def show_overdue_detail(record_id, username, book_title, due_date):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_notifications).place(x=1325, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text=f"OVERDUE BOOK — USER: {username}",
             font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    header = tk.Frame(box, bg="#FFF3D0", padx=10, pady=8, relief="solid", borderwidth=1)
    header.pack(fill="x", pady=(0, 1))
    
    tk.Label(header, text="Book Title", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=25, anchor="w").grid(row=0, column=0)
    tk.Label(header, text="Due Date", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=15).grid(row=0, column=1)
    tk.Label(header, text="Days Late", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=12).grid(row=0, column=2)
    tk.Label(header, text="Fine Amount", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK, width=15).grid(row=0, column=3)
    
    due_date = normalize_date(due_date)
    days_late = max((date.today() - due_date).days, 0) if due_date else 0
    fine_per_day = 5
    fine_amount = days_late * fine_per_day
    
    row_frame = tk.Frame(box, bg="#7B2CBF", padx=2, pady=2)
    row_frame.pack(fill="x", pady=(0, 15))
    
    row_content = tk.Frame(row_frame, bg=BG_CONTENT, padx=10, pady=10)
    row_content.pack(fill="x")
    
    tk.Label(row_content, text=book_title, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=25, anchor="w").grid(row=0, column=0)
    tk.Label(row_content, text=due_date.strftime("%b %d, %Y") if due_date else "—", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15).grid(row=0, column=1)
    tk.Label(row_content, text=f"{days_late} days", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=12).grid(row=0, column=2)
    tk.Label(row_content, text=f"₱{fine_amount:.2f}", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15).grid(row=0, column=3)
    
    total_frame = tk.Frame(box, bg="#FFF3D0", padx=15, pady=12, relief="solid", borderwidth=1)
    total_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(total_frame, text=f"TOTAL OUTSTANDING FINE: ₱{fine_amount:.2f}",
             font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w")

    def mark_returned():
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE borrow_records SET Status='Completed', Date_Returned=NOW() WHERE Record_ID=%s", (record_id,))
                conn.commit()
                messagebox.showinfo("Returned", "Marked as returned!")
                show_notifications()
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
            finally:
                conn.close()
    
    btn_frame = tk.Frame(box, bg=BG_CONTENT)
    btn_frame.pack(anchor="w")
    
    tk.Button(btn_frame, text="Mark All Returned", bg=BTN_GREEN, fg=TEXT_DARK, width=20, font=FONT,
              relief="solid", borderwidth=1, command=mark_returned).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Send Reminder", bg=BTN_YELLOW, fg="#000", width=20, font=FONT,
              relief="solid", borderwidth=1, command=lambda: messagebox.showinfo("Reminder", f"Reminder sent to {username}!")).grid(row=0, column=1, padx=5)

def show_notifications():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)

    header = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=10)
    header.pack(fill="x")
    tk.Label(header, text="NOTIFICATIONS", font=FONT_HEADING,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    tk.Button(header, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).pack(side="right")

    notifications_area = tk.Frame(frame, bg=BG_MAIN)
    notifications_area.pack(fill="both", expand=True, padx=25, pady=15)
    notifications_canvas = tk.Canvas(notifications_area, bg=BG_MAIN, highlightthickness=0)
    notifications_scrollbar = tk.Scrollbar(
        notifications_area, orient="vertical", command=notifications_canvas.yview
    )
    notifications_body = tk.Frame(notifications_canvas, bg=BG_MAIN)
    notifications_window = notifications_canvas.create_window(
        (0, 0), window=notifications_body, anchor="nw"
    )
    notifications_body.bind(
        "<Configure>",
        lambda event: notifications_canvas.configure(
            scrollregion=notifications_canvas.bbox("all")
        ),
    )
    notifications_canvas.bind(
        "<Configure>",
        lambda event: notifications_canvas.itemconfigure(
            notifications_window, width=event.width
        ),
    )
    notifications_canvas.configure(yscrollcommand=notifications_scrollbar.set)
    notifications_canvas.pack(side="left", fill="both", expand=True)
    notifications_scrollbar.pack(side="right", fill="y")
    
    # ========= PENDING BORROW REQUESTS =========
    pending_frame = tk.Frame(notifications_body, bg="#FFF3D0", padx=15, pady=15, relief="solid", borderwidth=1)
    pending_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(pending_frame, text="PENDING BORROW REQUESTS:", font=FONT_TITLE,
             bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    conn = get_db_connection()
    pending_requests = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT br.Record_ID AS id, u.Username, b.Book_Title AS Title,
                       br.Borrow_Date, br.Book_Review
                FROM borrow_records br
                JOIN User u ON br.User_ID = u.User_ID
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.Status = 'Pending'
                ORDER BY br.Borrow_Date DESC, br.Record_ID DESC
            """)
            pending_requests = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Notification Error", f"Could not load pending requests:\n{e}")
        finally:
            conn.close()
    
    if not pending_requests:
        tk.Label(pending_frame, text="No pending requests.", font=FONT, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w")
    else:
        for req in pending_requests:
            req_id = req['id']
            uname = req['Username']
            btitle = req['Title']
            requested_date = req.get("Borrow_Date")
            notes = req.get("Book_Review")
            
            req_row = tk.Frame(pending_frame, bg="#FFF3D0")
            req_row.pack(fill="x", pady=5)
            
            detail_text = f"{uname} requested \"{btitle}\""
            if requested_date:
                detail_text += f" on {str(requested_date)[:10]}"
            if notes:
                detail_text += f"\nNote: {notes}"
            tk.Label(req_row, text=detail_text, font=FONT,
                     bg="#FFF3D0", fg=TEXT_DARK, justify="left",
                     anchor="w", wraplength=650).pack(side="left", fill="x", expand=True)
            
            def approve_this(rid=req_id):
                c = get_db_connection()
                if c:
                    try:
                        cur = c.cursor()
                        cur.execute(
                            "UPDATE borrow_records SET Status='Reading' "
                            "WHERE Record_ID=%s AND Status='Pending'",
                            (rid,)
                        )
                        if cur.rowcount != 1:
                            c.rollback()
                            messagebox.showwarning(
                                "Request Updated",
                                "This request is no longer pending. The list will be refreshed."
                            )
                            show_notifications()
                            return
                        c.commit()
                        messagebox.showinfo("Approved", "Request approved!")
                        show_notifications()
                    except Exception as e:
                        messagebox.showerror("Error", f"Approve failed: {e}")
                    finally:
                        c.close()
            
            def reject_this(rid=req_id):
                c = get_db_connection()
                if c:
                    try:
                        cur = c.cursor()
                        cur.execute(
                            "UPDATE borrow_records SET Status='Dropped' "
                            "WHERE Record_ID=%s AND Status='Pending'",
                            (rid,)
                        )
                        if cur.rowcount != 1:
                            c.rollback()
                            messagebox.showwarning(
                                "Request Updated",
                                "This request is no longer pending. The list will be refreshed."
                            )
                            show_notifications()
                            return
                        c.commit()
                        messagebox.showinfo("Rejected", "Request rejected!")
                        show_notifications()
                    except Exception as e:
                        messagebox.showerror("Error", f"Reject failed: {e}")
                    finally:
                        c.close()
            
            tk.Button(req_row, text="APPROVE", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
                      relief="solid", borderwidth=1, command=approve_this).pack(side="right", padx=3)
            tk.Button(req_row, text="REJECT", bg=BTN_RED, fg="white", width=10, font=FONT,
                      relief="solid", borderwidth=1, command=reject_this).pack(side="right", padx=3)
    
    # ========= OVERDUE BOOKS =========
    overdue_frame = tk.Frame(notifications_body, bg="#FFF3D0", padx=15, pady=15, relief="solid", borderwidth=1)
    overdue_frame.pack(fill="x")
    
    tk.Label(overdue_frame, text="OVERDUE BOOKS:", font=FONT_TITLE,
             bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    overdue_items = []
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT br.Record_ID AS id, u.Username, b.Book_Title AS Title,
                       br.Date_Returned AS Due_Date
                FROM borrow_records br
                JOIN User u ON br.User_ID = u.User_ID
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.Status IN ('Reading', 'On Hold')
                  AND br.Date_Returned < %s
                  AND br.Date_Returned IS NOT NULL
            """, (datetime.now(),))
            overdue_items = cur.fetchall()
        except Exception as e:
            print(f"Overdue error: {e}")
        finally:
            conn.close()
    
    if not overdue_items:
        tk.Label(overdue_frame, text="No overdue books.", font=FONT, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w")
    else:
        for item in overdue_items:
            o_id = item['id']
            o_user = item['Username']
            o_book = item['Title']
            o_due = normalize_date(item['Due_Date'])
            days_late = (date.today() - o_due).days if o_due else 0
            
            item_row = tk.Frame(overdue_frame, bg="#FFF3D0")
            item_row.pack(fill="x", pady=5)
            
            tk.Label(item_row, text=f"• \"{o_book}\" — {days_late} day{'s' if days_late!=1 else ''} late ({o_user})", 
                     font=FONT, bg="#FFF3D0", fg=TEXT_DARK).pack(side="left")
            
            def view_detail(rid=o_id, usr=o_user, bk=o_book, due=o_due):
                show_overdue_detail(rid, usr, bk, due)
            
            tk.Button(item_row, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
                      relief="solid", borderwidth=1, command=view_detail).pack(side="right", padx=3)


# ==================================================
# ADD NEW USER — WITH HASHING & STRENGTH CHECK
# ==================================================
def show_add_user():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)

    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(side="right")
    
    form_container = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=30, relief="solid", borderwidth=1)
    form_container.place(relx=0.5, rely=0.45, anchor="center")

    tk.Label(form_container, text="ADD NEW USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

    entries = {}
    pass_shown = False
    confirm_shown = False

    # --- Username ---
    tk.Label(form_container, text="Username:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_user = tk.Entry(form_container, width=35, font=FONT)
    e_user.pack(pady=(0, 10))
    entries["Username"] = e_user

    # --- Email ---
    tk.Label(form_container, text="Email:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_email = tk.Entry(form_container, width=35, font=FONT)
    e_email.pack(pady=(0, 10))
    entries["Email"] = e_email

    # --- Password with SHOW/HIDE + STRENGTH ---
    tk.Label(form_container, text="Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    pass_frame = tk.Frame(form_container, bg=BG_CONTENT)
    pass_frame.pack(fill="x", pady=(0, 2))
    e_pass = tk.Entry(pass_frame, width=30, show="*", font=FONT)
    e_pass.pack(side="left")
    show_pass = tk.Button(pass_frame, text="👁️", bg=BG_CONTENT, fg=TEXT_DARK, 
                          relief="flat", width=3, command=lambda: toggle_password("pass"))
    show_pass.pack(side="right", padx=(5, 0))
    entries["Password"] = e_pass

    # Strength label
    strength_label = tk.Label(form_container, text="", font=("Arial", 10, "bold"),
                               bg=BG_CONTENT, anchor="w")
    strength_label.pack(fill="x", pady=(0, 10))

    def update_strength(*args):
        pw = e_pass.get()
        text, color = check_password_strength(pw)
        strength_label.config(text=f"Strength: {text}", fg=color)
    e_pass.bind("<KeyRelease>", update_strength)

    # --- Confirm Password with SHOW/HIDE ---
    tk.Label(form_container, text="Confirm Password:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    confirm_frame = tk.Frame(form_container, bg=BG_CONTENT)
    confirm_frame.pack(fill="x", pady=(0, 10))
    e_confirm = tk.Entry(confirm_frame, width=30, show="*", font=FONT)
    e_confirm.pack(side="left")
    show_confirm = tk.Button(confirm_frame, text="👁️", bg=BG_CONTENT, fg=TEXT_DARK, 
                              relief="flat", width=3, command=lambda: toggle_password("confirm"))
    show_confirm.pack(side="right", padx=(5, 0))
    entries["Confirm Password"] = e_confirm

    # --- Toggle Function ---
    def toggle_password(field):
        nonlocal pass_shown, confirm_shown
        if field == "pass":
            pass_shown = not pass_shown
            e_pass.config(show="" if pass_shown else "*")
            show_pass.config(text="🙈" if pass_shown else "👁️")
        elif field == "confirm":
            confirm_shown = not confirm_shown
            e_confirm.config(show="" if confirm_shown else "*")
            show_confirm.config(text="🙈" if confirm_shown else "👁️")

    # --- Role Dropdown ---
    tk.Label(form_container, text="Role:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    role_drop = ttk.Combobox(form_container, values=["User", "Admin"],
                              state="readonly", width=32, font=FONT)
    role_drop.set("User")
    role_drop.pack(pady=(0, 10))

    # --- Security Question ---
    tk.Label(form_container, text='"What is your favorite book?"', font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_security = tk.Entry(form_container, width=35, font=FONT)
    e_security.pack(pady=(0, 20))
    entries["Security Answer"] = e_security

    # --- CREATE ACCOUNT ---
    def create_account():
        username = e_user.get().strip()
        email = e_email.get().strip()
        password = e_pass.get()
        confirm = e_confirm.get()
        role = role_drop.get()
        answer = e_security.get().strip()

        if not username:
            messagebox.showwarning("Warning", "Username is required!")
            return
        
        if email:
            import Main
            valid_email, email_msg = Main.validate_email(email)
            if not valid_email:
                messagebox.showerror("Invalid Email", email_msg)
                return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Use Main's password validation (same rules everywhere)
        import Main
        is_valid, msg = Main.validate_password(password)
        if not is_valid:
            messagebox.showerror("Invalid Password", msg)
            return
        
        if not answer:
            messagebox.showwarning("Warning", "Security answer is required!")
            return

        # Hash password — ONE correct way
        hashed_pw = hash_password(password)

        conn = get_db_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO User (Username, Email, Password, Security_Question, Security_Answer, User_Role, Status)
                VALUES (%s, %s, %s, 'What is your favorite book?', %s, %s, 'Offline')
            """, (username, email if email else None, hashed_pw, answer, role))
            conn.commit()
            
            messagebox.showinfo("Success", 
                f"User '{username}' created!\nPassword hashed and stored securely.")
            show_admin_dashboard()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user:\n{e}")
        finally:
            conn.close()

    btn_frame = tk.Frame(form_container, bg=BG_CONTENT)
    btn_frame.pack(fill="x")

    tk.Button(btn_frame, text="CREATE ACCOUNT", bg=BTN_GREEN, fg=TEXT_DARK, width=20, font=FONT,
              relief="solid", borderwidth=1, command=create_account).pack(side="left", padx=5)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(side="left", padx=5)

# ==================================================
# VIEW ALL USERS
# ==================================================
def show_all_users():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)

    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_admin_dashboard).place(x=1325, y=15)

    box = tk.Frame(frame, bg="#FFF3D0", padx=30, pady=25, relief="solid", borderwidth=2)
    box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(box, text="VIEW ALL USERS", font=FONT_TITLE, bg="#FFF3D0", fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))

    # SCROLLABLE
    table_wrapper = tk.Frame(box, bg="#FFF3D0")
    table_wrapper.pack(fill="both", expand=True)

    canvas = tk.Canvas(table_wrapper, bg="#FFF3D0", highlightthickness=0, width=650, height=400)
    scrollbar = tk.Scrollbar(table_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#FFF3D0")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=630)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header
    header = tk.Frame(scrollable_frame, bg="#FFF3D0")
    header.pack(fill="x")

    tk.Label(header, text="USERNAME", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=18, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=0)
    tk.Label(header, text="ROLE", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=12, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=1)
    tk.Label(header, text="JOINED DATE", font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
             width=22, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=2)

    tk.Frame(scrollable_frame, bg="#000", height=1).pack(fill="x", pady=2)

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
        tk.Label(scrollable_frame, text="No users found.", font=FONT, bg="#FFF3D0", fg=TEXT_DARK, pady=15).pack()
        return

    for username, role, date in users:
        row = tk.Frame(scrollable_frame, bg="#FFF3D0")
        row.pack(fill="x")

        if date:
            month = date.strftime("%b")
            day = date.day
            year = date.year
            date_str = f"Joined {month} {day}, {year}"
        else:
            date_str = "—"

        tk.Label(row, text=username, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=18, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=0)
        tk.Label(row, text=role, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=12, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=1)
        tk.Label(row, text=date_str, font=FONT, bg="#FFF3D0", fg=TEXT_DARK,
                 width=22, relief="solid", borderwidth=1, padx=10, pady=5).grid(row=0, column=2)

# ==================================================
# VIEW USER DETAIL
# ==================================================
def show_user_detail(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1325, y=15)
    
    outer_box = tk.Frame(frame, bg="#7B2CBF", padx=3, pady=3)
    outer_box.place(relx=0.5, rely=0.5, anchor="center")
    
    box = tk.Frame(outer_box, bg=BG_CONTENT, padx=40, pady=30)
    box.pack()
    
    tk.Label(box, text="VIEW USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    profile_frame = tk.Frame(box, bg="#e5d9b6", width=100, height=100, relief="solid", borderwidth=1)
    profile_frame.pack(anchor="w", pady=(0, 20))
    profile_frame.pack_propagate(False)
    profile_label = tk.Label(
        profile_frame, text="PROFILE\nPICTURE", font=("Arial", 9, "bold"),
        bg="#e5d9b6", fg=TEXT_DARK, justify="center",
    )
    profile_label.pack(fill="both", expand=True)
    
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT User_ID, Username, Email, User_Role, Profile_Picture "
            "FROM User WHERE Username=%s",
            (username,),
        )
        user = cur.fetchone()
        if user:
            uid, uname, email, role, profile_picture = user
            display_user_picture(profile_label, profile_picture)
            
            def make_display_field(label, value):
                tk.Label(box, text=f"{label}:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
                display_val = value or "Not provided"
                tk.Label(box, text=display_val, font=FONT, bg="#e5d9b6", relief="solid", borderwidth=1,
                         width=35, anchor="w", padx=8, pady=5).pack(pady=(0, 10))
            
            make_display_field("ID", str(uid))
            make_display_field("Username", uname)
            make_display_field("Email", email[:3] + "***" if email else "Not provided")
            make_display_field("Role", role.upper() if role else "USER")
        else:
            tk.Label(box, text="User not found.", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load user:\n{e}")
    finally:
        conn.close()

# ==================================================
# EDIT USER — WITH HASHING + STRENGTH CHECK
# ==================================================
def show_edit_user(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1325, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="EDIT USER", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    conn = get_db_connection()
    if not conn: return
    user_data = None
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT User_ID, Username, Email, User_Role, Profile_Picture "
            "FROM User WHERE Username=%s",
            (username,),
        )
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
    
    uid, uname, email, role, current_picture_path = user_data
    entries = {}
    pass_shown = False
    picture_state = {"selected_path": None, "remove": False}

    profile_frame = tk.Frame(box, bg="#e5d9b6", width=100, height=100, relief="solid", borderwidth=1)
    profile_frame.pack(anchor="w", pady=(0, 5))
    profile_frame.pack_propagate(False)
    profile_label = tk.Label(
        profile_frame, text="PROFILE\nPICTURE", font=("Arial", 9, "bold"),
        bg="#e5d9b6", fg=TEXT_DARK, justify="center",
    )
    profile_label.pack(fill="both", expand=True)

    picture_buttons = tk.Frame(box, bg=BG_CONTENT)
    picture_buttons.pack(anchor="w", pady=(0, 15))

    def refresh_profile_preview():
        path = picture_state["selected_path"]
        if path is None and not picture_state["remove"]:
            path = current_picture_path
        display_user_picture(profile_label, path)

    def upload_profile_picture():
        path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")],
        )
        if not path:
            return

        extension = os.path.splitext(path)[1].lower()
        if extension not in (".png", ".jpg", ".jpeg"):
            messagebox.showerror("Invalid Image", "Choose a PNG or JPEG image.")
            return
        try:
            with Image.open(path) as image:
                image.verify()
        except (OSError, ValueError) as err:
            messagebox.showerror("Invalid Image", f"Could not read the selected image:\n{err}")
            return

        picture_state["selected_path"] = path
        picture_state["remove"] = False
        refresh_profile_preview()

    def remove_profile_picture():
        picture_state["selected_path"] = None
        picture_state["remove"] = True
        refresh_profile_preview()

    tk.Button(
        picture_buttons, text="UPLOAD", bg=BTN_GREEN, fg=TEXT_DARK,
        width=10, font=FONT, relief="solid", borderwidth=1,
        command=upload_profile_picture,
    ).pack(side="left", padx=(0, 5))
    tk.Button(
        picture_buttons, text="REMOVE", bg=BTN_RED, fg="white",
        width=10, font=FONT, relief="solid", borderwidth=1,
        command=remove_profile_picture,
    ).pack(side="left")
    refresh_profile_preview()

    def make_edit_field(label, value):
        tk.Label(box, text=f"{label}:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
        e = tk.Entry(box, width=35, font=FONT)
        e.insert(0, value or "")
        e.pack(pady=(0, 10))
        entries[label] = e

    make_edit_field("Username", uname)
    make_edit_field("Email", email or "")

    # --- Password with SHOW/HIDE + STRENGTH ---
    tk.Label(box, text="New Password (leave blank to keep current):", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    pass_frame = tk.Frame(box, bg=BG_CONTENT)
    pass_frame.pack(fill="x", pady=(0, 2))
    e_pass = tk.Entry(pass_frame, width=30, show="*", font=FONT)
    e_pass.pack(side="left")
    show_pass = tk.Button(pass_frame, text="👁️", bg=BG_CONTENT, fg=TEXT_DARK, 
                          relief="flat", width=3, command=lambda: toggle_edit_pass())
    show_pass.pack(side="right", padx=(5, 0))
    entries["Password"] = e_pass

    edit_strength_label = tk.Label(box, text="", font=("Arial", 10, "bold"),
                                     bg=BG_CONTENT, anchor="w")
    edit_strength_label.pack(fill="x", pady=(0, 10))

    def update_edit_strength(*args):
        pw = e_pass.get()
        if pw:
            text, color = check_password_strength(pw)
            edit_strength_label.config(text=f"Strength: {text}", fg=color)
        else:
            edit_strength_label.config(text="Will keep current password", fg="#666")
    
    e_pass.bind("<KeyRelease>", update_edit_strength)
    update_edit_strength()

    def toggle_edit_pass():
        nonlocal pass_shown
        pass_shown = not pass_shown
        e_pass.config(show="" if pass_shown else "*")
        show_pass.config(text="🙈" if pass_shown else "👁️")

    # --- Role Dropdown ---
    tk.Label(box, text="Role:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(fill="x")
    
    role_drop = ttk.Combobox(box, values=["User", "Admin"],
                              state="readonly", width=32, font=FONT)
    role_drop.set(role or "User")
    role_drop.pack(pady=(0, 10))

    def save_changes():
        new_user = entries["Username"].get().strip()
        new_email = entries["Email"].get().strip()
        new_password = entries["Password"].get()
        new_role = role_drop.get()
        new_picture_path = current_picture_path
        installed_picture_path = None
        
        if not new_user:
            messagebox.showwarning("Warning", "Username cannot be empty!")
            return

        if new_email:
            valid_email, email_msg = Main.validate_email(new_email)
            if not valid_email:
                messagebox.showerror("Invalid Email", email_msg)
                return

        hashed_pw = None
        if new_password:
            valid_password, password_msg = Main.validate_password(new_password)
            if not valid_password:
                messagebox.showwarning("Invalid Password", password_msg)
                return
            hashed_pw = hash_password(new_password)

        conn = get_db_connection()
        if not conn: return
        database_committed = False
        try:
            cur = conn.cursor()

            if picture_state["remove"]:
                new_picture_path = None
            elif picture_state["selected_path"]:
                extension = os.path.splitext(picture_state["selected_path"])[1].lower()
                os.makedirs(PROFILE_PICTURE_DIR, exist_ok=True)
                new_picture_path = os.path.join(
                    PROFILE_PICTURE_DIR, f"user_{uid}_{uuid.uuid4().hex}{extension}"
                )
                installed_picture_path = new_picture_path
                shutil.copyfile(picture_state["selected_path"], new_picture_path)
            
            if new_password:
                cur.execute("""
                    UPDATE User
                    SET Username=%s, Email=%s, Password=%s, User_Role=%s,
                        Profile_Picture=%s
                    WHERE User_ID=%s
                    """, (new_user, new_email if new_email else None, hashed_pw,
                          new_role, new_picture_path, uid))
                msg = "User updated!\nPassword changed and secured."
            else:
                cur.execute("""
                    UPDATE User
                    SET Username=%s, Email=%s, User_Role=%s, Profile_Picture=%s
                    WHERE User_ID=%s
                    """, (new_user, new_email if new_email else None, new_role,
                          new_picture_path, uid))
                msg = "User updated!\nPassword unchanged."
            
            conn.commit()
            database_committed = True
            if picture_state["remove"] or picture_state["selected_path"]:
                remove_managed_profile_picture(current_picture_path)
            messagebox.showinfo("Success", msg)
            show_admin_dashboard()
        except Exception as e:
            if not database_committed and installed_picture_path and os.path.isfile(installed_picture_path):
                try:
                    os.remove(installed_picture_path)
                except OSError as cleanup_error:
                    messagebox.showwarning(
                        "Picture Cleanup",
                        f"Could not clean up the new profile picture:\n{cleanup_error}",
                    )
            messagebox.showerror("Error", f"Update failed!\n{e}")
        finally:
            conn.close()
    
    tk.Button(box, text="SAVE CHANGES", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=save_changes).pack(pady=10)
    tk.Button(box, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_admin_dashboard).pack(pady=5)

# ==================================================
# DELETE USER CONFIRM
# ==================================================
def show_delete_confirm(username):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_admin_dashboard).place(x=1325, y=15)
    
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
# READING RECORDS & ACCOUNT
# ==================================================
def open_reading_records():
    import Main
    role = Main.current_user.get("role", "")
    is_admin = (role == "Admin")
    
    if not is_admin:
        messagebox.showwarning(
            "Access Denied",
            "Only Admin can access Reading Records!\n\n"
            f"Current User: {Main.current_user.get('username', 'Unknown')}\n"
            f"Role: {role or 'Not set'}"
        )
        return

    
    import sys, os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        import AdminBorrow
        AdminBorrow.show_admin_borrow_screen()
    except ModuleNotFoundError as e:
        messagebox.showerror("File Missing", f"Cannot find AdminBorrow.py!\n\nError: {e}")

def show_admin_collection_screen():
    import Collection
    Collection.show_admin_collection_screen()

# ==================================================
# MAIN ADMIN DASHBOARD
# ==================================================
def show_admin_dashboard():
    clear_all()
    root.configure(bg=BG_MAIN)

    outer_content = tk.Frame(root, bg=BG_MAIN)
    outer_content.pack(fill="both", expand=True)

    # HEADER
    top_header = tk.Frame(outer_content, bg=BG_CONTENT, height=60)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)

    tk.Label(top_header, text="WELCOME — ADMIN",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)

    tk.Button(top_header, text="🔔", font=("Arial", 16), bg=BG_CONTENT, fg=TEXT_DARK,
              relief="flat", command=show_notifications).pack(side="right", padx=20)

    # SIDEBAR 
    sidebar = tk.Frame(outer_content, bg=BG_SIDEBAR, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    def open_books():
        import sys, os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        try:
            import books
            books.show_books_screen()
        except ModuleNotFoundError:
            messagebox.showerror("Error", "books.py not found!\nCheck filename and folder.")

    def open_authors():
        import sys, os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        try:
            import Authors
            Authors.show_authors_screen()
        except ModuleNotFoundError:
            messagebox.showerror("Error", "Authors.py not found!\nCheck filename and folder.")

    def open_categories():
        import sys, os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        try:
            import Category
            Category.show_categories_screen()
        except ModuleNotFoundError:
            messagebox.showerror("Error", "Category.py not found!\nCheck file exists and same folder.")

    nav_items = [
        ("Home", show_admin_dashboard),
        ("Navigations", show_navigation_dashboard),
        ("Books", open_books),
        ("Authors", open_authors),
        ("Categories", open_categories),
        ("Reading Records", open_reading_records),
        ("My Collection", show_admin_collection_screen),
        ("Account", show_account_screen),
        ("Settings", Main.open_settings),
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
              command=lambda: [set_user_status("Offline"), back_to_login()]).pack(pady=5, side="bottom")

    # ========= MAIN CONTENT AREA =========
    content = tk.Frame(outer_content, bg=BG_MAIN)
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
        finally: conn.close()

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
        
        if title == "Categories":
            card.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: open_categories())
        elif title == "Books":
            card.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: open_books())
        elif title == "Authors":
            card.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: open_authors())
        elif title == "Records":
            card.config(cursor="hand2")
            card.bind("<Button-1>", lambda e: open_reading_records())

        tk.Label(card, text=title, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
        tk.Label(card, text=f"[{count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=5)

    tk.Label(content, text="USERS MANAGEMENT", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 5), padx=20)

    # Users Table — SCROLLABLE
    table_wrapper = tk.Frame(content, bg=BG_CONTENT, relief="solid", borderwidth=1)
    table_wrapper.pack(padx=20, fill="both", expand=True)

    canvas = tk.Canvas(table_wrapper, bg=BG_CONTENT, highlightthickness=0)
    scrollbar = tk.Scrollbar(table_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_CONTENT)

    def sync_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", sync_scroll_region)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def sync_width(event):
        canvas.itemconfig(canvas.find_all()[0], width=event.width)
    canvas.bind("<Configure>", sync_width)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header
    hdr = tk.Frame(scrollable_frame, bg=BG_CONTENT)
    hdr.pack(fill="x", pady=5, padx=15)
    tk.Label(hdr, text="ID", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=6, anchor="w").grid(row=0, column=0)
    tk.Label(hdr, text="USERNAME", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=15, anchor="w").grid(row=0, column=1)
    tk.Label(hdr, text="ROLE", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=12, anchor="w").grid(row=0, column=2)
    tk.Label(hdr, text="ACTIONS", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK, width=25, anchor="center").grid(row=0, column=3)

    tk.Frame(scrollable_frame, bg="#e5cd90", height=1).pack(fill="x", pady=5, padx=15)

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT User_ID, Username, User_Role FROM User ORDER BY User_ID")
            users = cur.fetchall()
            
            if not users:
                tk.Label(scrollable_frame, text="No users found.", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=10)
            else:
                for uid, uname, role in users:
                    row = tk.Frame(scrollable_frame, bg=BG_CONTENT)
                    row.pack(fill="x", pady=3, padx=15)
                    tk.Label(row, text=str(uid), font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=6, anchor="w").grid(row=0, column=0)
                    tk.Label(row, text=uname, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=15, anchor="w").grid(row=0, column=1)
                    tk.Label(row, text=role, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, width=12, anchor="w").grid(row=0, column=2)
                    
                    act = tk.Frame(row, bg=BG_CONTENT)
                    act.grid(row=0, column=3)
                    tk.Button(act, text="VIEW", bg=BTN_YELLOW, fg="#000", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1, command=lambda u=uname: show_user_detail(u)).grid(row=0, column=0, padx=2)
                    tk.Button(act, text="EDIT", bg=BTN_BROWN, fg="white", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1, command=lambda u=uname: show_edit_user(u)).grid(row=0, column=1, padx=2)
                    tk.Button(act, text="DELETE", bg=BTN_RED, fg="white", width=7, font=("Arial", 10, "bold"),
                              relief="solid", borderwidth=1, command=lambda u=uname: show_delete_confirm(u)).grid(row=0, column=2, padx=2)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load users:\n{e}")
        finally: conn.close()

    tk.Label(content, text="QUICK ACTIONS", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(20, 5), padx=20)

    qa_frame = tk.Frame(content, bg=BG_MAIN)
    qa_frame.pack(anchor="w", padx=20, pady=(0, 30))
    tk.Button(qa_frame, text="+ ADD NEW USER", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=show_add_user).grid(row=0, column=0, padx=5)
    tk.Button(qa_frame, text="VIEW ALL USERS", bg=BTN_BROWN, fg="white", width=18, font=FONT,
              relief="solid", borderwidth=1, command=show_all_users).grid(row=0, column=1, padx=5)

def show_account_screen():
    clear_all()
    try:
        import Account
        Account.show_account_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open Account:\n{e}")
