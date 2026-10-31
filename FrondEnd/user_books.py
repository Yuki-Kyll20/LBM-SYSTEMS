import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
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
# USER BOOKS LIST
# ==================================================
def show_user_books_screen():
    global selected_book_index, books_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    # ========= TOP BAR =========
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="BOOKS LIST", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_book).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    
    # Search
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", lambda e: filter_books(search_entry.get()))
    
    # ========= SCROLLABLE LIST =========
    list_container = tk.Frame(frame, bg=BG_CARD, padx=15, pady=15, relief="solid", borderwidth=1)
    list_container.pack(fill="both", expand=True, padx=15, pady=5)
    
    canvas = tk.Canvas(list_container, bg=BG_CARD, highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    rows_container = tk.Frame(canvas, bg=BG_CARD)
    
    rows_container.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=rows_container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # HEADER
    header = tk.Frame(rows_container, bg="#d4b86a", padx=5, pady=10)
    header.pack(fill="x")

    tk.Label(header, text="ID", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=5, anchor="w").pack(side="left", padx=3)
    tk.Label(header, text="BOOK TITLE", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=20, anchor="w").pack(side="left", padx=3)
    tk.Label(header, text="PUBLISHER", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=16, anchor="w").pack(side="left", padx=3)
    tk.Label(header, text="YEAR", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=8, anchor="center").pack(side="left", padx=3)
    tk.Label(header, text="ISBN", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=20, anchor="w").pack(side="left", padx=3)
    tk.Label(header, text="DESCRIPTION", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=22, anchor="w").pack(side="left", padx=3)
    tk.Label(header, text="STATUS", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=10, anchor="e").pack(side="right", padx=5)
    
    load_books_from_db()
    render_books_list(books_data, rows_container)

# ==================================================
# RENDER LIST
# ==================================================
def render_books_list(data_list, parent_frame=None):
    global selected_book_index
    # Clear rows except header
    for w in parent_frame.winfo_children():
        if w.cget("bg") not in ["#d4b86a", "#7B2CBF"]:
            w.destroy()
    
    if not data_list:
        tk.Label(parent_frame, text="No books found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
        return
    
    for idx, book in enumerate(data_list):
        book_id, title, publisher, year, isbn, description, status = book
        status = status or "ACTIVE"
        
        row = tk.Frame(parent_frame, bg=BG_CARD, pady=8, cursor="hand2")
        row.pack(fill="x", padx=5)
        
        def make_select(i=idx, r=row):
            def select_this(e):
                global selected_book_index
                selected_book_index = i
                # Reset all rows
                for child in parent_frame.winfo_children():
                    if isinstance(child, tk.Frame) and child.cget("cursor") == "hand2":
                        child.config(bg=BG_CARD)
                # Highlight selected
                r.config(bg="#e5d9b6")
            return select_this
        
        # Bind click to row
        row.bind("<Button-1>", make_select(idx, row))

        # ID
        tk.Label(row, text=str(book_id), font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=5, anchor="w").pack(side="left", padx=3)
        # BOOK TITLE
        tk.Label(row, text=title or "", font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=20, anchor="w").pack(side="left", padx=3)
        # PUBLISHER
        tk.Label(row, text=publisher or "", font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=16, anchor="w").pack(side="left", padx=3)
        # YEAR
        tk.Label(row, text=str(year) if year else "", font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=8, anchor="w").pack(side="left", padx=3)
        # ISBN
        tk.Label(row, text=isbn or "", font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=20, anchor="w").pack(side="left", padx=3)
        # DESCRIPTION
        tk.Label(row, text=(description[:22] + "...") if description and len(description) > 22 else (description or ""),
                 font=FONT, bg=BG_CARD, fg=TEXT_DARK,
                 width=22, anchor="w").pack(side="left", padx=3)
        # STATUS
        status_color = "#22c55e" if status.upper() == "ACTIVE" else "#ef4444"
        tk.Label(row, text=status.upper(), font=FONT, bg=BG_CARD, fg=status_color,
                 width=10, anchor="e").pack(side="right", padx=5)

# ==================================================
# FILTER / SEARCH
# ==================================================
def filter_books(search_text):
    search_text = search_text.strip().lower()
    filtered = books_data
    if search_text:
        filtered = [b for b in books_data if search_text in str(b[1]).lower()]
    
    for w in root.winfo_children():
        if isinstance(w, tk.Frame) and w.cget("bg") == BG_MAIN:
            for child in w.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == BG_CARD:
                    for c in child.winfo_children():
                        if isinstance(c, tk.Canvas):
                            for win in c.winfo_children():
                                if isinstance(win, tk.Frame):
                                    render_books_list(filtered, win)
                                    return

# ==================================================
# VIEW BOOK
# ==================================================
def view_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    
    book = books_data[selected_book_index]
    status = book[6] if len(book) > 6 else "ACTIVE"
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Label(top_bar, text="VIEW BOOK", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_user_books_screen).pack(side="right", padx=5)
    
    view_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    view_container.pack(pady=30)
    
    # PROFILE PICTURE BOX
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
    global books_data, selected_book_index
    books_data = []
    selected_book_index = -1
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT Book_ID, Book_Title, Publisher, Publish_Year, ISBN, Book_Description, Status
            FROM books ORDER BY Book_ID
        """)
        books_data = cur.fetchall()
        print(f"✅ Loaded {len(books_data)} books")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load books:\n{e}")
    finally:
        conn.close()

# ==================================================
# NAVIGATION
# ==================================================
def go_back():
    """Return to User Dashboard"""
    try:
        import UserDB
        UserDB.show_user_dashboard()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot go back:\n{e}")
        show_navigation_dashboard()