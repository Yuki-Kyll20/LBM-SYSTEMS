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
    tk.Label(top_bar, text="ADMIN BOOKS SCREEN – (BOOKS Table)", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="+ Add Book", bg=BTN_GREEN, fg=TEXT_DARK, width=12,
              relief="solid", borderwidth=1, command=show_add_book_form).pack(side="right", padx=5)
    tk.Button(top_bar, text="Search", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    
    # --- Books List Container ---
    list_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=15, relief="solid", borderwidth=1)
    list_frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    tk.Label(list_frame, text="BOOKS LIST", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
    
    header = tk.Frame(list_frame, bg="#d4b86a", padx=5, pady=8)
    header.pack(fill="x")
    cols = [("ID", 5), ("BOOK TITLE", 25), ("YEAR", 10), ("ISBN", 18), ("STATUS", 10)]
    for col_name, width in cols:
        tk.Label(header, text=col_name, font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
                 width=width, anchor="w").pack(side="left", padx=2)
    
    tk.Frame(list_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=5)
    
    # --- Load Books ---
    load_books_from_db()
    
    # --- Book Rows ---
    rows_container = tk.Frame(list_frame, bg=BG_CONTENT)
    rows_container.pack(fill="both", expand=True)
    
    if not books_data:
        tk.Label(rows_container, text="No books found.", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=50)
    else:
        for idx, (book_id, title, year, isbn) in enumerate(books_data):
            status = "ACTIVE"
            row = tk.Frame(rows_container, bg=BG_CONTENT, pady=6, cursor="hand2")
            row.pack(fill="x")
            
            def make_select(i=idx, r=row):
                def select_this():
                    global selected_book_index
                    selected_book_index = i
                    for w in rows_container.winfo_children():
                        w.configure(bg=BG_CONTENT)
                    r.configure(bg="#e5d9b6")
                return select_this
            row.bind("<Button-1>", lambda e, f=make_select(idx): f())
            
            tk.Label(row, text=str(book_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=5, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=title, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=25, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=str(year) if year else "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=10, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=isbn or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=18, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=status, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=10, anchor="w").pack(side="left", padx=2)
    
    # --- Action Buttons ---
    list_btn_frame = tk.Frame(list_frame, bg=BG_CONTENT)
    list_btn_frame.pack(fill="x", pady=(15, 0))
    tk.Button(list_btn_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=12, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_book).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="EDIT", bg=BTN_BROWN, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_book_form).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="DELETE", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_book).pack(side="right", padx=5)

# ==================================================
# SCREEN 2: ADD / EDIT BOOK FORM — FIXED LAYOUT
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
    tk.Label(top_bar, text=page_title, font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="right", padx=5)
    
    # --- Form Container — FIXED: Don't use pack_propagate(False) ---
    form_container = tk.Frame(frame, bg=BG_CONTENT, padx=30, pady=30, relief="solid", borderwidth=1)
    form_container.pack(fill="both", expand=True, padx=150, pady=20)
    
    tk.Label(form_container, text="ADD / EDIT BOOK FORM", font=FONT_TITLE, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    form_entries = {}
    
    def make_form_field(label_text):
        row = tk.Frame(form_container, bg=BG_CONTENT)
        row.pack(fill="x", pady=8)
        tk.Label(row, text=label_text + ":", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK, anchor="w").pack(anchor="w")
        entry = tk.Entry(row, font=FONT)
        entry.pack(fill="x", pady=(3, 0))
        form_entries[label_text] = entry
    
    make_form_field("Title")
    make_form_field("Publisher Year")
    make_form_field("ISBN")
    make_form_field("Description")
    
    # --- Author Dropdown ---
    tk.Label(form_container, text="Assign Author:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(15, 0))
    author_select = ttk.Combobox(form_container, state="readonly", font=FONT)
    author_select.pack(fill="x", pady=(3, 0))
    form_entries["Author"] = author_select
    tk.Label(form_container, text="List linked authors here", font=("Arial", 9), bg=BG_CONTENT, fg="#666").pack(anchor="w")
    
    # --- Category Dropdown ---
    tk.Label(form_container, text="Assign Category:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(15, 0))
    cat_select = ttk.Combobox(form_container, state="readonly", font=FONT)
    cat_select.pack(fill="x", pady=(3, 0))
    form_entries["Category"] = cat_select
    tk.Label(form_container, text="List linked categories here", font=("Arial", 9), bg=BG_CONTENT, fg="#666").pack(anchor="w")
    
    load_dropdowns(author_select, cat_select)
    
    # --- Fill data if editing ---
    if book_data:
        form_entries["Title"].insert(0, book_data[1] or "")
        form_entries["Publisher Year"].insert(0, str(book_data[2]) if book_data[2] else "")
        form_entries["ISBN"].insert(0, book_data[3] or "")
    
    # --- SAVE & CANCEL BUTTONS — GUARANTEED VISIBLE ---
    btn_frame = tk.Frame(form_container, bg=BG_CONTENT)
    btn_frame.pack(fill="x", pady=(30, 20))
    
    def save_wrapper():
        save_book(form_entries)
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=5)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="left", padx=5)

# ==================================================
# DATABASE FUNCTIONS — FIXED COLUMN NAMES
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
        author_select.set("-- Select Author --")
        
        cur.execute("SELECT Category_ID, Category_Name FROM categories ORDER BY Category_Name")
        categories = cur.fetchall()
        cat_select['values'] = [f"{c[0]} - {c[1]}" for c in categories]
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
        # ✅ EXACT match from your XAMPP screenshot
        cur.execute("SELECT Book_ID, Book_Title, Publish_Year, ISBN FROM books ORDER BY Book_ID")
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
                SET Book_Title=%s, Publish_Year=%s, ISBN=%s, Book_Description=%s, Author_ID=%s, Category_ID=%s
                WHERE Book_ID=%s
            """, (title, int(year) if year.isdigit() else None, isbn, desc, author_id, cat_id, editing_book_id))
            messagebox.showinfo("Success", "Book updated!")
        else:
            cur.execute("""
                INSERT INTO books (Book_Title, Publish_Year, ISBN, Book_Description, Author_ID, Category_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, int(year) if year.isdigit() else None, isbn, desc, author_id, cat_id))
            messagebox.showinfo("Success", "Book added!")
        
        conn.commit()
        show_books_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Save failed:\n{e}")
    finally:
        conn.close()

def view_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    book = books_data[selected_book_index]
    messagebox.showinfo("Book Details",
        f"ID: {book[0]}\nTitle: {book[1]}\nYear: {book[2] or '—'}\nISBN: {book[3] or '—'}")

def delete_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    if not messagebox.askyesno("Confirm Delete", "Delete this book?"):
        return
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

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()