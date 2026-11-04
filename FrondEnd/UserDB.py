import tkinter as tk
from tkinter import messagebox
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
# USER DASHBOARD
# ==================================================
def show_approved_request_detail(record_id, book_title, date_started, date_due):
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)

    tk.Button(frame, text="Back To Notifications", bg=BTN_BROWN, fg="white", width=18,
              command=show_notifications).place(x=1030, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="APPROVED REQUEST DETAILS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 25))
    
    tk.Label(box, text="Book Title:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text=book_title, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    tk.Label(box, text="Status:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    status_frame = tk.Frame(box, bg=BTN_YELLOW, padx=10, pady=3)
    status_frame.pack(anchor="w", pady=(0, 15))
    tk.Label(status_frame, text="Currently Reading", font=FONT, bg=BTN_YELLOW, fg="#000").pack()
    
    tk.Label(box, text="Started:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    start_display = date_started.strftime("%Y   %m   %d") if date_started else "—"
    tk.Label(box, text=start_display, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    tk.Label(box, text="Due Date:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    due_display = date_due.strftime("%Y   %m   %d") if date_due else "—"
    tk.Label(box, text=due_display, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    tk.Label(box, text="WHERE TO FIND:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 5))
    tk.Label(box, text="Reading Status & Records → " + book_title, font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text="You can now update your reading progress there!", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    tk.Button(box, text="Go To Record", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=show_reading_records).pack(anchor="w")

def show_notifications():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)

    header = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=10)
    header.pack(fill="x")
    tk.Label(header, text="NOTIFICATIONS", font=FONT_HEADING,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    tk.Button(header, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).pack(side="right")

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

    my_user_id = current_user.get("user_id")
    if not my_user_id:
        messagebox.showwarning("Sign In Required", "Please sign in to view notifications.")
        Main.show_login()
        return

    # ========= PENDING REQUESTS =========
    pending_frame = tk.Frame(notifications_body, bg="#fff3cd", padx=15, pady=15, relief="solid", borderwidth=1)
    pending_frame.pack(fill="x", pady=(0, 10))
    tk.Label(pending_frame, text="WAITING FOR ADMIN APPROVAL:",
             font=FONT_TITLE, bg="#fff3cd", fg="#856404").pack(anchor="w")

    conn = get_db_connection()
    pending_list = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT b.Book_Title, br.Borrow_Date
                FROM borrow_records br
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.User_ID = %s AND br.Status = 'Pending'
                ORDER BY br.Borrow_Date DESC, br.Record_ID DESC
            """, (my_user_id,))
            pending_list = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Notification Error", f"Could not load pending requests:\n{e}")
        finally:
            conn.close()

    if not pending_list:
        tk.Label(pending_frame, text="No requests waiting for approval.",
                 font=FONT, bg="#fff3cd", fg=TEXT_DARK).pack(anchor="w", pady=(5, 0))
    else:
        for item in pending_list:
            requested_date = item["Borrow_Date"]
            date_text = str(requested_date)[:10] if requested_date else "date not set"
            tk.Label(
                pending_frame,
                text=f"\"{item['Book_Title']}\" — Waiting for admin approval (requested {date_text})",
                font=FONT, bg="#fff3cd", fg=TEXT_DARK, anchor="w", wraplength=950,
            ).pack(anchor="w", pady=3)
    
    # ========= APPROVED REQUESTS =========
    approved_frame = tk.Frame(notifications_body, bg="#d4edda", padx=15, pady=15, relief="solid", borderwidth=1)
    approved_frame.pack(fill="x", pady=(0, 10))
    tk.Label(approved_frame, text="APPROVED:", font=FONT_TITLE, bg="#d4edda", fg="#155724").pack(anchor="w")
    
    conn = get_db_connection()
    approved_list = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT br.Record_ID, b.Book_Title, br.Borrow_Date, br.Date_Returned
                FROM borrow_records br
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.User_ID = %s AND br.Status = 'Reading'
                ORDER BY br.Borrow_Date DESC
            """, (my_user_id,))
            approved_list = cur.fetchall()
        except Exception as e:
            print(f"Approved error: {e}")
        finally:
            conn.close()
    
    if not approved_list:
        tk.Label(approved_frame, text="No approved requests yet.", font=FONT, bg="#d4edda", fg=TEXT_DARK).pack(anchor="w")
    else:
        for item in approved_list:
            aid = item['Record_ID']
            atitle = item['Book_Title']
            astart = item['Borrow_Date']
            adue = item['Date_Returned']
            
            row = tk.Frame(approved_frame, bg="#d4edda")
            row.pack(fill="x", pady=5)
            
            start_str = astart.strftime("%b %d") if astart else "—"
            due_str = adue.strftime("%b %d") if adue else "—"
            
            tk.Label(row, text=f"Your request for \"{atitle}\" — APPROVED!", 
                     font=FONT, bg="#d4edda", fg=TEXT_DARK).pack(anchor="w")
            tk.Label(row, text=f"Start: {start_str}   |   Due: {due_str}", 
                     font=FONT, bg="#d4edda", fg=TEXT_DARK).pack(anchor="w")
            
            def view_approved(rid=aid, bk=atitle, st=astart, du=adue):
                show_approved_request_detail(rid, bk, st, du)
            
            tk.Button(row, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
                      relief="solid", borderwidth=1, command=view_approved).pack(anchor="e")
    
    # ========= REJECTED REQUESTS =========
    rejected_frame = tk.Frame(notifications_body, bg="#f8d7da", padx=15, pady=15, relief="solid", borderwidth=1)
    rejected_frame.pack(fill="x", pady=(0, 10))
    tk.Label(rejected_frame, text="REJECTED / CANCELLED:", font=FONT_TITLE, bg="#f8d7da", fg="#721c24").pack(anchor="w")
    
    conn = get_db_connection()
    rejected_list = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT br.Record_ID, b.Book_Title
                FROM borrow_records br
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.User_ID = %s AND br.Status = 'Dropped'
                ORDER BY br.Record_ID DESC LIMIT 5
            """, (my_user_id,))

            rejected_list = cur.fetchall()
        except Exception as e:
            print(f"Rejected error: {e}")
        finally:
            conn.close()
    
    if not rejected_list:
        tk.Label(rejected_frame, text="No rejected requests.", font=FONT, bg="#f8d7da", fg=TEXT_DARK).pack(anchor="w")
    else:
        for item in rejected_list:
            tk.Label(rejected_frame, text=f"• \"{item['Book_Title']}\" — Not Available / Cancelled",
                     font=FONT, bg="#f8d7da", fg=TEXT_DARK).pack(anchor="w", pady=3)
    
    # ========= UPCOMING / DUE SOON =========
    upcoming_frame = tk.Frame(notifications_body, bg="#fff3cd", padx=15, pady=15, relief="solid", borderwidth=1)
    upcoming_frame.pack(fill="x")
    tk.Label(upcoming_frame, text="COMING UP / DUE SOON:", font=FONT_TITLE, bg="#fff3cd", fg="#856404").pack(anchor="w")
    
    from datetime import datetime, timedelta
    conn = get_db_connection()
    due_list = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT b.Book_Title AS Book_Title, br.Date_Returned AS Due_Date
                FROM borrow_records br
                JOIN Books b ON br.Book_ID = b.Book_ID
                WHERE br.User_ID = %s AND br.Status = 'Reading' AND br.Date_Returned IS NOT NULL
                ORDER BY br.Date_Returned ASC LIMIT 3
            """, (my_user_id,))

            due_list = cur.fetchall()
        except Exception as e:
            print(f"Due error: {e}")
        finally:
            conn.close()
    
    if not due_list:
        tk.Label(upcoming_frame, text="No upcoming due dates.", font=FONT, bg="#fff3cd", fg=TEXT_DARK).pack(anchor="w")
    else:
        for item in due_list:
            due_date = item['Due_Date']
            if isinstance(due_date, datetime):
                due_date = due_date.date()
            days_left = (due_date - datetime.now().date()).days
            if days_left < 0:
                label = f"⚠️ OVERDUE: \"{item['Book_Title']}\" — {-days_left} day(s) late!"
            elif days_left == 0:
                label = f"⚠️ DUE TODAY: \"{item['Book_Title']}\""
            else:
                label = f"\"{item['Book_Title']}\" — Due in {days_left} day(s)"

            tk.Label(upcoming_frame, text=label, font=FONT, bg="#fff3cd", fg=TEXT_DARK).pack(anchor="w", pady=3)


def show_books():
    clear_all()
    try:
        import user_books
        user_books.show_user_books_screen()
    except ModuleNotFoundError:
        messagebox.showerror("Error", "user_books.py not found!\nCheck filename and folder.")

def show_authors():
    clear_all()
    try:
        import user_Authors
        user_Authors.show_user_authors_screen()
    except ModuleNotFoundError:
        messagebox.showerror("Error", "user_Authors.py not found!\nCheck filename and folder.")

def show_categories():
    clear_all()
    try:
        import user_Category
        user_Category.show_user_categories_screen()
    except ModuleNotFoundError:
        messagebox.showerror("Error", "user_Category.py not found!\nCheck filename and folder.")

def show_reading_records():
    clear_all()
    try:
        import UserBorrow
        UserBorrow.show_user_borrow_screen()
    except ModuleNotFoundError:
        messagebox.showerror("Error", "UserBorrow.py not found!\nCheck filename and folder.")

def show_my_collection():
    clear_all()
    try:
        import user_Collection
        user_Collection.show_user_collection_screen()
    except ModuleNotFoundError:
        messagebox.showerror("Error", "user_Collection.py not found!\nCheck filename and folder.")

def show_account():
    clear_all()
    try:
        import Account
        Account.show_account_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open Account:\n{e}")

def show_settings():
    Main.open_settings()

# ==================================================
# MAIN USER DASHBOARD
# ==================================================
def show_user_dashboard():
    clear_all()
    root.configure(bg=BG_MAIN)
    
    username = Main.current_user.get("username") or "User"
    display_name = username.upper() if username != "User" else "USER"
    
    # ========= TOP HEADER =========
    top_header = tk.Frame(root, bg=BG_CONTENT, height=60, relief="solid", borderwidth=1)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)
    
    tk.Label(top_header, text=f"WELCOME — {display_name}",
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)

    tk.Button(top_header, text="🔔", font=("Arial", 16), bg=BG_CONTENT, fg=TEXT_DARK,
              relief="flat", command=show_notifications).pack(side="right", padx=20)
    
    # ========= SIDEBAR =========
    sidebar = tk.Frame(root, bg=BG_SIDEBAR, width=200, relief="solid", borderwidth=1)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    nav_items = [
        ("Home", show_user_dashboard),
        ("Navigations", show_navigation_dashboard),
        ("Books", show_books),
        ("Authors", show_authors),
        ("Categories", show_categories),
        ("Reading Records", show_reading_records),
        ("My Collection", show_my_collection),
        ("Account", show_account),
        ("Settings", show_settings),
    ]
    
    for name, cmd in nav_items:
        is_home = (name == "Home")
        btn_bg = "#6b3a10" if is_home else BG_SIDEBAR
        tk.Button(sidebar, text=name, font=FONT, bg=btn_bg, fg=TEXT_LIGHT,
                  relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
                  command=cmd).pack(pady=1)
    
    tk.Frame(sidebar, bg="#6b3a10", height=2).pack(fill="x", pady=10)
    
    tk.Button(sidebar, text="Logout", font=FONT, bg=BTN_RED, fg="white",
              relief="flat", cursor="hand2", width=22, anchor="w", padx=10,
              command=lambda: [Main.set_user_status("Offline"), back_to_login()]).pack(pady=5, side="bottom")

    # ========= MAIN CONTENT =========
    content = tk.Frame(root, bg=BG_MAIN)
    content.pack(side="right", fill="both", expand=True)
    
    conn = get_db_connection()
    book_count = author_count = cat_count = rec_count = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Books"); book_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Authors"); author_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Categories"); cat_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM borrow_records"); rec_count = cur.fetchone()[0]
        except Exception as e:
            print(f"Stats error: {e}")
        finally:
            conn.close()
    
    stats_row = tk.Frame(content, bg=BG_MAIN)
    stats_row.pack(pady=25, padx=20, anchor="w")
    
    card_style = {"bg": BG_CONTENT, "padx": 30, "pady": 20, "relief": "solid", "borderwidth": 1}
    
    books_card = tk.Frame(stats_row, **card_style)
    books_card.pack(side="left", padx=5)
    tk.Label(books_card, text="Books", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(books_card, text=f"[{book_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    authors_card = tk.Frame(stats_row, **card_style)
    authors_card.pack(side="left", padx=5)
    tk.Label(authors_card, text="Authors", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(authors_card, text=f"[{author_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    cat_card = tk.Frame(stats_row, **card_style)
    cat_card.pack(side="left", padx=5)
    tk.Label(cat_card, text="Categories", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(cat_card, text=f"[{cat_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    rec_card = tk.Frame(stats_row, **card_style)
    rec_card.pack(side="left", padx=5)
    tk.Label(rec_card, text="Records", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(rec_card, text=f"[{rec_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    search_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=12, relief="solid", borderwidth=1)
    search_frame.pack(pady=5, padx=20, fill="x")
    
    tk.Label(search_frame, text="Quick Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=50, font=FONT)
    search_entry.pack(side="left")
    
    activity_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=15, relief="solid", borderwidth=1)
    activity_frame.pack(pady=15, padx=20, fill="both", expand=True)
    
    tk.Label(activity_frame, text="RECENT ACTIVITY / OVERVIEW", font=FONT_TITLE, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    header_row = tk.Frame(activity_frame, bg=BG_CONTENT)
    header_row.pack(fill="x", pady=5)
    tk.Label(header_row, text="Title — Author — Status — Date Added", font=FONT, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    
    tk.Frame(activity_frame, bg="#d4b86a", height=1).pack(fill="x", pady=8)