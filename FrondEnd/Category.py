import tkinter as tk
from tkinter import messagebox
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

categories_data = []
selected_category_index = -1
editing_category_id = None

# ==================================================
# CATEGORIES LIST
# ==================================================
def show_categories_screen():
    global selected_category_index, categories_data
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)

    # ========= TOP BAR =========
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="CATEGORIES LIST", 
             font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="DELETE", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=delete_selected_category).pack(side="right", padx=3)
    tk.Button(top_bar, text="EDIT", bg=BTN_BROWN, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_edit_category_form).pack(side="right", padx=3)
    tk.Button(top_bar, text="VIEW", bg=BTN_YELLOW, fg="#000", width=10, font=FONT,
              relief="solid", borderwidth=1, command=view_selected_category).pack(side="right", padx=3)
    tk.Button(top_bar, text="+ Add Category", bg=BTN_GREEN, fg=TEXT_DARK, width=14,
              relief="solid", borderwidth=1, command=show_add_category_form).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5)

    # Search
    search_frame = tk.Frame(frame, bg=BG_CONTENT, padx=15, pady=8, relief="solid", borderwidth=1)
    search_frame.pack(fill="x", padx=15, pady=(10, 5))
    
    tk.Label(search_frame, text="Search:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=(0, 10))
    search_entry = tk.Entry(search_frame, width=40, font=FONT)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", lambda e: filter_categories(search_entry.get()))

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
    tk.Label(header, text="CATEGORY NAME", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=45, anchor="w").pack(side="left", padx=5)
    tk.Label(header, text="BOOKS IN CATEGORY", font=FONT_TITLE, bg="#d4b86a", fg=TEXT_DARK,
             width=18, anchor="e").pack(side="right", padx=10)
    
    tk.Frame(rows_container, bg="#7B2CBF", height=2).pack(fill="x", pady=8)
    
    load_categories_from_db()
    render_categories_list(categories_data, rows_container)

# ==================================================
# RENDER LIST
# ==================================================
def render_categories_list(data_list, parent_frame=None):
    global selected_category_index
    # Clear rows
    for w in parent_frame.winfo_children():
        if w.cget("bg") not in ["#d4b86a", "#7B2CBF"]:
            w.destroy()
    
    if not data_list:
        tk.Label(parent_frame, text="No categories found.", font=FONT, bg=BG_CARD, fg=TEXT_DARK).pack(pady=50)
        return
    
    for idx, cat in enumerate(data_list):
        cat_id, name, book_count = cat
        
        row = tk.Frame(parent_frame, bg=BG_CARD, pady=8, cursor="hand2")
        row.pack(fill="x")
        
        def make_select(i=idx, r=row):
            def select_this():
                global selected_category_index
                selected_category_index = i
                for w in parent_frame.winfo_children():
                    if isinstance(w, tk.Frame) and w.cget("cursor") == "hand2":
                        w.configure(bg=BG_CARD)
                r.configure(bg="#e5d9b6")
            return select_this
        row.bind("<Button-1>", lambda e, f=make_select(idx): f())
        
        # ID
        tk.Label(row, text=str(cat_id), font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=6, anchor="w").pack(side="left", padx=5)
        # Category Name
        tk.Label(row, text=name or "", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=45, anchor="w").pack(side="left", padx=5)
        # Books Count
        tk.Label(row, text=f"{book_count} Books", font=FONT, bg=row.cget("bg"), fg=TEXT_DARK,
                 width=18, anchor="e").pack(side="right", padx=10)

def filter_categories(search_text):
    search_text = search_text.strip().lower()
    filtered = categories_data
    if search_text:
        filtered = [c for c in categories_data if search_text in str(c[1]).lower()]
    
    for w in root.winfo_children():
        if isinstance(w, tk.Frame) and w.cget("bg") == BG_MAIN:
            for child in w.winfo_children():
                if isinstance(child, tk.Frame) and child.cget("bg") == BG_CARD:
                    for c in child.winfo_children():
                        if isinstance(c, tk.Canvas):
                            for win in c.winfo_children():
                                if isinstance(win, tk.Frame):
                                    render_categories_list(filtered, win)
                                    return

# ==================================================
# ADD / EDIT CATEGORY
# ==================================================
def show_add_category_form():
    global editing_category_id
    editing_category_id = None
    show_category_form_screen()

def show_edit_category_form():
    global selected_category_index, editing_category_id
    if selected_category_index < 0 or selected_category_index >= len(categories_data):
        messagebox.showwarning("Warning", "Select a category first!")
        return
    cat = categories_data[selected_category_index]
    editing_category_id = cat[0]
    show_category_form_screen(category_data=cat)

def show_category_form_screen(category_data=None):
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    page_title = "Edit Category" if editing_category_id else "Add Category"
    tk.Label(top_bar, text=page_title, font=FONT_TITLE, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_categories_screen).pack(side="right", padx=5)
    
    form_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    form_container.pack(pady=50)
    
    tk.Label(form_container, text="ADD / EDIT CATEGORY", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
    
    tk.Label(form_container, text="Category Name:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    name_entry = tk.Entry(form_container, font=FONT, width=40)
    name_entry.pack(fill="x")
    
    if category_data:
        name_entry.insert(0, category_data[1] or "")
    
    btn_frame = tk.Frame(form_container, bg=BG_CARD)
    btn_frame.pack(pady=(25, 0))
    
    def save_wrapper():
        save_category(name_entry.get().strip())
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, width=12, font=FONT,
              relief="solid", borderwidth=1, command=save_wrapper).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", width=12, font=FONT,
              relief="solid", borderwidth=1, command=show_categories_screen).pack(side="left", padx=10)

# ==================================================
# VIEW CATEGORY
# ==================================================
def view_selected_category():
    global selected_category_index
    if selected_category_index < 0 or selected_category_index >= len(categories_data):
        messagebox.showwarning("Warning", "Select a category first!")
        return
    cat = categories_data[selected_category_index]
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    top_bar = tk.Frame(frame, bg=BG_CARD, padx=15, pady=10)
    top_bar.pack(fill="x")
    
    tk.Label(top_bar, text="VIEW CATEGORY", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="BACK", bg=BTN_YELLOW, fg="#000", width=10,
              relief="solid", borderwidth=1, command=show_categories_screen).pack(side="right", padx=5)
    
    view_container = tk.Frame(frame, bg=BG_CARD, padx=30, pady=30, relief="solid", borderwidth=1)
    view_container.pack(pady=50)
    
    def make_view_field(label_text, value):
        tk.Label(view_container, text=label_text, font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(8, 2))
        entry = tk.Entry(view_container, font=FONT, width=40)
        entry.insert(0, value or "")
        entry.configure(state="readonly")
        entry.pack(fill="x")
    
    make_view_field("ID:", str(cat[0]))
    make_view_field("CATEGORY NAME:", cat[1] or "")
    make_view_field("BOOKS IN CATEGORY:", f"{cat[2]} Books")

# ==================================================
# DELETE CATEGORY
# ==================================================
def delete_selected_category():
    global selected_category_index
    if selected_category_index < 0 or selected_category_index >= len(categories_data):
        messagebox.showwarning("Warning", "Select a category first!")
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    delete_container = tk.Frame(frame, bg=BG_CARD, padx=40, pady=30, relief="solid", borderwidth=1)
    delete_container.pack(pady=100)
    
    tk.Label(delete_container, text="DELETE CATEGORY", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(pady=(0, 20))
    tk.Label(delete_container, text="ARE YOU SURE YOU WANT TO\nDELETE THIS CATEGORY?", 
             font=FONT, bg=BG_CARD, fg=TEXT_DARK, justify="center").pack(pady=(0, 25))
    
    btn_frame = tk.Frame(delete_container, bg=BG_CARD)
    btn_frame.pack()
    
    def confirm_delete():
        cat_id = categories_data[selected_category_index][0]
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM categories WHERE Category_ID = %s", (cat_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Category removed!")
                show_categories_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed:\n{e}")
            finally:
                conn.close()
    
    tk.Button(btn_frame, text="YES", bg=BTN_GREEN, fg=TEXT_DARK, width=10, font=FONT,
              relief="solid", borderwidth=1, command=confirm_delete).pack(side="left", padx=15)
    tk.Button(btn_frame, text="NO", bg=BTN_RED, fg="white", width=10, font=FONT,
              relief="solid", borderwidth=1, command=show_categories_screen).pack(side="left", padx=15)

# ==================================================
# DATABASE FUNCTIONS
# ==================================================
def load_categories_from_db():
    global categories_data, selected_category_index
    categories_data = []
    selected_category_index = -1
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.Category_ID, c.Category_Name,
                   COUNT(b.Book_ID) as Book_Count
            FROM categories c
            LEFT JOIN books b ON c.Category_ID = b.Category_ID
            GROUP BY c.Category_ID
            ORDER BY c.Category_ID
        """)
        categories_data = cur.fetchall()
        print(f"✅ Loaded {len(categories_data)} categories")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load categories:\n{e}")
    finally:
        conn.close()

def save_category(name):
    global editing_category_id
    if not name:
        messagebox.showwarning("Warning", "Category name is required!")
        return
    
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        
        if editing_category_id:
            cur.execute("""
                UPDATE categories 
                SET Category_Name=%s
                WHERE Category_ID=%s
            """, (name, editing_category_id))
            messagebox.showinfo("Success", "Category updated!")
        else:
            cur.execute("""
                INSERT INTO categories (Category_Name)
                VALUES (%s)
            """, (name,))
            messagebox.showinfo("Success", "Category added!")
        
        conn.commit()
        show_categories_screen()
    except Exception as e:
        messagebox.showerror("Error", f"Save failed:\n{e}")
    finally:
        conn.close()

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()