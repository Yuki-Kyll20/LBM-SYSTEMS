import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import Main
import os
import shutil

# ========== SHORTCUTS ==========
root = (Main.root)
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

BOOK_COVER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book_covers")
books_data = []
selected_book_index = -1
editing_book_id = None

def get_book_cover_path(book_id):
    for extension in (".png", ".jpg", ".jpeg"):
        path = os.path.join(BOOK_COVER_DIR, f"book_{book_id}{extension}")
        if os.path.isfile(path):
            return path
    return None

def remove_book_cover_files(book_id, keep_path=None):
    keep_path = os.path.abspath(keep_path) if keep_path else None
    for extension in (".png", ".jpg", ".jpeg"):
        path = os.path.join(BOOK_COVER_DIR, f"book_{book_id}{extension}")
        if os.path.isfile(path) and os.path.abspath(path) != keep_path:
            os.remove(path)

def display_book_cover(label, image_path, size=(160, 200)):
    if not image_path:
        label.config(
            image="", text="BOOK\nCOVER", width=20, height=10,
            bg="#e5d9b6",
        )
        label.image = None
        return None

    try:
        with Image.open(image_path) as source:
            image = source.convert("RGB")
            image.thumbnail(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo, text="", width=size[0], height=size[1])
        label.image = photo
        return photo
    except (OSError, tk.TclError) as err:
        messagebox.showerror("Cover Error", f"Could not display book cover:\n{err}")
        return None

# ==================================================
# BOOKS LIST
# ==================================================
def show_books_screen():
    global selected_book_index, books_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)

    # ========= TOP BAR =========
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="BOOKS LIST", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="DELETE", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_book).pack(side="right", padx=3)
    tk.Button(top_bar, text="EDIT", bg=BTN_BROWN, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_book_form).pack(side="right", padx=3)
    tk.Button(top_bar, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_book).pack(side="right", padx=3)
    tk.Button(top_bar, text="+ Add Book", bg=BTN_GREEN, fg=TEXT_DARK, width=14,
              relief="solid", borderwidth=1, command=show_add_book_form).pack(side="right", padx=5)
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
    
    rows_window = canvas.create_window((0, 0), window=rows_container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(rows_window, width=event.width),
    )
    
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
    # Clear rows except header and divider
    for w in parent_frame.winfo_children():
        if w.cget("bg") not in ["#d4b86a", "#7B2CBF"]:
            w.destroy()
    
    if not data_list:
        tk.Label(parent_frame, text="No books found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
        return
    
    for book in data_list:
        book_id, title, publisher, year, isbn, description, status = book
        status = status or "ACTIVE"
        original_index = next(
            (i for i, original in enumerate(books_data) if original[0] == book_id),
            -1,
        )
        
        row = tk.Frame(parent_frame, bg=BG_CARD, pady=8, cursor="hand2")
        row.pack(fill="x", padx=5)
        
        def make_select(i=original_index, r=row):
            def select_this(e):
                global selected_book_index
                selected_book_index = i
                for child in parent_frame.winfo_children():
                    if isinstance(child, tk.Frame) and child.cget("cursor") == "hand2":
                        child.config(bg=BG_CARD)
                        for item in child.winfo_children():
                            if isinstance(item, tk.Label):
                                item.config(bg=BG_CARD)
                r.config(bg="#e5d9b6")
                for item in r.winfo_children():
                    if isinstance(item, tk.Label):
                        item.config(bg="#e5d9b6")
            return select_this

        select_row = make_select()
        row.bind("<Button-1>", select_row)
        
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
        for item in row.winfo_children():
            item.bind("<Button-1>", select_row)

# ==================================================
# FILTER / SEARCH
# ==================================================
def filter_books(search_text):
    global selected_book_index
    selected_book_index = -1
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
# ADD / EDIT BOOK
# ==================================================
def show_add_book_form():
    global editing_book_id
    editing_book_id = None
    show_book_form_screen()

def show_edit_book_form():
    global selected_book_index, editing_book_id
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    book = books_data[selected_book_index]
    editing_book_id = book[0]
    show_book_form_screen(book_data=book)

def show_book_form_screen(book_data=None):
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    page_title = "Edit Book" if editing_book_id else "Add Book"
    tk.Label(top_bar, text=page_title, font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="right", padx=5)

    action_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    action_bar.pack(side="bottom", fill="x")
    form_area = tk.Frame(frame, bg=BG_MAIN)
    form_area.pack(fill="both", expand=True, padx=20, pady=10)
    form_canvas = tk.Canvas(form_area, bg=BG_MAIN, highlightthickness=0)
    form_scrollbar = tk.Scrollbar(form_area, orient="vertical", command=form_canvas.yview)
    form_container = tk.Frame(
        form_canvas, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1
    )
    form_area.grid_rowconfigure(0, weight=1)
    form_area.grid_columnconfigure(0, weight=1)
    form_canvas.grid(row=0, column=0, sticky="nsew")
    form_scrollbar.grid(row=0, column=1, sticky="ns")
    form_window = form_canvas.create_window((0, 0), window=form_container, anchor="nw")
    form_container.bind(
        "<Configure>",
        lambda _event: form_canvas.configure(scrollregion=form_canvas.bbox("all")),
    )
    form_canvas.bind(
        "<Configure>",
        lambda event: form_canvas.itemconfigure(form_window, width=event.width),
    )
    form_canvas.configure(yscrollcommand=form_scrollbar.set)
    
    tk.Label(form_container, text="ADD / EDIT BOOK", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

    cover_state = {"selected_path": None, "remove": False, "photo": None}
    cover_frame = tk.Frame(form_container, bg=BG_CARD)
    cover_frame.pack(anchor="w", pady=(0, 15))
    cover_preview = tk.Label(
        cover_frame, text="BOOK\nCOVER", bg="#e5d9b6", fg=TEXT_DARK,
        font=FONT, width=20, height=10, relief="solid", borderwidth=1,
    )
    cover_preview.pack(side="left", padx=(0, 12))
    cover_buttons = tk.Frame(cover_frame, bg=BG_CARD)
    cover_buttons.pack(side="left")

    def refresh_cover_preview():
        path = cover_state["selected_path"]
        if not path and not cover_state["remove"] and editing_book_id:
            path = get_book_cover_path(editing_book_id)
        cover_state["photo"] = display_book_cover(cover_preview, path)

    def upload_book_cover():
        path = filedialog.askopenfilename(
            title="Select Book Cover",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")],
        )
        if not path:
            return
        try:
            with Image.open(path) as image:
                image.verify()
        except (OSError, ValueError) as err:
            messagebox.showerror("Invalid Image", f"Could not open this image:\n{err}")
            return
        cover_state["selected_path"] = path
        cover_state["remove"] = False
        refresh_cover_preview()

    def remove_book_cover():
        cover_state["selected_path"] = None
        cover_state["remove"] = True
        refresh_cover_preview()

    tk.Button(
        cover_buttons, text="UPLOAD", bg=BTN_GREEN, fg=TEXT_DARK,
        width=12, font=FONT, relief="solid", borderwidth=1,
        command=upload_book_cover,
    ).pack(pady=3)
    tk.Button(
        cover_buttons, text="REMOVE", bg=BTN_RED, fg="white",
        width=12, font=FONT, relief="solid", borderwidth=1,
        command=remove_book_cover,
    ).pack(pady=3)
    refresh_cover_preview()
    
    content_row = tk.Frame(form_container, bg=BG_CARD)
    content_row.pack()
    
    left_col = tk.Frame(content_row, bg=BG_CARD)
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 30))
    
    def make_field(parent, label_text):
        tk.Label(parent, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
        entry = tk.Entry(parent, font=FONT, width=30)
        entry.pack(pady=(2, 10))
        return entry
    
    title_entry = make_field(left_col, "Title:")
    publisher_entry = make_field(left_col, "Publisher:")
    year_entry = make_field(left_col, "Publish Year:")
    isbn_entry = make_field(left_col, "ISBN:")
    
    tk.Label(left_col, text="Description:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    desc_text = tk.Text(left_col, font=FONT, width=30, height=4)
    desc_text.pack(pady=(2, 10))
    
    right_col = tk.Frame(content_row, bg=BG_CARD)
    right_col.pack(side="right", fill="both", expand=True)
    
    tk.Label(right_col, text="Assign Author:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    author_frame = tk.Frame(right_col, bg=BG_CARD)
    author_frame.pack(pady=(2, 10))
    author_select = ttk.Combobox(author_frame, state="readonly", font=FONT, width=25)
    author_select.pack(side="left")
    
    tk.Label(right_col, text="Assign Category:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x")
    cat_frame = tk.Frame(right_col, bg=BG_CARD)
    cat_frame.pack(pady=(2, 10))
    cat_select = ttk.Combobox(cat_frame, state="readonly", font=FONT, width=25)
    cat_select.pack(side="left")
    
    load_dropdowns(author_select, cat_select)

    if book_data:
        title_entry.insert(0, book_data[1] or "")
        publisher_entry.insert(0, book_data[2] or "")
        year_entry.insert(0, str(book_data[3]) if book_data[3] else "")
        isbn_entry.insert(0, book_data[4] or "")
        desc_text.insert("1.0", book_data[5] or "")
        author_select.set("")
        cat_select.set("")
        conn = get_db_connection()
        if not conn:
            show_books_screen()
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT Author_ID, Category_ID FROM books WHERE Book_ID=%s",
                (editing_book_id,),
            )
            assignments = cur.fetchone()
            if assignments:
                author_id, category_id = assignments
                for index, value in enumerate(author_select["values"]):
                    if value.split(" - ", 1)[0] == str(author_id):
                        author_select.current(index)
                        break
                for index, value in enumerate(cat_select["values"]):
                    if value.split(" - ", 1)[0] == str(category_id):
                        cat_select.current(index)
                        break
        except Exception as err:
            messagebox.showerror("Load Error", f"Could not load book author/category:\n{err}")
            show_books_screen()
            return
        finally:
            conn.close()

    btn_frame = tk.Frame(action_bar, bg=BG_CARD)
    btn_frame.pack()
    
    def save_wrapper():
        try:
            author_sel = author_select.get()
            cat_sel = cat_select.get()
            author_id = int(author_sel.split(" - ", 1)[0]) if " - " in author_sel else None
            cat_id = int(cat_sel.split(" - ", 1)[0]) if " - " in cat_sel else None
        except ValueError as err:
            messagebox.showerror("Invalid Selection", f"Could not read the selected author or category:\n{err}")
            return

        year_value = year_entry.get().strip()
        if year_value and not year_value.isdigit():
            messagebox.showwarning("Invalid Year", "Publish year must contain digits only.")
            return
        save_book_data(
            title_entry.get().strip(),
            publisher_entry.get().strip(),
            year_value,
            isbn_entry.get().strip(),
            desc_text.get("1.0", "end-1c").strip(),
            author_id, cat_id, cover_state
        )
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="left", padx=10)

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
              relief="solid", borderwidth=1, command=show_books_screen).pack(side="right", padx=5)

    view_area = tk.Frame(frame, bg=BG_MAIN)
    view_area.pack(fill="both", expand=True, padx=20, pady=10)
    view_canvas = tk.Canvas(view_area, bg=BG_MAIN, highlightthickness=0)
    view_scrollbar = tk.Scrollbar(view_area, orient="vertical", command=view_canvas.yview)
    view_container = tk.Frame(
        view_canvas, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1
    )
    view_window = view_canvas.create_window((0, 0), window=view_container, anchor="nw")
    view_container.bind(
        "<Configure>",
        lambda _event: view_canvas.configure(scrollregion=view_canvas.bbox("all")),
    )
    view_canvas.bind(
        "<Configure>",
        lambda event: view_canvas.itemconfigure(view_window, width=event.width),
    )
    view_canvas.configure(yscrollcommand=view_scrollbar.set)
    view_canvas.pack(side="left", fill="both", expand=True)
    view_scrollbar.pack(side="right", fill="y")
    
    cover_label = tk.Label(
        view_container, text="BOOK\nCOVER", font=FONT, bg="#e5d9b6", fg=TEXT_DARK,
        width=20, height=10, relief="solid", borderwidth=1,
    )
    cover_label.pack(anchor="w", pady=(0, 15))
    display_book_cover(cover_label, get_book_cover_path(book[0]))
    
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
# DELETE BOOK
# ==================================================
def delete_selected_book():
    global selected_book_index
    if selected_book_index < 0 or selected_book_index >= len(books_data):
        messagebox.showwarning("Warning", "Select a book first!")
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
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
                try:
                    remove_book_cover_files(book_id)
                except OSError as err:
                    messagebox.showwarning(
                        "Cover Cleanup",
                        f"Book deleted, but its cover file could not be removed:\n{err}",
                    )
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
            author_select.current(0)
        
        cur.execute("SELECT Category_ID, Category_Name FROM categories ORDER BY Category_Name")
        categories = cur.fetchall()
        cat_select['values'] = [f"{c[0]} - {c[1]}" for c in categories]
        if categories:
            cat_select.current(0)
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load author/category choices:\n{e}")
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

def save_book_data(title, publisher, year, isbn, desc, author_id, cat_id, cover_state=None):
    global editing_book_id
    if not title:
        messagebox.showwarning("Warning", "Title is required!")
        return
    if year and (not year.isdigit() or not 1 <= int(year) <= 9999):
        messagebox.showwarning("Invalid Year", "Publish year must be a number between 1 and 9999.")
        return
    
    conn = get_db_connection()
    if not conn:
        return
    staged_cover_path = None
    try:
        cur = conn.cursor()
        year_val = int(year) if year.isdigit() else None
        
        if editing_book_id:
            cur.execute("""
                UPDATE books
                SET Book_Title=%s, Publisher=%s, Publish_Year=%s, ISBN=%s,
                    Book_Description=%s, Author_ID=%s, Category_ID=%s
                WHERE Book_ID=%s
            """, (title, publisher, year_val, isbn, desc, author_id, cat_id, editing_book_id))
            book_id = editing_book_id
        else:
            cur.execute("""
                INSERT INTO books (Book_Title, Publisher, Publish_Year, ISBN,
                                   Book_Description, Author_ID, Category_ID, Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'ACTIVE')
            """, (title, publisher, year_val, isbn, desc, author_id, cat_id))
            book_id = cur.lastrowid

        selected_cover = cover_state.get("selected_path") if cover_state else None
        cover_path = None
        if selected_cover:
            extension = os.path.splitext(selected_cover)[1].lower()
            if extension not in {".png", ".jpg", ".jpeg"}:
                raise ValueError("Book covers must be PNG or JPEG files.")
            os.makedirs(BOOK_COVER_DIR, exist_ok=True)
            cover_path = os.path.join(BOOK_COVER_DIR, f"book_{book_id}{extension}")
            if os.path.abspath(selected_cover) != os.path.abspath(cover_path):
                staged_cover_path = cover_path + ".uploading"
                shutil.copy2(selected_cover, staged_cover_path)
                with Image.open(staged_cover_path) as image:
                    image.verify()
        
        conn.commit()
        if staged_cover_path:
            try:
                os.replace(staged_cover_path, cover_path)
                staged_cover_path = None
            except OSError as err:
                messagebox.showwarning(
                    "Book Saved",
                    f"Book details were saved, but the new cover could not be installed:\n{err}",
                )
                show_books_screen()
                return

        if cover_state and (selected_cover or cover_state.get("remove")):
            try:
                remove_book_cover_files(book_id, keep_path=cover_path)
            except OSError as err:
                messagebox.showwarning(
                    "Cover Cleanup",
                    f"Book details were saved, but an old cover file could not be removed:\n{err}",
                )

        messagebox.showinfo("Success", "Book updated!" if editing_book_id else "Book added!")
        show_books_screen()
    except Exception as e:
        conn.rollback()
        if staged_cover_path and os.path.isfile(staged_cover_path):
            try:
                os.remove(staged_cover_path)
            except OSError as cleanup_error:
                messagebox.showwarning(
                    "Cover Cleanup",
                    f"Could not remove temporary cover file:\n{cleanup_error}",
                )
        messagebox.showerror("Error", f"Save failed:\n{e}")
    finally:
        conn.close()

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()