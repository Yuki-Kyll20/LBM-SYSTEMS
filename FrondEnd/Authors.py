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

authors_data = []
selected_author_index = -1
editing_author_id = None

# ==================================================
# SCREEN 2: AUTHORS LIST
# ==================================================

def show_authors_screen():
    global selected_author_index, authors_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="ADMIN AUTHORS SCREEN – (AUTHORS Table)", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    tk.Button(top_bar, text="+ Add Author", bg=BTN_GREEN, fg=TEXT_DARK, width=12,
              relief="solid", borderwidth=1, command=show_add_author_form).pack(side="right", padx=5)
    
    # --- Search Bar ---
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    
    # --- Authors List ---
    list_frame = tk.Frame(frame, bg=BG_CARD, padx=15, pady=15, relief="solid", borderwidth=1)
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)
    
    tk.Label(list_frame, text="AUTHORS LIST", font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))
    
    header = tk.Frame(list_frame, bg="#d4b86a", padx=5, pady=8)
    header.pack(fill="x")
    
    cols = [("ID", 5), ("FULL NAME", 25), ("BIOGRAPHY", 35), ("BOOK COUNT", 12)]
    for col_name, width in cols:
        tk.Label(header, text=col_name, font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
                 width=width, anchor="w").pack(side="left", padx=2)
    
    tk.Frame(list_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=8)
    
    load_authors_from_db()
    
    rows_container = tk.Frame(list_frame, bg=BG_CARD)
    rows_container.pack(fill="both", expand=True)
    
    if not authors_data:
        tk.Label(rows_container, text="No authors found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
    else:
        for idx, author in enumerate(authors_data):
            author_id, fullname, bio, book_count = author
            
            row = tk.Frame(rows_container, bg=BG_CARD, pady=6, cursor="hand2")
            row.pack(fill="x")
            
            def make_select(i=idx, r=row):
                def select_this():
                    global selected_author_index
                    selected_author_index = i
                    for w in rows_container.winfo_children():
                        w.configure(bg=BG_CARD)
                    r.configure(bg="#e5d9b6")
                return select_this
            row.bind("<Button-1>", lambda e, f=make_select(idx): f())
            
            tk.Label(row, text=str(author_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=5, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=fullname or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=25, anchor="w").pack(side="left", padx=2)
            bio_short = (bio[:30] + "...") if bio and len(bio) > 30 else (bio or "")
            tk.Label(row, text=bio_short, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=35, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=str(book_count), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=2)
    
    list_btn_frame = tk.Frame(list_frame, bg=BG_CARD)
    list_btn_frame.pack(fill="x", pady=(15, 0))
    
    tk.Button(list_btn_frame, text="DELETE", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_author).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="EDIT", bg=BTN_BROWN, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_author_form).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=12, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_author).pack(side="right", padx=5)

# ==================================================
# SCREEN 2: ADD / EDIT AUTHOR
# ==================================================
def show_add_author_form():
    global editing_author_id
    editing_author_id = None
    show_author_form_screen()

def show_edit_author_form():
    global selected_author_index, editing_author_id
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Please select an author first!")
        return
    author = authors_data[selected_author_index]
    editing_author_id = author[0]
    show_author_form_screen(author_data=author)

def show_author_form_screen(author_data=None):
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    page_title = "Edit Author" if editing_author_id else "Add Author"
    tk.Label(top_bar, text=page_title, font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="right", padx=5)
    
    form_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    form_container.pack(pady=50)
    
    tk.Label(form_container, text="ADD / EDIT AUTHOR", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    form_entries = {}
    
    def make_field(label_text):
        tk.Label(form_container, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
        entry = tk.Entry(form_container, font=FONT, width=40)
        entry.pack(fill="x")
        form_entries[label_text] = entry
    
    make_field("First Name")
    make_field("Last Name")
    
    tk.Label(form_container, text="Biography", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    bio_text = tk.Text(form_container, font=FONT, width=40, height=6, wrap="word")
    bio_text.pack(fill="x")
    form_entries["Biography"] = bio_text
    
    if author_data:
        name_parts = (author_data[1] or "").split(", ", 1)
        if len(name_parts) == 2:
            last, first = name_parts
        else:
            first = author_data[1] or ""
            last = ""
        
        form_entries["First Name"].insert(0, first.strip())
        form_entries["Last Name"].insert(0, last.strip())
        form_entries["Biography"].insert("1.0", author_data[2] or "")
    
    btn_frame = tk.Frame(form_container, bg=BG_CARD)
    btn_frame.pack(pady=(25, 0))
    
    def save_wrapper():
        save_author(form_entries)
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="left", padx=10)

# ==================================================
# SCREEN 3: VIEW AUTHOR
# ==================================================
def view_selected_author():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Select an author first!")
        return
    author = authors_data[selected_author_index]
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- View Card ---
    view_card = tk.Frame(frame, bg="#FFF3D0", padx=20, pady=20, relief="solid", borderwidth=2)
    view_card.pack(pady=40)
    
    # Header row: Title + BACK button
    header_row = tk.Frame(view_card, bg="#FFF3D0")
    header_row.pack(fill="x", pady=(0, 20))
    
    tk.Label(header_row, text="VIEW AUTHOR", font=FONT_HEADING, bg="#FFF3D0", fg=TEXT_DARK).pack(side="left")
    tk.Button(header_row, text="BACK", bg=BTN_BROWN, fg="white", width=8,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="right")
    
    # Profile Picture Placeholder
    profile_frame = tk.Frame(view_card, bg="#FFF3D0")
    profile_frame.pack(anchor="w", pady=(0, 15))
    tk.Label(profile_frame, text="PROFILE\nPICTURE", font=FONT, bg="#FFE082", fg=TEXT_DARK,
             width=12, height=4, relief="solid", borderwidth=1).pack()
    
    # Fields — Exact label formatting
    def make_view_field(label_text, value):
        tk.Label(view_card, text=label_text, font=FONT, bg="#FFF3D0", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 2))
        entry = tk.Entry(view_card, font=FONT, width=35)
        entry.insert(0, value or "")
        entry.configure(state="readonly")
        entry.pack(fill="x")
    
    make_view_field("ID:", str(author[0]))
    make_view_field("FULL NAME:", author[1] or "")
    make_view_field("BIOGRAPHY:", author[2] or "")
    make_view_field("BOOK COUNT:", str(author[3]))

# ==================================================
# SCREEN 4: DELETE AUTHOR
# ==================================================
def delete_selected_author():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Select an author first!")
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Delete Card — Exact Design ---
    delete_card = tk.Frame(frame, bg="#FFF3D0", padx=40, pady=30, relief="solid", borderwidth=2)
    delete_card.pack(pady=120)
    
    tk.Label(delete_card, text="DELETE AUTHOR", font=FONT_HEADING, bg="#FFF3D0", fg=TEXT_DARK).pack(pady=(0, 20))
    tk.Label(delete_card, text="ARE YOU SURE YOU WANT TO\nDELETE THIS AUTHOR?", 
             font=FONT, bg="#FFF3D0", fg=TEXT_DARK, justify="center").pack(pady=(0, 25))
    
    btn_frame = tk.Frame(delete_card, bg="#FFF3D0")
    btn_frame.pack()
    
    def confirm_delete():
        author_id = authors_data[selected_author_index][0]
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM authors WHERE Author_ID = %s", (author_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Author removed!")
                show_authors_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed:\n{e}")
            finally:
                conn.close()
    
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1, command=confirm_delete).pack(side="left", padx=15)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="left", padx=15)

# ==================================================
# DATABASE FUNCTIONS
# ==================================================
def load_authors_from_db():
    global authors_data, selected_author_index
    authors_data = []
    selected_author_index = -1
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.Author_ID, a.Author_Fullname, a.Author_Biography,
                   COUNT(b.Book_ID) as Book_Count
            FROM authors a
            LEFT JOIN books b ON a.Author_ID = b.Author_ID
            GROUP BY a.Author_ID
            ORDER BY a.Author_ID
        """)
        authors_data = cur.fetchall()
        print(f"✅ Loaded {len(authors_data)} authors")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load authors:\n{e}")
    finally:
        conn.close()

def save_author(form_entries):
    global editing_author_id
    first = form_entries["First Name"].get().strip()
    last = form_entries["Last Name"].get().strip()
    bio = form_entries["Biography"].get("1.0", tk.END).strip()
    
    if not first and not last:
        messagebox.showwarning("Warning", "Please enter at least a name!")
        return
    
    fullname = f"{last}, {first}" if last and first else (last or first)
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        
        if editing_author_id:
            cur.execute("""
                UPDATE authors 
                SET Author_Fullname=%s, Author_Biography=%s
                WHERE Author_ID=%s
            """, (fullname, bio, editing_author_id))
            messagebox.showinfo("Success", "Author updated!")
        else:
            cur.execute("""
                INSERT INTO authors (Author_Fullname, Author_Biography)
                VALUES (%s, %s)
            """, (fullname, bio))
            messagebox.showinfo("Success", "Author added!")
        
        conn.commit()
        show_authors_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Save failed:\n{e}")
    finally:
        conn.close()

def view_selected_author():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Select an author first!")
        return
    
    author = authors_data[selected_author_index]
    messagebox.showinfo(
        "Author Details",
        f"ID: {author[0]}\n"
        f"Full Name: {author[1]}\n"
        f"Biography:\n{author[2] or '—'}\n"
        f"Books Linked: {author[3]}"
    )

def delete_selected_author():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Select an author first!")
        return
    
    if not messagebox.askyesno("Confirm Delete", "Delete this author? Books linked to them may be affected!"):
        return
    
    author_id = authors_data[selected_author_index][0]
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM authors WHERE Author_ID = %s", (author_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Author removed successfully!")
        show_authors_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed:\n{e}")
    finally:
        conn.close()

def clear_form():
    if hasattr(show_authors_screen, '_form_entries'):
        for label, field in show_authors_screen._form_entries.items():
            if label == "Biography":
                field.delete("1.0", tk.END)
            else:
                field.delete(0, tk.END)
    global selected_author_index
    selected_author_index = -1

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()