import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
back_to_login = Main.back_to_login
show_navigation_dashboard = Main.show_navigation_dashboard
BG_MAIN = Main.BG_MAIN
BG_CONTENT = Main.BG_CONTENT
BG_CARD = Main.BG_CARD
BTN_BROWN = Main.BTN_BROWN
BTN_RED = Main.BTN_RED
BTN_GREEN = Main.BTN_GREEN
BTN_YELLOW = Main.BTN_YELLOW
TEXT_DARK = Main.TEXT_DARK
FONT = Main.FONT
FONT_TITLE = Main.FONT_TITLE
FONT_HEADING = Main.FONT_HEADING

books_data = []
selected_book_index = -1

# ==================================================
# SCREEN 1: USER BOOKS LIST — READ-ONLY VIEW
# ==================================================
def show_user_books_screen():
    global selected_book_index, books_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="USER BOOKS SCREEN – (BOOKS TABLE)", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", lambda e: filter_books(search_entry.get()))
    
    list_frame = tk.Frame(frame, bg=BG_CARD, padx=15, pady=15, relief="solid", borderwidth=1)
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)

    header = tk.Frame(list_frame, bg="#d4b86a", padx=5, pady=8)
    header.pack(fill="x")
    
    cols = [
        ("ID", 5),
        ("BOOK TITLE", 22),
        ("PUBLISHER", 25),
        ("YEAR", 10),
        ("ISBN", 18),
        ("DESCRIPTION", 22),
        ("STATUS", 12)
    ]
    for col_name, width in cols:
        tk.Label(header, text=col_name, font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
                 width=width, anchor="w").pack(side="left", padx=2)
    
    tk.Frame(list_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=8)
    
    load_books_from_db()
    render_books_list(books_data)

# ==================================================
# RENDER LIST HELPER
# ==================================================
def render_books_list(data_list):
    global selected_book_index
    rows_container = tk.Frame(list_frame_ref)
    rows_container.pack(fill="both", expand=True)
    
    if not data_list:
        tk.Label(rows_container, text="No books found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
        return
    
    for idx, book in enumerate(data_list):
        book_id = book[0]
        title = book[1]
        publisher = book[2] or ""
        year = book[3]
        isbn = book[4]
        description = book[5] or ""
        status = book[6] if len(book) > 6 and book[6] else "ACTIVE"
        
        row = tk.Frame(rows_container, bg=BG_CARD, pady=6, cursor="hand2")
        row.pack(fill="x")
        
        def make_select(i=idx, r=row):
            def select_this():
                global selected_book_index
                selected_book_index = i
                for w in rows_container.winfo_children():
                    w.configure(bg=BG_CARD)
                r.configure(bg="#e5d9b6")
            return select_this
        row.bind("<Button-1>", lambda e, f=make_select(idx): f())
        
        tk.Label(row, text=str(book_id), font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=6, anchor="w").pack(side="left", padx=2)
        tk.Label(row, text=title, font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=25, anchor="w").pack(side="left", padx=2)
        tk.Label(row, text=publisher, font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=22, anchor="w").pack(side="left", padx=2)
        tk.Label(row, text=str(year) if year else "", font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=10, anchor="w").pack(side="left", padx=2)
        tk.Label(row, text=isbn or "", font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=18, anchor="w").pack(side="left", padx=2)
        desc_short = (description[:22] + "...") if description and len(description) > 22 else (description or "")
        tk.Label(row, text=desc_short, font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=TEXT_DARK, width=25, anchor="w").pack(side="left", padx=2)
        status_color = "#22c55e" if status.upper() == "ACTIVE" else "#ef4444"
        tk.Label(row, text=status.upper(), font=("Arial", 9, "bold"), bg=row.cget("bg"), fg=status_color, width=12, anchor="w").pack(side="left", padx=2)

    list_btn_frame = tk.Frame(list_frame_ref, bg=BG_CARD)
    list_btn_frame.pack(fill="x", pady=(15, 0))
    
    tk.Button(list_btn_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=12, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_book).pack(side="right", padx=5)

def filter_books(search_text):
    search_text = search_text.strip().lower()
    if not search_text:
        filtered = books_data
    else:
        filtered = [b for b in books_data if search_text in str(b[1]).lower()]
    for w in list_frame_ref.winfo_children():
        if isinstance(w, tk.Frame) and w not in [header_ref, tk.Frame(list_frame_ref, bg="#7B2CBF")]:
            try: w.destroy()
            except: pass
    render_books_list(filtered)

# ==================================================
# SCREEN 2: VIEW BOOK — USER ONLY
# ==================================================
def view_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    book = books_data[selected_book_index]
    status = book[6] if len(book) > 6 else "ACTIVE"
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)

    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="VIEW BOOK", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_user_books_screen).pack(side="right", padx=5)

    view_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    view_container.pack(pady=30)
    
    tk.Label(view_container, text="PROFILE\nPICTURE", font=FONT, bg="#e5d9b6", fg=TEXT_DARK,
             width=12, height=4, relief="solid", borderwidth=1).pack(anchor="w", pady=(0, 15))

    def make_view_field(label_text, value):
        tk.Label(view_container, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
        entry = tk.Entry(view_container, font=FONT, width=35)
        entry.insert(0, value or "")
        entry.configure(state="readonly")
        entry.pack(pady=(2, 10))

    make_view_field("ID:", str(book[0]))
    make_view_field("TITLE:", book[1] or "")
    make_view_field("PUBLISHER:", book[2] or "")
    make_view_field("PUBLISH YEAR:", str(book[3]) if book[3] else "")
    make_view_field("ISBN:", book[4] or "")
    
    tk.Label(view_container, text="DESCRIPTION:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    desc_box = tk.Text(view_container, font=FONT, width=35, height=4)
    desc_box.insert("1.0", book[5] or "")
    desc_box.configure(state="disabled")
    desc_box.pack(pady=(2, 10))
    
    make_view_field("STATUS:", status)

# ==================================================
# DATABASE FUNCTIONS
# ==================================================
def load_books_from_db():
    global books_data, selected_book_index, list_frame_ref, header_ref
    books_data = []
    selected_book_index = -1
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT Book_ID, Book_Title, Publisher, Publish_Year, ISBN, Book_Description, Status 
        FROM books ORDER BY Book_ID""")
        books_data = cur.fetchall()
        print(f"✅ User view: Loaded {len(books_data)} books")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load books:\n{e}")
    finally:
        conn.close()
    
    # Save references for search/filter
    for w in root.winfo_children():
        if isinstance(w, tk.Frame) and w.cget("bg") == BG_MAIN:
            for child in w.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == BG_CARD:
                    list_frame_ref = child
                    for c in child.winfo_children():
                        if isinstance(c, tk.Frame) and c.cget("bg") == "#d4b86a":
                            header_ref = c
                    break

# ==================================================
# NAVIGATION
# ==================================================
def go_back():
    # Go back to User Dashboard
    try:
        import UserDB
        UserDB.show_user_dashboard()
    except:
        show_navigation_dashboard()