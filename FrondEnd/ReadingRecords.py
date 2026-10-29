import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
show_navigation_dashboard = Main.show_navigation_dashboard
current_user = Main.current_user

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

records_data = []
status_filter = "ALL"

# ==================================================
# 1. MAIN SCREEN — FIRST so other functions can call it
# ==================================================
def show_reading_records_screen():
    global records_data, status_filter
    # ✅ Admin only protection
    if not current_user.get("is_admin", False):
        messagebox.showwarning("Access Denied", "Only Admin can access Reading Records!")
        show_navigation_dashboard()
        return

    clear_all()

    # Top Header
    top_frame = tk.Frame(root, bg=BG_CONTENT, relief="solid", borderwidth=1)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="ADMIN READING STATUS & RECORDS – (BORROWING BOOKS)",
             font=FONT_HEADING, bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left", padx=20, pady=12)

    tk.Button(top_frame, text="+ Add Books", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, command=add_borrow_book).pack(side="right", padx=5, pady=10)

    tk.Button(top_frame, text="BACK", bg=BTN_YELLOW, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, command=go_back).pack(side="right", padx=5, pady=10)

    # Search & Filter Bar
    filter_frame = tk.Frame(root, bg=BG_MAIN, padx=10, pady=10)
    filter_frame.pack(fill="x")

    tk.Label(filter_frame, text="Search:", font=FONT, bg=BG_MAIN, fg=TEXT_DARK).grid(row=0, column=0, padx=5, sticky="w")
    search_entry = tk.Entry(filter_frame, width=25, font=FONT)
    search_entry.grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Status List:", font=FONT, bg=BG_MAIN, fg=TEXT_DARK).grid(row=0, column=2, padx=15, sticky="w")
    status_options = ["ALL", "Reading", "Completed", "PENDING APPROVAL"]
    status_var = tk.StringVar(value=status_filter)
    status_menu = ttk.Combobox(filter_frame, textvariable=status_var, values=status_options,
                                state="readonly", width=20, font=FONT)
    status_menu.grid(row=0, column=3, padx=5)
    status_menu.bind("<<ComboboxSelected>>", lambda e: apply_status_filter(status_var.get()))

    tk.Button(filter_frame, text="FILTER", bg=BTN_BROWN, fg="white",
              font=FONT, relief="solid", borderwidth=1,
              command=lambda: search_records(search_entry.get())).grid(row=0, column=4, padx=10)

    tk.Button(filter_frame, text="VIEW", bg=BTN_YELLOW, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1,
              command=view_selected).grid(row=0, column=5, padx=5)

    # Table Frame
    table_frame = tk.Frame(root, bg=BG_CARD, padx=10, pady=10)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "USER NAME", "BOOK TITLE", "STATUS", "DATE STARTED")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    tree.heading("ID", text="ID")
    tree.heading("USER NAME", text="USER NAME")
    tree.heading("BOOK TITLE", text="BOOK TITLE")
    tree.heading("STATUS", text="STATUS")
    tree.heading("DATE STARTED", text="DATE STARTED")

    tree.column("ID", width=50, anchor="center")
    tree.column("USER NAME", width=150, anchor="w")
    tree.column("BOOK TITLE", width=250, anchor="w")
    tree.column("STATUS", width=150, anchor="center")
    tree.column("DATE STARTED", width=150, anchor="center")

    tree.pack(fill="both", expand=True)
    load_records(tree)

# ==================================================
# 2. LOAD RECORDS
# ==================================================
def load_records(tree=None):
    global records_data, status_filter
    if tree is None:
        for widget in root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Treeview):
                        tree = child
                        break

    if not tree:
        return

    for item in tree.get_children():
        tree.delete(item)

    conn = get_db_connection()
    if not conn:
        return

    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT br.Record_ID as id,
                   u.Username as user_name,
                   b.Book_Title as book_title,
                   br.Reading_Status as status,
                   br.Borrow_Date as date_started
            FROM borrow_records br
            LEFT JOIN User u ON br.User_ID = u.User_ID
            LEFT JOIN books b ON br.Book_ID = b.Book_ID
        """
        params = []
        if status_filter != "ALL":
            query += " WHERE br.Reading_Status = %s"
            params = [status_filter]
        query += " ORDER BY br.Borrow_Date DESC"
        cur.execute(query, params)
        records_data = cur.fetchall()

        for rec in records_data:
            status_display = rec["status"] or "PENDING APPROVAL"
            date_str = rec["date_started"].strftime("%Y-%m-%d") if rec["date_started"] else ""
            item_id = tree.insert("", "end", values=(rec["id"], rec["user_name"], rec["book_title"], status_display, date_str))
            if status_display == "PENDING APPROVAL":
                tree.tag_configure("pending", background="#fff9c4")
                tree.item(item_id, tags=("pending",))
            elif status_display == "Reading":
                tree.tag_configure("reading", background="#e8f5e9")
                tree.item(item_id, tags=("reading",))
            elif status_display == "Completed":
                tree.tag_configure("completed", background="#e3f2fd")
                tree.item(item_id, tags=("completed",))
        conn.close()
    except Exception as e:
        messagebox.showerror("Load Error", f"Cannot load records:\n{e}")
        conn.close()

# ==================================================
# 3. FILTER & SEARCH
# ==================================================
def apply_status_filter(selected_status):
    global status_filter
    status_filter = selected_status
    load_records()

def search_records(keyword):
    global records_data, status_filter
    keyword = keyword.strip().lower()
    tree = None
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Treeview):
                    tree = child
                    break
    if not tree:
        return
    for item in tree.get_children():
        tree.delete(item)
    for rec in records_data:
        match = (keyword == "" or keyword in str(rec["user_name"] or "").lower() or keyword in str(rec["book_title"] or "").lower())
        status_match = (status_filter == "ALL" or rec["status"] == status_filter)
        if match and status_match:
            status_display = rec["status"] or "PENDING APPROVAL"
            date_str = rec["date_started"].strftime("%Y-%m-%d") if rec["date_started"] else ""
            tree.insert("", "end", values=(rec["id"], rec["user_name"], rec["book_title"], status_display, date_str))

# ==================================================
# 4. ADD BORROW FORM
# ==================================================
def add_borrow_book():
    if not current_user.get("is_admin", False):
        messagebox.showwarning("Access Denied", "Only Admin can add records!")
        show_reading_records_screen()
        return

    clear_all()
    form_frame = tk.Frame(root, bg=BG_MAIN, padx=20, pady=20)
    form_frame.pack(fill="both", expand=True)

    header_frame = tk.Frame(form_frame, bg=BG_CARD, relief="solid", borderwidth=1)
    header_frame.pack(fill="x", pady=(0, 15))
    tk.Label(header_frame, text="ADD BOOKS & RECORD", font=FONT_HEADING, bg=BG_CARD, fg=TEXT_DARK).pack(side="left", padx=20, pady=15)
    tk.Button(header_frame, text="BACK", bg=BTN_YELLOW, fg=TEXT_DARK, font=FONT, relief="solid", borderwidth=1,
              command=show_reading_records_screen).pack(side="right", padx=15, pady=15)

    card = tk.Frame(form_frame, bg=BG_CARD, relief="solid", borderwidth=1, padx=30, pady=20)
    card.pack()

    tk.Label(card, text="Select Book:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=0, column=0, sticky="w", pady=8)
    book_conn = get_db_connection()
    book_titles = []
    if book_conn:
        try:
            cur = book_conn.cursor()
            cur.execute("SELECT Book_Title FROM books ORDER BY Book_Title")
            book_titles = [row[0] for row in cur.fetchall()]
            book_conn.close()
        except: pass
    book_var = tk.StringVar()
    book_menu = ttk.Combobox(card, textvariable=book_var, values=book_titles, state="readonly", width=35, font=FONT)
    book_menu.grid(row=0, column=1, pady=8, padx=10)

    tk.Label(card, text="Status:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=1, column=0, sticky="w", pady=8)
    status_var = tk.StringVar(value="PENDING APPROVAL")
    status_menu = ttk.Combobox(card, textvariable=status_var, values=["PENDING APPROVAL", "Reading", "Completed"],
                                state="readonly", width=35, font=FONT)
    status_menu.grid(row=1, column=1, pady=8, padx=10)

    tk.Label(card, text="Date Started:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=2, column=0, sticky="w", pady=8)
    date_started = tk.Entry(card, width=38, font=FONT)
    date_started.insert(0, "YYYY-MM-DD")
    date_started.grid(row=2, column=1, pady=8, padx=10)

    tk.Label(card, text="Due Date:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=3, column=0, sticky="w", pady=8)
    due_date = tk.Entry(card, width=38, font=FONT)
    due_date.insert(0, "YYYY-MM-DD")
    due_date.grid(row=3, column=1, pady=8, padx=10)

    tk.Label(card, text="Borrower Name:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=4, column=0, sticky="w", pady=8)
    user_conn = get_db_connection()
    user_names = []
    if user_conn:
        try:
            cur = user_conn.cursor()
            cur.execute("SELECT Username FROM User ORDER BY Username")
            user_names = [row[0] for row in cur.fetchall()]
            user_conn.close()
        except: pass
    user_var = tk.StringVar()
    user_menu = ttk.Combobox(card, textvariable=user_var, values=user_names, state="readonly", width=35, font=FONT)
    user_menu.grid(row=4, column=1, pady=8, padx=10)

    tk.Label(card, text="Notes:", font=FONT, bg=BG_CARD, fg=TEXT_DARK, anchor="w").grid(row=5, column=0, sticky="w", pady=8)
    notes_entry = tk.Entry(card, width=38, font=FONT)
    notes_entry.grid(row=5, column=1, pady=8, padx=10)

    btn_frame = tk.Frame(card, bg=BG_CARD)
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

    def save_record():
        selected_book = book_var.get()
        selected_user = user_var.get()
        status = status_var.get()
        s_date = date_started.get()
        d_date = due_date.get()
        if not selected_book or not selected_user:
            messagebox.showwarning("Warning", "Select Book and Borrower!")
            return
        conn = get_db_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT Book_ID FROM books WHERE Book_Title = %s", (selected_book,))
            book_id = cur.fetchone()[0]
            cur.execute("SELECT User_ID FROM User WHERE Username = %s", (selected_user,))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO borrow_records (User_ID, Book_ID, Borrow_Date, Due_Date, Reading_Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, book_id, s_date if s_date != "YYYY-MM-DD" else None,
                  d_date if d_date != "YYYY-MM-DD" else None, status))
            conn.commit()
            messagebox.showinfo("Saved", "Borrow record added successfully!")
            show_reading_records_screen()
        except Exception as e:
            messagebox.showerror("Save Error", f"Cannot save:\n{e}")
        finally:
            conn.close()

    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK, font=FONT, relief="solid", borderwidth=1,
              command=save_record).pack(side="left", padx=10)
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white", font=FONT, relief="solid", borderwidth=1,
              command=show_reading_records_screen).pack(side="left", padx=10)

# ==================================================
# 5. VIEW SELECTED
# ==================================================
def view_selected():
    global records_data
    tree = None
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Treeview):
                    tree = child
                    break
    if not tree:
        messagebox.showwarning("Warning", "Cannot find records table!")
        return
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a record row first!")
        return
    item = tree.item(selected[0])
    values = item["values"]
    detail_text = f"""RECORD DETAILS

ID: {values[0]}
User Name: {values[1]}
Book Title: {values[2]}
Status: {values[3]}
Date Started: {values[4]}
"""
    record_id = values[0]
    status = values[3]
    if status == "PENDING APPROVAL":
        result = messagebox.askyesnocancel("PENDING APPROVAL", f"{detail_text}\nYES = Approve | NO = Reject | Cancel = Close")
        if result is True:
            approve_borrow(record_id)
        elif result is False:
            reject_borrow(record_id)
    else:
        messagebox.showinfo("Record Details", detail_text)

# ==================================================
# 6. NAVIGATION
# ==================================================
def go_back():
    show_navigation_dashboard()

# ==================================================
# 7. APPROVE / REJECT — ADMIN ONLY
# ==================================================
def approve_borrow(record_id):
    if not current_user.get("is_admin", False):
        messagebox.showwarning("Access Denied", "Only Admin can approve requests!")
        return
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE borrow_records SET Reading_Status = 'Reading' WHERE Record_ID = %s", (record_id,))
        conn.commit()
        messagebox.showinfo("Approved", "Borrow request approved!")
        load_records()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot approve:\n{e}")
    finally:
        conn.close()

def reject_borrow(record_id):
    if not current_user.get("is_admin", False):
        messagebox.showwarning("Access Denied", "Only Admin can reject requests!")
        return
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE borrow_records SET Reading_Status = 'Rejected' WHERE Record_ID = %s", (record_id,))
        conn.commit()
        messagebox.showinfo("Rejected", "Borrow request rejected!")
        load_records()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot reject:\n{e}")
    finally:
        conn.close()