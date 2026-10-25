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

def show_authors_screen():
    global form_entries, selected_author_index
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1280, height=720)
    frame.pack(fill="both", expand=True)
    
    # --- Top Bar ---
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Label(top_bar, text="ADMIN AUTHORS SCREEN – (AUTHORS Table)", font=FONT_HEADING, 
             bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="+ Add Author", bg=BTN_GREEN, fg=TEXT_DARK, width=12,
              relief="solid", borderwidth=1, command=show_add_author_form).pack(side="right", padx=5)
    tk.Button(top_bar, text="Search", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)
    
    # --- Main Content: Split into LEFT (Form) and RIGHT (List) ---
    content_pane = tk.Frame(frame, bg=BG_MAIN)
    content_pane.pack(fill="both", expand=True, padx=15, pady=10)
    
    # ========== LEFT SIDE — ADD AUTHOR FORM ==========
    form_container = tk.Frame(content_pane, bg=BG_CONTENT, padx=20, pady=20, 
                              relief="solid", borderwidth=1, width=350)
    form_container.pack(side="left", fill="y", padx=(0, 10))
    form_container.pack_propagate(False)
    
    tk.Label(form_container, text="Add Author", font=FONT_HEADING, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 5))
    tk.Label(form_container, text="ADD / EDIT AUTHOR", font=FONT_TITLE, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 15))
    
    form_entries = {}
    editing_author_id = [None]
    
    tk.Label(form_container, text="First Name", font=FONT, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(10, 0))
    e_first = tk.Entry(form_container, font=FONT)
    e_first.pack(fill="x", pady=(3, 0))
    form_entries["First Name"] = e_first
    
    tk.Label(form_container, text="Last Name", font=FONT, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(10, 0))
    e_last = tk.Entry(form_container, font=FONT)
    e_last.pack(fill="x", pady=(3, 0))
    form_entries["Last Name"] = e_last
    
    tk.Label(form_container, text="Biography", font=FONT, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(10, 0))
    bio_text = tk.Text(form_container, font=FONT, height=5, wrap="word")
    bio_text.pack(fill="x", pady=(3, 0))
    form_entries["Biography"] = bio_text
    
    # --- Save / Cancel Buttons ---
    btn_frame = tk.Frame(form_container, bg=BG_CONTENT)
    btn_frame.pack(fill="x", pady=(25, 0))
    
    def save_wrapper():
        save_author(editing_author_id[0])
        editing_author_id[0] = None
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=5)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=clear_form).pack(side="left", padx=5)
    
    show_authors_screen._editing_ref = editing_author_id
    show_authors_screen._form_entries = form_entries
    
    # ========== RIGHT SIDE — AUTHORS LIST ==========
    list_frame = tk.Frame(content_pane, bg=BG_CONTENT, padx=15, pady=15, relief="solid", borderwidth=1)
    list_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    tk.Label(list_frame, text="AUTHORS LIST", font=FONT_TITLE, 
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
    
    header = tk.Frame(list_frame, bg="#d4b86a", padx=5, pady=8)
    header.pack(fill="x")
    cols = [("ID", 5), ("FULL NAME", 25), ("BIOGRAPHY", 35), ("BOOK COUNT", 12)]
    for col_name, width in cols:
        tk.Label(header, text=col_name, font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
                 width=width, anchor="w").pack(side="left", padx=2)
    
    tk.Frame(list_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=5)
    
    # --- Load Authors from Database ---
    load_authors_from_db()
    
    # --- Author Rows ---
    rows_container = tk.Frame(list_frame, bg=BG_CONTENT)
    rows_container.pack(fill="both", expand=True)
    
    if not authors_data:
        tk.Label(rows_container, text="No authors found.", font=FONT, 
                 bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=15)
    else:
        for idx, row_data in enumerate(authors_data):
            author_id, fullname, bio, book_count = row_data
            row = tk.Frame(rows_container, bg=BG_CONTENT, pady=6, cursor="hand2")
            row.pack(fill="x")
            
            def make_select(i=idx, r=row):
                def select_this():
                    global selected_author_index
                    selected_author_index = i
                    for w in rows_container.winfo_children():
                        w.configure(bg=BG_CONTENT)
                    r.configure(bg="#e5d9b6")
                return select_this
            row.bind("<Button-1>", lambda e, f=make_select(idx): f())
            
            tk.Label(row, text=str(author_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, 
                     width=5, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=fullname or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, 
                     width=25, anchor="w").pack(side="left", padx=2)
            bio_short = (bio[:30] + "...") if bio and len(bio) > 30 else (bio or "")
            tk.Label(row, text=bio_short, font=FONT, bg=row.cget("bg"), fg=TEXT_DARK, 
                     width=35, anchor="w").pack(side="left", padx=2)
            tk.Label(row, text=str(book_count), font=FONT, bg=row.cget("bg"), 
                     fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=2)
    
    # --- Action Buttons under List ---
    list_btn_frame = tk.Frame(list_frame, bg=BG_CONTENT)
    list_btn_frame.pack(fill="x", pady=(15, 0))
    tk.Button(list_btn_frame, text="VIEW", bg=BTN_YELLOW, fg="#000", width=12, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_author).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="EDIT", bg=BTN_BROWN, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_author_form).pack(side="right", padx=5)
    tk.Button(list_btn_frame, text="DELETE", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_author).pack(side="right", padx=5)

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
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load authors:\n{e}")
    finally:
        conn.close()

def show_add_author_form():
    clear_form()
    if hasattr(show_authors_screen, '_editing_ref'):
        show_authors_screen._editing_ref[0] = None

def show_edit_author_form():
    global selected_author_index
    if selected_author_index < 0 or selected_author_index >= len(authors_data):
        messagebox.showwarning("Warning", "Please select an author first!")
        return
    
    author = authors_data[selected_author_index]
    
    if not hasattr(show_authors_screen, '_form_entries'):
        return
    
    form_entries = show_authors_screen._form_entries
    show_authors_screen._editing_ref[0] = author[0]
    
    # Split "Last, First" format
    name_parts = (author[1] or "").split(", ", 1)
    if len(name_parts) == 2:
        last, first = name_parts
    else:
        first = author[1] or ""
        last = ""
    
    form_entries["First Name"].delete(0, tk.END)
    form_entries["First Name"].insert(0, first.strip())
    
    form_entries["Last Name"].delete(0, tk.END)
    form_entries["Last Name"].insert(0, last.strip())
    
    form_entries["Biography"].delete("1.0", tk.END)
    form_entries["Biography"].insert("1.0", author[2] or "")

def save_author(edit_id=None):
    if not hasattr(show_authors_screen, '_form_entries'):
        return
    
    form_entries = show_authors_screen._form_entries
    
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
        
        if edit_id:
            cur.execute("""
                UPDATE authors 
                SET Author_Fullname=%s, Author_Biography=%s
                WHERE Author_ID=%s
            """, (fullname, bio, edit_id))
            messagebox.showinfo("Success", "Author updated successfully!")
        else:
            cur.execute("""
                INSERT INTO authors (Author_Fullname, Author_Biography)
                VALUES (%s, %s)
            """, (fullname, bio))
            messagebox.showinfo("Success", "Author added successfully!")
        
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