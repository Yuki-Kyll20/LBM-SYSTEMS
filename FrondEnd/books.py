import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
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
editing_book_id = None

# ==================================================
# SCREEN 1: BOOKS LIST
# ==================================================
def show_books_screen():
    global selected_book_index, books_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="ADMIN BOOKS SCREEN – (BOOKS Table)", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    tk.Button(top_bar, text="+ Add Book", bg=BTN_GREEN, fg=TEXT_DARK, width=12,
              relief="solid", borderwidth=1, command=show_add_book_form).pack(side="right", padx=5)
    
    # --- Search Bar ---
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    
    # --- Books List ---
    list_frame = tk.Frame(frame, bg=BG_CARD, padx=15, pady=15, relief="solid", borderwidth=1)
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)
    
    tk.Label(list_frame, text="BOOKS LIST", font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    header = tk.Frame(list_frame, bg="#d4b86a", padx=5, pady=8)
    header.pack(fill="x")
    
    cols = [("ID", 5), ("BOOK TITLE", 30), ("YEAR", 12), ("ISBN", 20), ("STATUS", 12)]
    for col_name, width in cols:
        tk.Label(header, text=col_name, font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
                 width=width, anchor="w").pack(side="left", padx=2)
    
    tk.Frame(list_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=8)
    
    load_books_from_db()
    
    rows_container = tk.Frame(list_frame, bg=BG_CARD)
    rows_container.pack(fill="both", expand=True)
    
    if not books_data:
        tk.Label(rows_container, text="No books found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
    else:
        for idx, book in enumerate(books_data):
            book_id = book[0]
            title = book[1]
            year = book[2]
            isbn = book[3]
            status = book[4] if len(book) > 4 and book[4] else "ACTIVE"
            
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
            
            tk.Label(row, text=str(book_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=5, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=title, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=30, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=str(year) if year else "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=isbn or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=20, anchor="w").pack(side="left", padx=2)
            
            status_color = "#22c55e" if status.upper() == "ACTIVE" else "#ef4444"
            tk.Label(row, text=status.upper(), font=FONT, bg=row.cget("bg"), fg=status_color, width=12, anchor="w").pack(side="left", padx=2)
    
    list_btn_frame = tk.Frame(list_frame, bg=BG_CARD)
    list_btn_frame.pack(fill="x", pady=(15, 0))
    
    tk.Button(list_btn_frame, text="DELETE", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_book).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="EDIT", bg=BTN_BROWN, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_book_form).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=12, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_book).pack(side="right", padx=5)

# ==================================================
# SCREEN 2: ADD / EDIT BOOK — 2-COLUMN DESIGN
# ==================================================
def show_add_book_form():
    global editing_book_id
    editing_book_id = None
    show_book_form_screen()

def show_edit_book_form():
    global selected_book_index, editing_book_id
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Please select a book first!")
        return
    book = books_data[selected_book_index]
    editing_book_id = book[0]
    show_book_form_screen(book_data=book)

def show_book_form_screen(book_data=None):
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    page_title = "Edit Book" if editing_book_id else "Add Book"
    tk.Label(top_bar, text=page_title, font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="right", padx=5)
    
    form_container = tk.Frame(frame, bg=BG_CARD, padx=20, pady=20, relief="solid", borderwidth=1)
    form_container.pack(fill="both", expand=True, padx=100, pady=30)
    
    tk.Label(form_container, text="ADD / EDIT BOOK", font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    form_entries = {}
    content_row = tk.Frame(form_container, bg=BG_CARD)
    content_row.pack(fill="both", expand=True)
    
    left_col = tk.Frame(content_row, bg=BG_CARD)
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 30))
    
    def make_field(parent, label_text):
        tk.Label(parent, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 2))
        entry = tk.Entry(parent, font=FONT, width=35)
        entry.pack(fill="x", pady=(0, 5))
        form_entries[label_text] = entry
        return entry
    
    make_field(left_col, "Title")
    make_field(left_col, "Publisher Year")
    make_field(left_col, "ISBN")
    make_field(left_col, "Description")
    
    right_col = tk.Frame(content_row, bg=BG_CARD)
    right_col.pack(side="right", fill="both", expand=True)
    
    tk.Label(right_col, text="Assign Authors:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 2))
    author_frame = tk.Frame(right_col, bg=BG_CARD)
    author_frame.pack(fill="x", pady=(0, 5))
    author_select = ttk.Combobox(author_frame, state="readonly", font=FONT, width=25)
    author_select.pack(side="left")
    tk.Label(author_frame, text="List linked authors here", font=("Arial", 9), bg=BG_CARD, fg="#666").pack(side="left", padx=10)
    form_entries["Author"] = author_select
    
    tk.Label(right_col, text="Assign Categories:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(15, 2))
    cat_frame = tk.Frame(right_col, bg=BG_CARD)
    cat_frame.pack(fill="x", pady=(0, 5))
    cat_select = ttk.Combobox(cat_frame, state="readonly", font=FONT, width=25)
    cat_select.pack(side="left")
    tk.Label(cat_frame, text="List linked categories here", font=("Arial", 9), bg=BG_CARD, fg="#666").pack(side="left", padx=10)
    form_entries["Category"] = cat_select
       
    load_dropdowns(author_select, cat_select)
    
    # --- Fill data if editing ---
    if book_data:
        form_entries["Title"].insert(0, book_data[1] or "")
        form_entries["Publisher Year"].insert(0, str(book_data[2]) if book_data[2] else "")
        form_entries["ISBN"].insert(0, book_data[3] or "")
    
    btn_frame = tk.Frame(form_container, bg=BG_CARD)
    btn_frame.pack(pady=(30, 10))
    
    def save_wrapper():
        save_book(form_entries)
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="left", padx=10)

# ==================================================
# SCREEN 3: VIEW BOOK — YOUR DESIGN
# ==================================================
def view_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    book = books_data[selected_book_index]
    status = book[4] if len(book) > 4 else "ACTIVE"
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="VIEW BOOK", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="right", padx=5)
    
    # --- View Form — Exact Design ---
    view_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    view_container.pack(pady=50)
    
    # Profile Picture Placeholder
    profile_frame = tk.Frame(view_container, bg=BG_CARD)
    profile_frame.pack(anchor="w", pady=(0, 15))
    tk.Label(profile_frame, text="PROFILE\nPICTURE", font=FONT, bg="#e5d9b6", fg=TEXT_DARK,
             width=12, height=4, relief="solid", borderwidth=1).pack()
    
    # Read-only Fields
    def make_view_field(label_text, value):
        tk.Label(view_container, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
        entry = tk.Entry(view_container, font=FONT, width=40)
        entry.insert(0, value or "")
        entry.configure(state="readonly")
        entry.pack(fill="x")
    
    make_view_field("ID:", str(book[0]))
    make_view_field("TITLE:", book[1] or "")
    make_view_field("YEAR:", str(book[2]) if book[2] else "")
    make_view_field("ISBN:", book[3] or "")
    make_view_field("STATUS:", status)

# ==================================================
# SCREEN 4: DELETE BOOK — YOUR DESIGN
# ==================================================
def delete_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Delete Confirmation Box — Exact Design ---
    delete_container = tk.Frame(frame, bg=BG_CARD, padx=40, pady=30, relief="solid", borderwidth=1)
    delete_container.pack(pady=100)
    
    tk.Label(delete_container, text="DELETE BOOK", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(pady=(0, 20))
    tk.Label(delete_container, text="ARE YOU SURE YOU WANT TO\nDELETE THIS BOOK?", 
             font=FONT, bg=BG_CARD, fg=TEXT_DARK, justify="center").pack(pady=(0, 25))
    
    btn_frame = tk.Frame(delete_container, bg=BG_CARD)
    btn_frame.pack()
    
    def confirm_delete():
        book_id = books_data[selected_book_index][0]
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM books WHERE Book_ID = %s", (book_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Book removed!")
                show_books_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed:\n{e}")
            finally:
                conn.close()
    
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1, command=confirm_delete).pack(side="left", padx=15)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="left", padx=15)

# ==================================================
# DATABASE FUNCTIONS
# ==================================================
def load_dropdowns(author_select, cat_select):
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT Author_ID, Author_Fullname FROM authors ORDER BY Author_Fullname")
        authors = cur.fetchall()
        author_select['values'] = [f"{a[0]} - {a[1]}" for a in authors]
        if authors:
            author_select.set("-- Select Author --")
        
        cur.execute("SELECT Category_ID, Category_Name FROM categories ORDER BY Category_Name")
        categories = cur.fetchall()
        cat_select['values'] = [f"{c[0]} - {c[1]}" for c in categories]
        if categories:
            cat_select.set("-- Select Category --")
    except Exception as e:
        print(f"Dropdown error: {e}")
    finally:
        conn.close()

def load_books_from_db():
    global books_data, selected_book_index
    books_data = []
    selected_book_index = -1
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT Book_ID, Book_Title, Publish_Year, ISBN, Status FROM books ORDER BY Book_ID")
        books_data = cur.fetchall()
        print(f"✅ Loaded {len(books_data)} books")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load books:\n{e}")
    finally:
        conn.close()

def save_book(form_entries):
    global editing_book_id
    title = form_entries["Title"].get().strip()
    year = form_entries["Publisher Year"].get().strip()
    isbn = form_entries["ISBN"].get().strip()
    desc = form_entries["Description"].get().strip()
    author_sel = form_entries["Author"].get()
    cat_sel = form_entries["Category"].get()
    
    if not title:
        messagebox.showwarning("Warning", "Title is required!")
        return
    
    author_id = int(author_sel.split(" - ")[0]) if " - " in author_sel else None
    cat_id = int(cat_sel.split(" - ")[0]) if " - " in cat_sel else None
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        
        if editing_book_id:
            cur.execute("""
                UPDATE books 
                SET Book_Title=%s, Publish_Year=%s, ISBN=%s, Book_Description=%s, 
                    Author_ID=%s, Category_ID=%s
                WHERE Book_ID=%s
            """, (title, int(year) if year.isdigit() else None, isbn, desc, author_id, cat_id, editing_book_id))
            messagebox.showinfo("Success", "Book updated!")
        else:
            cur.execute("""
                INSERT INTO books (Book_Title, Publish_Year, ISBN, Book_Description, 
                                   Author_ID, Category_ID, Status)
                VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVE')
            """, (title, int(year) if year.isdigit() else None, isbn, desc, author_id, cat_id))
            messagebox.showinfo("Success", "Book added!")
        
        conn.commit()
        show_books_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Save failed:\n{e}")
    finally:
        conn.close()

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()