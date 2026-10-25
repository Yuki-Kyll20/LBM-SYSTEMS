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
# USER DASHBOARD — Screens
# ==================================================

def show_approved_request_detail():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # Back button — top right
    tk.Button(frame, text="Back To Notifications", bg=BTN_BROWN, fg="white", width=18,
              command=show_notifications).place(x=1030, y=15)
    
    # Main box
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="APPROVED REQUEST DETAILS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 25))
    
    # Book Title
    tk.Label(box, text="Book Title:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text="Oshi Mayncrap", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    # Status
    tk.Label(box, text="Status:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    status_frame = tk.Frame(box, bg=BTN_YELLOW, padx=10, pady=3)
    status_frame.pack(anchor="w", pady=(0, 15))
    tk.Label(status_frame, text="Currently Reading", font=FONT, bg=BTN_YELLOW, fg="#000").pack()
    
    # Started
    tk.Label(box, text="Started:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text="2026    12    11", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    # Due Date
    tk.Label(box, text="Due Date:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text="2026    26    11", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    # Where to Find
    tk.Label(box, text="WHERE TO FIND:", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 5))
    tk.Label(box, text="Reading Status & Records - \"Oshi Mayncrap\"", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(box, text="You can now update your progress here!", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    # Go To Record button
    tk.Button(box, text="Go To Record", bg=BTN_GREEN, fg=TEXT_DARK, width=18, font=FONT,
              relief="solid", borderwidth=1, command=lambda: messagebox.showinfo("Go To Record", "Redirecting to Reading Records...")).pack(anchor="w")

def show_notifications():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    
    box = tk.Frame(frame, bg=BG_CONTENT, padx=40, pady=30, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(box, text="NOTIFICATIONS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    # --- APPROVED ---
    approved_frame = tk.Frame(box, bg="#d4edda", padx=15, pady=15, relief="solid", borderwidth=1)
    approved_frame.pack(fill="x", pady=(0, 10))
    
    tk.Label(approved_frame, text="APPROVED:", font=FONT_TITLE, bg="#d4edda", fg="#155724").pack(anchor="w")
    tk.Label(approved_frame, text="Your request for \"Oshi Mayncrap\" - APPROVED!", 
             font=FONT, bg="#d4edda", fg=TEXT_DARK).pack(anchor="w")
    tk.Label(approved_frame, text="Start: Nov 12   |   Due: Nov 26", 
             font=FONT, bg="#d4edda", fg=TEXT_DARK).pack(anchor="w", pady=(0, 5))
    
    tk.Button(approved_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_approved_request_detail).pack(anchor="e")
    
    # --- REJECTED ---
    rejected_frame = tk.Frame(box, bg="#f8d7da", padx=15, pady=15, relief="solid", borderwidth=1)
    rejected_frame.pack(fill="x", pady=(0, 10))
    
    tk.Label(rejected_frame, text="REJECTED:", font=FONT_TITLE, bg="#f8d7da", fg="#721c24").pack(anchor="w")
    tk.Label(rejected_frame, text="Your request for \"Earth 616\" → Not Available", 
             font=FONT, bg="#f8d7da", fg=TEXT_DARK).pack(anchor="w")
    
    # --- COMING UP ---
    upcoming_frame = tk.Frame(box, bg="#fff3cd", padx=15, pady=15, relief="solid", borderwidth=1)
    upcoming_frame.pack(fill="x")
    
    tk.Label(upcoming_frame, text="COMING UP:", font=FONT_TITLE, bg="#fff3cd", fg="#856404").pack(anchor="w")
    tk.Label(upcoming_frame, text="\"1984\" — Due in 3 days (Oct 4)", 
             font=FONT, bg="#fff3cd", fg=TEXT_DARK).pack(anchor="w")

def show_books():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="BOOKS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

def show_authors():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="AUTHORS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

def show_categories():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="CATEGORIES", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

def show_reading_records():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="READING RECORDS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

def show_my_collection():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="MY COLLECTION", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

def show_account():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="ACCOUNT", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)
    if Main.current_user:
        tk.Label(box, text=f"Username: {Main.current_user['username']}", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=5)
        tk.Label(box, text=f"Role: {Main.current_user['role']}", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=5)

def show_settings():
    clear_all()
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    tk.Button(frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              command=show_user_dashboard).place(x=1130, y=15)
    box = tk.Frame(frame, bg=BG_CONTENT, padx=50, pady=40, relief="solid", borderwidth=1)
    box.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(box, text="SETTINGS", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=20)

# ==================================================
# MAIN USER DASHBOARD — Exact match to your design
# ==================================================
def show_user_dashboard():
    clear_all()
    root.configure(bg=BG_MAIN)
    
    username = Main.current_user["username"] if Main.current_user else "User"
    
    # ========= TOP HEADER =========
    top_header = tk.Frame(root, bg=BG_CONTENT, height=60, relief="solid", borderwidth=1)
    top_header.pack(side="top", fill="x")
    top_header.pack_propagate(False)
    
    tk.Label(top_header, text=f"WELCOME - USER", 
             font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)
    
    # Notification bell — top right
    tk.Button(top_header, text="🔔", font=16, bg=BG_CONTENT, fg=TEXT_DARK,
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
              command=back_to_login).pack(pady=5, side="bottom")
    
    # ========= MAIN CONTENT =========
    content = tk.Frame(root, bg=BG_MAIN)
    content.pack(side="right", fill="both", expand=True)
    
    # Get stats from database
    conn = get_db_connection()
    book_count = author_count = cat_count = rec_count = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Books"); book_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Authors"); author_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Categories"); cat_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Borrow_Records"); rec_count = cur.fetchone()[0]
        except Exception as e:
            print(f"Stats error: {e}")
        finally:
            conn.close()
    
    # === STATS CARDS — Books / Authors / Categories / Records ===
    stats_row = tk.Frame(content, bg=BG_MAIN)
    stats_row.pack(pady=25, padx=20, anchor="w")
    
    card_style = {"bg": BG_CONTENT, "padx": 30, "pady": 20, "relief": "solid", "borderwidth": 1}
    
    # Books Card
    books_card = tk.Frame(stats_row, **card_style)
    books_card.pack(side="left", padx=5)
    tk.Label(books_card, text="📚 Books", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(books_card, text=f"[{book_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    # Authors Card
    authors_card = tk.Frame(stats_row, **card_style)
    authors_card.pack(side="left", padx=5)
    tk.Label(authors_card, text="✍️ Authors", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(authors_card, text=f"[{author_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    # Categories Card
    cat_card = tk.Frame(stats_row, **card_style)
    cat_card.pack(side="left", padx=5)
    tk.Label(cat_card, text="📁 Categories", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(cat_card, text=f"[{cat_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    # Records Card
    rec_card = tk.Frame(stats_row, **card_style)
    rec_card.pack(side="left", padx=5)
    tk.Label(rec_card, text="⭐ Records", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack()
    tk.Label(rec_card, text=f"[{rec_count}]", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=3)
    
    # === QUICK SEARCH ===
    search_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=12, relief="solid", borderwidth=1)
    search_frame.pack(pady=5, padx=20, fill="x")
    
    tk.Label(search_frame, text="🔍 Quick Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=50, font=FONT)
    search_entry.pack(side="left")
    
    # === RECENT ACTIVITY / OVERVIEW ===
    activity_frame = tk.Frame(content, bg=BG_CONTENT, padx=15, pady=15, relief="solid", borderwidth=1)
    activity_frame.pack(pady=15, padx=20, fill="both", expand=True)
    
    tk.Label(activity_frame, text="📈 RECENT ACTIVITY / OVERVIEW", font=FONT_TITLE, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    # Table header
    header_row = tk.Frame(activity_frame, bg=BG_CONTENT)
    header_row.pack(fill="x", pady=5)
    tk.Label(header_row, text="Title — Author — Status — Date Added", font=FONT, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w")
    
    tk.Frame(activity_frame, bg="#d4b86a", height=1).pack(fill="x", pady=8)
    
    # Example list view
    tk.Label(activity_frame, text="(List View)  ← Example Quick Search: Oshi Mayncrap — Yuki — Reading — 2026-11-12", 
             font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=5)