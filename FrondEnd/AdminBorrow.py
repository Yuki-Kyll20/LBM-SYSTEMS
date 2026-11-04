import tkinter as tk
from tkinter import messagebox, ttk
import Main
import calendar
from datetime import datetime

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

borrow_data = []
rows_container_ref = None

# ========== DATE PICKER COMPONENT ==========
class DatePicker:
    """Simple calendar-style date picker"""
    def __init__(self, parent, default_text="YYYY-MM-DD", width=48):
        self.frame = tk.Frame(parent, bg="#f7e797")
        self.entry = tk.Entry(self.frame, font=FONT, width=width)
        self.entry.insert(0, default_text)
        self.entry.pack(side="left", padx=(0, 5))
        
        self.calendar_btn = tk.Button(
            self.frame, text="📅", bg=BTN_BROWN, fg="white",
            relief="solid", borderwidth=1, command=self.show_calendar
        )
        self.calendar_btn.pack(side="left")
        
        self.cal_window = None
        self.selected_date = None

    def show_calendar(self):
        if self.cal_window and self.cal_window.winfo_exists():
            self.cal_window.lift()
            return
        
        self.cal_window = tk.Toplevel(root)
        self.cal_window.title("Select Date")
        self.cal_window.geometry("300x280")
        self.cal_window.configure(bg="#f7e797")
        self.cal_window.transient(root)
        self.cal_window.grab_set()
        
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month

        # Navigation
        nav_frame = tk.Frame(self.cal_window, bg="#e8d590", pady=5)
        nav_frame.pack(fill="x")
        
        tk.Button(nav_frame, text="<", command=self.prev_month,
                  bg=BTN_BROWN, fg="white", width=3).pack(side="left", padx=5)
        self.month_label = tk.Label(nav_frame, text="", font=FONT_TITLE, bg="#e8d590")
        self.month_label.pack(side="left", expand=True)
        tk.Button(nav_frame, text=">", command=self.next_month,
                  bg=BTN_BROWN, fg="white", width=3).pack(side="right", padx=5)
        
        days_frame = tk.Frame(self.cal_window, bg="#f7e797", pady=5)
        days_frame.pack()
        for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            tk.Label(days_frame, text=day, font=FONT, bg="#e8d590", width=5).grid(row=0, column=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].index(day))
        
        self.dates_frame = tk.Frame(self.cal_window, bg="#f7e797")
        self.dates_frame.pack(pady=5)
        
        self.update_calendar()

    def update_calendar(self):
        for widget in self.dates_frame.winfo_children():
            widget.destroy()
        
        month_name = datetime(self.current_year, self.current_month, 1).strftime("%B %Y")
        self.month_label.config(text=month_name)
        
        first_day = datetime(self.current_year, self.current_month, 1)
        start_weekday = first_day.weekday()
        start_weekday = (start_weekday + 1) % 7
        
        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]

        row = 1
        for i in range(start_weekday):
            tk.Label(self.dates_frame, text="", width=5, bg="#f7e797").grid(row=row, column=i)
        
        for day in range(1, days_in_month + 1):
            col = (start_weekday + day - 1) % 7
            if col == 0 and day > 1:
                row += 1
            
            btn = tk.Button(
                self.dates_frame, text=str(day), width=5,
                bg=BG_CONTENT, fg=TEXT_DARK, relief="solid", borderwidth=1,
                command=lambda d=day: self.select_date(d)
            )
            btn.grid(row=row, column=col, pady=2)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def select_date(self, day):
        self.selected_date = datetime(self.current_year, self.current_month, day)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.selected_date.strftime("%Y-%m-%d"))
        if self.cal_window:
            self.cal_window.destroy()

    def get(self):
        val = self.entry.get().strip()
        if val in ["YYYY-MM-DD", ""]:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except ValueError as err:
            raise ValueError("Enter a valid date in YYYY-MM-DD format.") from err

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

# ==================================================
# ADMIN READING STATUS & RECORDS
# ==================================================
def show_admin_borrow_screen():
    username = Main.current_user.get("username", "")
    
    # ✅ SAME CHECK EVERYWHERE
    is_admin = Main.current_user.get("is_admin", False)
    
    print(f"AdminBorrow — is_admin = {is_admin} | User = {username}")
    
    if not is_admin:
        messagebox.showerror(
            "Access Denied",
            f"Only Admin can access Reading Records!\n\n"
            f"Username: {username}"
        )
        Main.show_navigation_dashboard()
        return
    
    clear_all()
    
    frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    # ========= HEADER BAR =========
    header_frame = tk.Frame(frame, bg="#f7e797", padx=15, pady=12, relief="solid", borderwidth=2)
    header_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Label(header_frame, text="ADMIN READING STATUS & RECORDS – (BORROWING BOOKS)", 
             font=FONT_HEADING, bg="#f7e797", fg=TEXT_DARK).pack(side="left")
    
    tk.Button(header_frame, text="+ Add Books", bg=BTN_GREEN, fg="white", width=12,
              relief="solid", borderwidth=1, command=add_borrow_book).pack(side="right", padx=5)
    
    tk.Button(header_frame, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=go_back).pack(side="right")
    
    # ========= SEARCH & FILTER BAR =========
    filter_frame = tk.Frame(frame, bg=BG_MAIN, pady=10)
    filter_frame.pack(fill="x", padx=20)
    
    tk.Label(filter_frame, text="Search:", font=FONT, bg=BG_MAIN, fg=TEXT_DARK).pack(side="left", padx=5)
    search_entry = tk.Entry(filter_frame, font=FONT, width=25)
    search_entry.pack(side="left", padx=5)
    search_entry.bind("<KeyRelease>", lambda e: filter_records(search_entry.get(), status_combo.get()))
    
    tk.Label(filter_frame, text="Status List:", font=FONT, bg=BG_MAIN, fg=TEXT_DARK).pack(side="left", padx=(20,5))
    status_combo = ttk.Combobox(filter_frame, 
        values=["ALL", "Unread", "Reading", "Completed", "On Hold", "Dropped", "Pending"], 
        font=FONT, width=18, state="readonly")
    status_combo.set("ALL")
    status_combo.pack(side="left", padx=5)
    status_combo.bind("<<ComboboxSelected>>", lambda e: filter_records(search_entry.get(), status_combo.get()))
    
    # ========= TABLE =========
    table_frame = tk.Frame(frame, bg="#f7e797", padx=15, pady=15, relief="solid", borderwidth=2)
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    header_row = tk.Frame(table_frame, bg="#e8d590", pady=8)
    header_row.pack(fill="x")
    
    tk.Label(header_row, text="ID", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=5, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="USER NAME", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=12, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="BOOK TITLE", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=25, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="STATUS", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=12, anchor="center").pack(side="left", padx=5)
    tk.Label(header_row, text="DATE STARTED", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=12, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="DATE FINISHED", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=12, anchor="w").pack(side="left", padx=5)
    tk.Label(header_row, text="ACTIONS", font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK,
             width=15, anchor="center").pack(side="right", padx=5)
    
    tk.Frame(table_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=5)
    
    # ========= SCROLLABLE LIST =========
    list_container = tk.Frame(table_frame, bg="#f7e797")
    list_container.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(list_container, bg="#f7e797", highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    rows_container = tk.Frame(canvas, bg="#f7e797")
    
    rows_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=rows_container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    load_borrow_from_db()
    render_borrow_rows(rows_container)
    
    global rows_container_ref
    rows_container_ref = rows_container

def get_status_color(status):
    colors = {
        "Unread": "#D3D3D3",
        "Pending": BTN_YELLOW,
        "Reading": "#90EE90",
        "Completed": BTN_GREEN,
        "On Hold": "#FFB347",
        "Dropped": BTN_RED
    }
    return colors.get(status, BG_CONTENT)

def render_borrow_rows(parent_frame, filtered_list=None):
    for w in parent_frame.winfo_children():
        w.destroy()
    
    display_data = filtered_list if filtered_list is not None else borrow_data
    
    if not display_data:
        tk.Label(parent_frame, text="No records found.", font=FONT, bg="#f7e797", fg=TEXT_DARK).pack(pady=30)
        return
    
    for idx, item in enumerate(display_data, 1):
        rec_id, username, book_title, status, date_started, date_finished = item
        
        row = tk.Frame(parent_frame, bg="#f7e797", pady=6)
        row.pack(fill="x")
        
        tk.Label(row, text=str(idx), font=FONT, bg="#f7e797", fg=TEXT_DARK, width=5, anchor="w").pack(side="left", padx=5)
        tk.Label(row, text=username or "", font=FONT, bg="#f7e797", fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=5)
        tk.Label(row, text=book_title or "", font=FONT, bg="#f7e797", fg=TEXT_DARK, width=25, anchor="w").pack(side="left", padx=5)
        
        status_bg = get_status_color(status)
        tk.Label(row, text=status or "", font=FONT, bg=status_bg, fg=TEXT_DARK,
                 width=12, anchor="center", relief="solid", borderwidth=1).pack(side="left", padx=5)
        
        ds_text = date_started.strftime("%Y-%m-%d") if (date_started and hasattr(date_started, 'strftime')) else ""
        df_text = date_finished.strftime("%Y-%m-%d") if (date_finished and hasattr(date_finished, 'strftime')) else ""

        tk.Label(row, text=ds_text, font=FONT, bg="#f7e797", fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=5)
        tk.Label(row, text=df_text, font=FONT, bg="#f7e797", fg=TEXT_DARK, width=12, anchor="w").pack(side="left", padx=5)
        
        action_frame = tk.Frame(row, bg="#f7e797")
        action_frame.pack(side="right", padx=5)
        
        # ALWAYS SHOW VIEW BUTTON
        tk.Button(action_frame, text="VIEW", bg=BTN_BROWN, fg="white", width=9,
                  font=("Arial", 9, "bold"), command=lambda rid=rec_id: view_record(rid)).pack(side="left", padx=2)
        
        if status == "Pending":
            tk.Button(action_frame, text="APPROVE", bg=BTN_GREEN, fg="white", width=9,
                      font=("Arial", 9, "bold"), command=lambda rid=rec_id: update_status(rid, "Reading")).pack(side="left", padx=2)
            tk.Button(action_frame, text="REJECT", bg=BTN_RED, fg="white", width=9,
                      font=("Arial", 9, "bold"), command=lambda rid=rec_id: update_status(rid, "Dropped")).pack(side="left", padx=2)
        elif status == "Reading":
            tk.Button(action_frame, text="DONE", bg=BTN_GREEN, fg="white", width=9,
                      font=("Arial", 9), command=lambda rid=rec_id: update_status(rid, "Completed")).pack(side="left", padx=2)
            tk.Button(action_frame, text="HOLD", bg=BTN_YELLOW, fg=TEXT_DARK, width=9,
                      font=("Arial", 9), command=lambda rid=rec_id: update_status(rid, "On Hold")).pack(side="left", padx=2)
        elif status == "On Hold":
            tk.Button(action_frame, text="RESUME", bg=BTN_GREEN, fg=TEXT_DARK, width=9,
                      font=("Arial", 9), command=lambda rid=rec_id: update_status(rid, "Reading")).pack(side="left", padx=2)
            tk.Button(action_frame, text="DONE", bg=BTN_GREEN, fg="white", width=9,
                      font=("Arial", 9), command=lambda rid=rec_id: update_status(rid, "Completed")).pack(side="left", padx=2)
        else:
            tk.Label(action_frame, text="", font=FONT, bg="#f7e797").pack(side="left", padx=20)

def filter_records(search_text, status_filter):
    global rows_container_ref
    if not rows_container_ref:
        return
    filtered = []
    search_text = search_text.lower()
    
    for item in borrow_data:
        rec_id, username, book_title, status, ds, df = item
        match_search = (search_text in (username or "").lower() or 
                        search_text in (book_title or "").lower())
        match_status = (status_filter == "ALL" or status == status_filter)
        if match_search and match_status:
            filtered.append(item)
    
    render_borrow_rows(rows_container_ref, filtered)

def load_borrow_from_db():
    global borrow_data
    borrow_data = []
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT br.Record_ID, u.Username, b.Book_Title, br.Status,
                   br.Borrow_Date, br.Date_Returned
            FROM borrow_records br
            JOIN User u ON br.User_ID = u.User_ID
            JOIN books b ON br.Book_ID = b.Book_ID
            ORDER BY br.Borrow_Date DESC
        """)

        borrow_data = cur.fetchall()
        # ✅ Debug: print to console
        print(f"Loaded {len(borrow_data)} records")
        for rec in borrow_data:
            print(f"Status: [{rec[3]}] — {rec[2]}")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load records:\n{e}")
    finally:
        conn.close()


def update_status(rec_id, new_status):
    allowed_previous_statuses = {
        "Reading": ("Pending", "On Hold"),
        "Dropped": ("Pending",),
        "Completed": ("Reading", "On Hold"),
        "On Hold": ("Reading",),
    }
    previous_statuses = allowed_previous_statuses.get(new_status)
    if previous_statuses is None:
        messagebox.showerror("Invalid Status", f"Unsupported status: {new_status}")
        return

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            placeholders = ", ".join(["%s"] * len(previous_statuses))
            update_query = "UPDATE borrow_records SET Status = %s"
            if new_status == "Completed":
                update_query += ", Date_Returned = CURDATE()"
            update_query += " WHERE Record_ID = %s AND Status IN (" + placeholders + ")"
            cur.execute(update_query, (new_status, rec_id, *previous_statuses))
            if cur.rowcount == 0:
                messagebox.showwarning(
                    "Status Not Changed",
                    "The record no longer has a status that allows this change."
                )
                return
            conn.commit()
            messagebox.showinfo("Updated", f"Status changed to: {new_status}")
            show_admin_borrow_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{e}")
        finally:
            conn.close()

def add_borrow_book():
    clear_all()
    
    # ✅ Wider form frame
    frame = tk.Frame(root, bg="#f7e797", width=1440, height=900)
    frame.pack(fill="both", expand=True)
    
    # ========= HEADER =========
    header = tk.Frame(frame, bg="#f7e797", padx=15, pady=10)
    header.pack(fill="x")
    
    tk.Label(header, text="ADD BOOKS", font=FONT_TITLE, bg="#f7e797", fg=TEXT_DARK).pack(side="left")
    
    tk.Button(header, text="BACK", bg=BTN_BROWN, fg="white", width=8,
              relief="solid", borderwidth=1, command=go_back).pack(side="right")
    
    # ========= FORM TITLE BAR =========
    title_bar = tk.Frame(frame, bg="#e8d590", padx=15, pady=8, relief="solid", borderwidth=1)
    title_bar.pack(fill="x", padx=20, pady=(0, 10))
    
    tk.Label(title_bar, text="ADD BOOKS & RECORD", font=FONT_HEADING,
             bg="#e8d590", fg=TEXT_DARK).pack(anchor="w")

    btn_frame = tk.Frame(frame, bg="#f7e797", pady=8)
    btn_frame.pack(side="bottom", fill="x")
    
    # ✅ FIXED: Wider form box + scrollable
    form_canvas = tk.Canvas(frame, bg="#f7e797", highlightthickness=0)
    form_scroll = tk.Scrollbar(frame, orient="vertical", command=form_canvas.yview)
    form_box = tk.Frame(form_canvas, bg="#f7e797", padx=30, pady=25)
    
    form_box.bind("<Configure>", lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))
    form_canvas.create_window((0, 0), window=form_box, anchor="nw", width=850)
    form_canvas.configure(yscrollcommand=form_scroll.set)
    
    form_canvas.pack(side="left", fill="both", expand=True, padx=20)
    form_scroll.pack(side="right", fill="y")
    
    # --- Select Book — Wider dropdown ---
    tk.Label(form_box, text="Select Book:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    
    conn = get_db_connection()
    book_titles = []
    debug_msg = ""
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DESCRIBE books")
            cols = [c[0] for c in cur.fetchall()]
            debug_msg = f"Books columns: {', '.join(cols)}\n"
            
            if "Book_Title" in cols:
                cur.execute("SELECT Book_Title FROM books ORDER BY Book_Title")
            elif "Title" in cols:
                cur.execute("SELECT Title FROM books ORDER BY Title")
            else:
                raise Exception(f"No title column found in books! Columns: {cols}")
            
            book_titles = [row[0] for row in cur.fetchall()]
            debug_msg += f"Found {len(book_titles)} books"
            
        except Exception as e:
            messagebox.showerror("DB Error", f"Cannot load books:\n{debug_msg}\n{e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "No database connection!")
    
    book_var = tk.StringVar()
    book_select = ttk.Combobox(form_box, textvariable=book_var,
                              values=book_titles, font=FONT, width=55, state="readonly")
    book_select.pack(pady=(2, 12))
    
    if not book_titles:
        tk.Label(form_box, text="⚠ No books found! Add books to the 'books' table first.", 
                 font=FONT, bg="#ffcccc", fg="red", padx=10, pady=5).pack(pady=(0, 10))
    
    # --- Status ---
    tk.Label(form_box, text="Status:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    status_var = tk.StringVar(value="Pending")
    status_select = ttk.Combobox(form_box, textvariable=status_var,
                                 values=["Pending", "Unread", "Reading", "On Hold", "Completed", "Dropped"],
                                 font=FONT, width=55, state="readonly")  # ← Wider
    status_select.pack(pady=(2, 12))
    
    # --- Date Started ---
    tk.Label(form_box, text="Date Started:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    date_started_picker = DatePicker(form_box, default_text="YYYY-MM-DD", width=45)
    date_started_picker.pack(anchor="w", pady=(2, 12))
    
    # --- Date Finished ---
    tk.Label(form_box, text="Date Finished:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    date_finished_picker = DatePicker(form_box, default_text="YYYY-MM-DD", width=45)
    date_finished_picker.pack(anchor="w", pady=(2, 12))
    
    # --- Rate ---
    tk.Label(form_box, text="Rate:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    rate_var = tk.StringVar(value="---/5")
    rate_select = ttk.Combobox(form_box, textvariable=rate_var,
                              values=["---/5", "1/5", "2/5", "3/5", "4/5", "5/5"],
                              font=FONT, width=55, state="readonly")  # ← Wider
    rate_select.pack(pady=(2, 12))
    
    # --- Notes — Wider input ---
    tk.Label(form_box, text="Notes:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
    e_notes = tk.Entry(form_box, width=55, font=FONT)  # ← Wider
    e_notes.pack(pady=(2, 20))
    
    # ========= BUTTONS =========
    def save_record():
        book_title = book_var.get().strip()
        status = status_var.get()
        rating = rate_var.get()
        notes = e_notes.get().strip()

        try:
            date_started = date_started_picker.get()
            date_finished = date_finished_picker.get()
        except ValueError as err:
            messagebox.showwarning("Invalid Date", str(err))
            return

        if not book_title:
            messagebox.showwarning("Warning", "Please select a Book!")
            return
        if not date_started:
            messagebox.showwarning("Warning", "Please select Date Started!")
            return
        if date_finished and date_finished < date_started:
            messagebox.showwarning("Invalid Date", "Date Finished cannot be before Date Started.")
            return
        
        conn = get_db_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            
            cur.execute("DESCRIBE books")
            cols = [c[0] for c in cur.fetchall()]
            title_col = "Book_Title" if "Book_Title" in cols else "Title"
            
            cur.execute(f"SELECT Book_ID FROM books WHERE {title_col} = %s", (book_title,))
            book_result = cur.fetchone()
            if not book_result:
                messagebox.showerror("Error", "Book not found in database!")
                return
            book_id = book_result[0]
            
            cur.execute("SELECT User_ID FROM User WHERE Username = %s", (Main.current_user["username"],))
            user_result = cur.fetchone()
            if not user_result:
                messagebox.showerror("Error", "Admin account not found!")
                return
            user_id = user_result[0]
            
            cur.execute("""
                INSERT INTO borrow_records 
                (User_ID, Book_ID, Status, Borrow_Date, Date_Returned, Book_Rating, Book_Review)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, book_id, status,
                date_started,
                date_finished if date_finished else None,
                rating if rating != "---/5" else None,
                notes if notes else None
            ))
            
            conn.commit()
            messagebox.showinfo("Success", f"Book added!\n\nTitle: {book_title}\nStatus: {status}")
            show_admin_borrow_screen()
            
        except Exception as err:
            messagebox.showerror("Save Failed", f"Error: {err}")
        finally:
            conn.close()
    
    tk.Button(btn_frame, text="SAVE", bg=BTN_GREEN, fg=TEXT_DARK,
              width=12, font=FONT, relief="solid", borderwidth=1,
              command=save_record).grid(row=0, column=0, padx=10)
    
    tk.Button(btn_frame, text="CANCEL", bg=BTN_RED, fg="white",
              width=12, font=FONT, relief="solid", borderwidth=1,
              command=show_admin_borrow_screen).grid(row=0, column=1, padx=10)

def view_record(rec_id):
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT br.Record_ID, u.Username, b.Book_Title, br.Status,
                   br.Borrow_Date, br.Date_Returned, br.Book_Rating, br.Book_Review
            FROM borrow_records br
            JOIN User u ON br.User_ID = u.User_ID
            JOIN books b ON br.Book_ID = b.Book_ID
            WHERE br.Record_ID = %s
        """, (rec_id,))

        result = cur.fetchone()
        
        if not result:
            messagebox.showerror("Error", "Record not found!")
            return
        
        rec_id, username, book_title, status, date_started, date_finished, rating, review = result
        
        # ✅ FIXED: Wider window + allow resizing
        view_win = tk.Toplevel(root)
        view_win.title(f"VIEW RECORD - {book_title}")
        view_win.geometry("520x520")  # ← WIDER & TALLER
        view_win.minsize(480, 480)     # ← Minimum size
        view_win.configure(bg="#f7e797")
        view_win.transient(root)
        view_win.grab_set()
        view_win.resizable(True, True)  # ← Allow resize

        # Title bar
        title_bar = tk.Frame(view_win, bg="#e8d590", padx=15, pady=10, relief="solid", borderwidth=1)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text=f"VIEW RECORD - {book_title}", 
                 font=("Arial", 11, "bold"), bg="#e8d590", fg=TEXT_DARK).pack(anchor="w")

        # ✅ FIXED: Proper scrollable area
        canvas = tk.Canvas(view_win, bg="#f7e797", highlightthickness=0)
        scrollbar = tk.Scrollbar(view_win, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg="#f7e797", padx=25, pady=15)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content.bind("<Configure>", on_configure)
        canvas.create_window((0, 0), window=content, anchor="nw", width=460)  # ← Wider content area
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        view_win.bind("<MouseWheel>", _on_mousewheel)

        def get_stars(rating_val):
            if not rating_val or rating_val in ["---/5", ""]:
                return "Not rated yet"
            try:
                num = int(str(rating_val).split("/")[0]) if "/" in str(rating_val) else int(rating_val)
                return "⭐" * num
            except:
                return str(rating_val)

        # --- Username ---
        tk.Label(content, text="Username:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=username, font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w").pack(fill="x", pady=(0, 10))

        # --- Book Title — Wrapped properly ---
        tk.Label(content, text="Book Title:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=book_title, font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w",
                 wraplength=440).pack(fill="x", pady=(0, 10))  # ← Wraps long titles

        # --- Status ---
        tk.Label(content, text="Status:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=status, font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w").pack(fill="x", pady=(0, 10))

        ds_text = date_started.strftime("%Y-%m-%d") if (date_started and hasattr(date_started, 'strftime')) else "—"
        df_text = date_finished.strftime("%Y-%m-%d") if (date_finished and hasattr(date_finished, 'strftime')) else "Not finished"

        tk.Label(content, text="Date Started:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=ds_text, font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w").pack(fill="x", pady=(0, 10))

        tk.Label(content, text="Date Finished:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=df_text, font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w").pack(fill="x", pady=(0, 10))

        # --- Rating ---
        tk.Label(content, text="Rating:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=get_stars(rating), font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w").pack(fill="x", pady=(0, 10))

        # --- Notes ---
        tk.Label(content, text="Notes:", font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        tk.Label(content, text=review or "No notes added", font=FONT, bg="white", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, padx=8, pady=4, anchor="w",
                 wraplength=440).pack(fill="x", pady=(0, 15))

        # BACK Button
        tk.Button(content, text="BACK", bg=BTN_BROWN, fg="white", width=12,
                 relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
                 command=view_win.destroy).pack(pady=(10, 15))

    except Exception as e:
        messagebox.showerror("Error", f"Could not load record:\n{e}")
    finally:
        conn.close()

def go_back():
    from AdminDB import show_admin_dashboard
    show_admin_dashboard()