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

authors_data = []
selected_author_index = -1
editing_author_id = None

# ==================================================
# AUTHORS LIST
# ==================================================
def show_authors_screen():
    global selected_author_index, authors_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # ========= TOP BAR =========
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="AUTHORS LIST", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="DELETE", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_author).pack(side="right", padx=3)
    tk.Button(top_bar, text="EDIT", bg=BTN_BROWN, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_author_form).pack(side="right", padx=3)
    tk.Button(top_bar, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_author).pack(side="right", padx=3)
    tk.Button(top_bar, text="+ Add Author", bg=BTN_GREEN, fg=TEXT_DARK, width=14,
              relief="solid", borderwidth=1, command=show_add_author_form).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)

    # Search
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", lambda e: filter_authors(search_entry.get()))

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
             width=6, anchor="w").pack(side="left", padx=5)
    tk.Label(header, text="FULL NAME", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=25, anchor="w").pack(side="left", padx=5)
    tk.Label(header, text="BIOGRAPHY", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=35, anchor="w").pack(side="left", padx=5)
    tk.Label(header, text="BOOK COUNT", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=12, anchor="e").pack(side="right", padx=10)
    
    tk.Frame(rows_container, bg="#7B2CBF", height=2).pack(fill="x", pady=8)
    
    load_authors_from_db()
    render_authors_list(authors_data, rows_container)

# ==================================================
# RENDER LIST
# ==================================================
def render_authors_list(data_list, parent_frame=None):
    global selected_author_index
    # Clear rows
    for w in parent_frame.winfo_children():
        if w.cget("bg") not in ["#d4b86a", "#7B2CBF"]:
            w.destroy()
    
    if not data_list:
        tk.Label(parent_frame, text="No authors found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
        return
    
    for idx, author in enumerate(data_list):
        author_id, fullname, bio, book_count = author
        
        row = tk.Frame(parent_frame, bg=BG_CARD, pady=8, cursor="hand2")
        row.pack(fill="x")
        
        def make_select(i=idx, r=row):
            def select_this():
                global selected_author_index
                selected_author_index = i
                for w in parent_frame.winfo_children():
                    if isinstance(w, tk.Frame) and w.cget("cursor") == "hand2":
                        w.configure(bg=BG_CARD)
                r.configure(bg="#e5d9b6")
            return select_this
        row.bind("<Button-1>", lambda e, f=make_select(idx): f())

        # ID
        tk.Label(row, text=str(author_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=6, anchor="w").pack(side="left", padx=5)
        # Full Name
        tk.Label(row, text=fullname or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=25, anchor="w").pack(side="left", padx=5)
        # Biography
        bio_short = (bio[:30] + "...") if bio and len(bio) > 30 else (bio or "")
        tk.Label(row, text=bio_short, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=35, anchor="w").pack(side="left", padx=5)
        # Book Count
        tk.Label(row, text=f"{book_count} Books", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=12, anchor="e").pack(side="right", padx=10)

def filter_authors(search_text):
    search_text = search_text.strip().lower()
    filtered = authors_data
    if search_text:
        filtered = [a for a in authors_data if search_text in str(a[1]).lower()]
    
    for w in root.winfo_children():
        if isinstance(w, tk.Frame) and w.cget("bg") == BG_MAIN:
            for child in w.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == BG_CARD:
                    for c in child.winfo_children():
                        if isinstance(c, tk.Canvas):
                            for win in c.winfo_children():
                                if isinstance(win, tk.Frame):
                                    render_authors_list(filtered, win)
                                    return

# ==================================================
# ADD / EDIT AUTHOR
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
    form_container.pack(pady=30)
    
    tk.Label(form_container, text="ADD / EDIT AUTHOR", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    form_entries = {}
    
    tk.Label(form_container, text="First Name", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    first_entry = tk.Entry(form_container, font=FONT, width=40)
    first_entry.pack(fill="x")
    form_entries["First Name"] = first_entry
    
    tk.Label(form_container, text="Last Name", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    last_entry = tk.Entry(form_container, font=FONT, width=40)
    last_entry.pack(fill="x")
    form_entries["Last Name"] = last_entry
    
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
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=lambda: save_author(form_entries)).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="left", padx=10)
    
# ==================================================
# VIEW AUTHOR
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
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Label(top_bar, text="VIEW AUTHOR", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=show_authors_screen).pack(side="right", padx=5)
    
    view_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=2)
    view_container.pack(pady=50)

    profile_frame = tk.Frame(view_container, bg=BG_CARD)
    profile_frame.pack(anchor="w", pady=(0, 15))
    tk.Label(profile_frame, text="PROFILE\nPICTURE", font=FONT, bg="#e5d9b6", fg=TEXT_DARK,
             width=12, height=4, relief="solid", borderwidth=1).pack()
     
    def make_view_field(label_text, value):
        tk.Label(view_container, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 2))
        entry = tk.Entry(view_container, font=FONT, width=40)
        entry.insert(0, value or "")
        entry.configure(state="readonly")
        entry.pack(fill="x")
    
    make_view_field("ID:", str(author[0]))
    make_view_field("FULL NAME:", author[1] or "")
    make_view_field("BIOGRAPHY:", author[2] or "")
    make_view_field("BOOK COUNT:", f"{author[3]} Books")

# ==================================================
# DELETE AUTHOR
# ==================================================
def delete_selected_author():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Select an author first!")
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    delete_container = tk.Frame(frame, bg=BG_CARD, padx=40, pady=30, relief="solid", borderwidth=2)
    delete_container.pack(pady=120)
    
    tk.Label(delete_container, text="DELETE AUTHOR", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(pady=(0, 20))
    tk.Label(delete_container, text="ARE YOU SURE YOU WANT TO\nDELETE THIS AUTHOR?", 
             font=FONT, bg=BG_CARD, fg=TEXT_DARK, justify="center").pack(pady=(0, 25))
    
    btn_frame = tk.Frame(delete_container, bg=BG_CARD)
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

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()