import tkinter as tk
from tkinter import messagebox, ttk
import Main
from datetime import datetime, date

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
current_user = Main.current_user

borrow_data = []
rows_container_ref = None

# ========== HELPER: SAFE DATE FORMATTER ==========
def safe_date_str(val):
    if not val:
        return ""
    if isinstance(val, (datetime, date)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, str):
        try:
            return datetime.strptime(val[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            return val[:10]
    return str(val)

# ========== DATE PICKER COMPONENT ==========
class DatePicker:
    def __init__(self, parent, label_text, default_text="YYYY-MM-DD", width=30):
        self.frame = tk.Frame(parent, bg="#f7e797")
        tk.Label(self.frame, text=label_text, font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
        entry_row = tk.Frame(self.frame, bg="#f7e797")
        entry_row.pack(fill="x")
        self.entry = tk.Entry(entry_row, font=FONT, width=width, bg="white")
        self.entry.insert(0, default_text)
        self.entry.pack(side="left")
        self.cal_btn = tk.Button(entry_row, text="📅", bg=BTN_BROWN, fg="white",
                                  width=3, relief="solid", borderwidth=1,
                                  command=self.show_calendar)
        self.cal_btn.pack(side="left", padx=(5, 0))
        self.calendar_window = None

    def show_calendar(self):
        if self.calendar_window and self.calendar_window.winfo_exists():
            self.calendar_window.destroy()
        top = tk.Toplevel(root)
        top.title("Select Date")
        top.geometry("300x280")
        top.configure(bg="#f7e797")
        top.transient(root)
        top.grab_set()
        self.calendar_window = top
        now = datetime.now()
        self.cur_year = now.year
        self.cur_month = now.month
        nav = tk.Frame(top, bg="#e8d590", pady=5)
        nav.pack(fill="x")
        tk.Button(nav, text="<", command=lambda: self.month_change(-1),
                  bg=BTN_BROWN, fg="white", width=3).pack(side="left", padx=5)
        self.month_lbl = tk.Label(nav, text="", font=FONT_TITLE, bg="#e8d590")
        self.month_lbl.pack(side="left", expand=True)
        tk.Button(nav, text=">", command=lambda: self.month_change(1),
                  bg=BTN_BROWN, fg="white", width=3).pack(side="right", padx=5)
        days_header = tk.Frame(top, bg="#f7e797")
        days_header.pack()
        for d in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            tk.Label(days_header, text=d, font=FONT, bg="#e8d590", width=5).grid(row=0, column=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].index(d))
        self.dates_frame = tk.Frame(top, bg="#f7e797")
        self.dates_frame.pack(pady=5)
        self._render_calendar()

    def _render_calendar(self):
        for w in self.dates_frame.winfo_children(): w.destroy()
        self.month_lbl.config(text=datetime(self.cur_year, self.cur_month, 1).strftime("%B %Y"))
        first = datetime(self.cur_year, self.cur_month, 1)
        start_col = (first.weekday() + 1) % 7
        next_month = self.cur_month % 12 + 1
        days_count = (datetime(self.cur_year, next_month, 1) - first).days
        row = 0
        for _ in range(start_col):
            tk.Label(self.dates_frame, text="", width=5, bg="#f7e797").grid(row=row, column=_)
        for day in range(1, days_count + 1):
            col = (start_col + day - 1) % 7
            if col == 0 and day > 1: row += 1
            tk.Button(self.dates_frame, text=str(day), width=5,
                      bg=BG_CONTENT, fg=TEXT_DARK, relief="solid", borderwidth=1,
                      command=lambda d=day: self._select(d)).grid(row=row, column=col, pady=2)

    def month_change(self, delta):
        self.cur_month += delta
        if self.cur_month < 1:
            self.cur_month = 12
            self.cur_year -= 1
        elif self.cur_month > 12:
            self.cur_month = 1
            self.cur_year += 1
        self._render_calendar()

    def _select(self, day):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{self.cur_year}-{self.cur_month:02d}-{day:02d}")
        if self.calendar_window and self.calendar_window.winfo_exists():
            self.calendar_window.destroy()

    def get(self):
        val = self.entry.get().strip()
        if not val or val == "YYYY-MM-DD":
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except:
            return None

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

# ========== LOAD BOOK LIST ==========
_cached_books = None
def get_book_list():
    global _cached_books
    if _cached_books is not None:
        return _cached_books
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT Book_Title FROM Books ORDER BY Book_Title")
        _cached_books = [row[0] for row in cur.fetchall()]
        return _cached_books
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load books:\n{e}")
        return []
    finally:
        conn.close()

# ==================================================
# USER BORROW — MAIN LIST
# ==================================================
def show_user_borrow_screen():
    global rows_container_ref, borrow_data
    role = current_user.get("role", "")
    if role == "Admin":
        messagebox.showerror("Access Denied", "This page is for Users only.")
        Main.show_navigation_dashboard()
        return
    clear_all()

    main_frame = tk.Frame(root, bg="#f5e9a5", width=1440, height=900)
    main_frame.pack(fill="both", expand=True)
    top_bar = tk.Frame(main_frame, bg="#e8d57a", padx=15, pady=10)
    top_bar.pack(fill="x")
    tk.Label(top_bar, text="BORROW BOOKS", font=FONT_TITLE, bg="#e8d57a", fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="+ Borrow Books", bg=BTN_GREEN, fg="white", width=14,
              relief="solid", borderwidth=1, command=borrow_book).pack(side="right", padx=5)
    tk.Button(top_bar, text="BACK", bg=BTN_BROWN, fg="white", width=10,
              relief="solid", borderwidth=1, command=Main.show_navigation_dashboard).pack(side="right")
    
    filter_frame = tk.Frame(main_frame, bg="#f5e9a5", pady=10)
    filter_frame.pack(fill="x", padx=20)
    tk.Label(filter_frame, text="Search:", font=FONT, bg="#f5e9a5", fg=TEXT_DARK).pack(side="left", padx=5)
    search_entry = tk.Entry(filter_frame, font=FONT, width=25)
    search_entry.pack(side="left", padx=5)
    tk.Label(filter_frame, text="Status List:", font=FONT, bg="#f5e9a5", fg=TEXT_DARK).pack(side="left", padx=(20,5))
    status_combo = ttk.Combobox(filter_frame, values=["ALL", "Unread", "Reading", "Completed", "On Hold", "Dropped", "Pending"],
                                font=FONT, width=18, state="readonly")
    status_combo.set("ALL")
    status_combo.pack(side="left", padx=5)
    
    table_frame = tk.Frame(main_frame, bg="#f7e797", padx=15, pady=15, relief="solid", borderwidth=2)
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    header_row = tk.Frame(table_frame, bg="#e8d590", pady=8)
    header_row.pack(fill="x")
    for col, w in [("#",5), ("BOOK TITLE",30), ("STATUS",15), ("DATE STARTED",15), ("DATE FINISHED",15), ("ACTIONS",12)]:
        tk.Label(header_row, text=col, font=FONT_TITLE, bg="#e8d590", fg=TEXT_DARK, width=w, anchor="w").pack(side="left", padx=5)
    tk.Frame(table_frame, bg="#7B2CBF", height=2).pack(fill="x", pady=5)

    list_container = tk.Frame(table_frame, bg="#f7e797")
    list_container.pack(fill="both", expand=True)
    canvas = tk.Canvas(list_container, bg="#f7e797", highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    rows_container = tk.Frame(canvas, bg="#f7e797")
    rows_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=rows_container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    rows_container_ref = rows_container
    
    load_borrow_from_db()
    render_borrow_rows(rows_container)
    
    def on_filter_change(_):
        if rows_container_ref:
            filter_records(search_entry.get(), status_combo.get())
    search_entry.bind("<KeyRelease>", on_filter_change)
    status_combo.bind("<<ComboboxSelected>>", on_filter_change)

def get_status_color(status):
    return {
        "Unread": "#D3D3D3", "Pending": BTN_YELLOW, "Reading": "#90EE90",
        "Completed": BTN_GREEN, "On Hold": "#FFB347", "Dropped": BTN_RED
    }.get(status, BG_CONTENT)

def render_borrow_rows(parent, filtered=None):
    if not parent:
        return
    for w in parent.winfo_children():
        w.destroy()
    data = filtered if filtered is not None else borrow_data
    if not data:
        tk.Label(parent, text="No records found.", font=FONT, bg="#f7e797", fg=TEXT_DARK).pack(pady=30)
        return
    for idx, item in enumerate(data, 1):
        rec_id, title, status, ds, df = item
        row = tk.Frame(parent, bg="#f7e797", pady=6)
        row.pack(fill="x")
        tk.Label(row, text=str(idx), font=FONT, bg="#f7e797", fg=TEXT_DARK, width=5).pack(side="left", padx=5)
        tk.Label(row, text=title or "", font=FONT, bg="#f7e797", fg=TEXT_DARK, width=30, anchor="w").pack(side="left", padx=5)
        tk.Label(row, text=status or "", font=FONT, bg=get_status_color(status), fg=TEXT_DARK,
                 width=15, anchor="center", relief="solid", borderwidth=1).pack(side="left", padx=5)
        tk.Label(row, text=safe_date_str(ds), font=FONT, bg="#f7e797", fg=TEXT_DARK, width=15).pack(side="left", padx=5)
        tk.Label(row, text=safe_date_str(df) or "Not Yet Edited", font=FONT, bg="#f7e797", fg=TEXT_DARK, width=15).pack(side="left", padx=5)
        act = tk.Frame(row, bg="#f7e797")
        act.pack(side="right", padx=5)
        tk.Button(act, text="VIEW", bg=BTN_BROWN, fg="white", width=9, font=("Arial",9,"bold"),
                  command=lambda rid=rec_id: view_record(rid)).pack(side="left", padx=2)

def filter_records(search_text, status_filter):
    if not rows_container_ref:
        return
    filtered = []
    search_text = search_text.lower()
    for item in borrow_data:
        _, title, status, _, _ = item
        match_search = search_text in (title or "").lower()
        match_status = status_filter == "ALL" or status == status_filter
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
        user_id = current_user.get("user_id")
        if not user_id:
            messagebox.showwarning("Note", "Please log in first.")
            return
        cur.execute("""
            SELECT br.Record_ID, b.Book_Title, br.Status, br.Borrow_Date, br.Date_Returned
            FROM borrow_records br
            JOIN Books b ON br.Book_ID = b.Book_ID
            WHERE br.User_ID = %s
            ORDER BY br.Borrow_Date DESC
        """, (user_id,))
        borrow_data = cur.fetchall()
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load records:\n{e}")
    finally:
        conn.close()

def save_borrow_request():
    book_title = book_select.get().strip()
    date_started = date_started_picker.get()
    date_finished = date_finished_picker.get()
    rating = rate_var.get()
    notes = e_notes.get().strip()

    if not book_title:
        messagebox.showwarning("Warning", "Please select a Book!")
        return
    if not date_started:
        messagebox.showwarning("Warning", "Date Started is required!")
        return

    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT Book_ID FROM books WHERE Book_Title = %s", (book_title,))
        book_result = cur.fetchone()
        if not book_result:
            messagebox.showerror("Error", "Book not found in database!")
            return
        book_id = book_result[0]

        user_id = current_user.get("user_id") or current_user.get("User_ID")
        if not user_id:
            messagebox.showerror("Error", "User not found! Please log in again.")
            return

        cur.execute("""
            INSERT INTO borrow_records
            (User_ID, Book_ID, Status, Borrow_Date, Date_Returned, Book_Rating, Book_Review)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, book_id, "Pending", date_started,
            date_finished if date_finished else None,
            rating if rating != "---/5" else None,
            notes if notes else None
        ))

        conn.commit()
        messagebox.showinfo("Request Submitted",
            "Your borrow request has been sent!\n\nWaiting for Admin approval.")
        show_user_borrow_screen()
    except Exception as err:
        messagebox.showerror("Request Failed", f"Error: {err}")
    finally:
        conn.close()

def view_record(rec_id):
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT br.Record_ID, b.Book_Title, br.Status,
                   br.Borrow_Date, br.Date_Returned, br.Book_Rating, br.Book_Review
            FROM borrow_records br
            JOIN Books b ON br.Book_ID = b.Book_ID
            WHERE br.Record_ID = %s
        """, (rec_id,))
        result = cur.fetchone()
        if not result:
            messagebox.showerror("Error", "Record not found!")
            return
        rec_id, book_title, status, date_started, date_finished, rating, review = result

        view_win = tk.Toplevel(root)
        view_win.title(f"VIEW RECORD - {book_title}")
        view_win.geometry("300x420")
        view_win.configure(bg="#f7e797")
        view_win.transient(root)
        view_win.grab_set()
        view_win.resizable(False, False)

        title_bar = tk.Frame(view_win, bg="#e8d590", padx=15, pady=10, relief="solid", borderwidth=1)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text=f"VIEW RECORD - {book_title}",
                 font=("Arial", 11, "bold"), bg="#e8d590", fg=TEXT_DARK).pack(anchor="w")

        content = tk.Frame(view_win, bg="#f7e797", padx=20, pady=15)
        content.pack(fill="both", expand=True)

        def get_stars(rating_val):
            if not rating_val or rating_val in ["---/5", ""]:
                return "Not rated yet"
            try:
                num = int(str(rating_val).split("/")[0]) if "/" in str(rating_val) else int(rating_val)
                return "⭐" * num
            except:
                return str(rating_val)

        fields = [
            ("Book Title:", book_title),
            ("Status:", status),
            ("Date Started:", safe_date_str(date_started) or "—"),
            ("Date Finished:", safe_date_str(date_finished) or "Not yet edited"),
            ("Rating:", get_stars(rating)),
            ("Notes:", review or "No notes added")
        ]

        for label_text, value in fields:
            tk.Label(content, text=label_text, font=FONT, bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x")
            tk.Label(content, text=value, font=FONT, bg="white", fg=TEXT_DARK,
                     relief="solid", borderwidth=1, padx=8, pady=4, anchor="w",
                     wraplength=220 if label_text == "Notes:" else None).pack(fill="x", pady=(0, 10))

        tk.Button(view_win, text="CLOSE", bg=BTN_BROWN, fg="white", width=12,
                  relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
                  command=view_win.destroy).pack(pady=(0, 10))

    except Exception as e:
        messagebox.showerror("Error", f"Could not load record:\n{e}")
    finally:
        conn.close()

# ==================================================
# BORROW BOOK FORM
# ==================================================
def borrow_book():
    clear_all()
    
    form_frame = tk.Frame(root, bg="#f7e797", padx=30, pady=25)
    form_frame.pack(fill="both", expand=True)
    
    tk.Label(form_frame, text="ADD BORROW REQUEST", font=FONT_TITLE, 
             bg="#f7e797", fg=TEXT_DARK).pack(pady=(0, 20))
    
    global book_select, date_started_picker, date_finished_picker, rate_var, e_notes
    
    # Book Selection
    tk.Label(form_frame, text="Select Book:", font=FONT, 
             bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    book_list = get_book_list()
    book_select = ttk.Combobox(form_frame, values=book_list, font=FONT, width=40, state="readonly")
    book_select.pack(pady=(0, 10))
    
    # Status (display only)
    tk.Label(form_frame, text="Status:", font=FONT, 
             bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 2))
    tk.Label(form_frame, text="Pending Approval — Admin will update status", 
             bg="#e8d590", fg=TEXT_DARK, font=FONT, padx=10, pady=8).pack(fill="x", pady=(0, 10))
    
    # Date Started
    date_started_picker = DatePicker(form_frame, "Date Started:")
    date_started_picker.pack(fill="x", pady=(10, 5))
    date_started_picker.entry.delete(0, tk.END)
    date_started_picker.entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    # Date Finished
    date_finished_picker = DatePicker(form_frame, "Date Finished (Optional):")
    date_finished_picker.pack(fill="x", pady=(10, 5))
    
    # Rating
    tk.Label(form_frame, text="Rating (Optional):", font=FONT, 
             bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(15, 2))
    rate_var = tk.StringVar(value="---/5")
    rate_select = ttk.Combobox(form_frame, textvariable=rate_var,
        values=["---/5", "1/5", "2/5", "3/5", "4/5", "5/5"],
        font=FONT, width=30, state="readonly")
    rate_select.pack(pady=(0, 10))
    
    # Notes / Message
    tk.Label(form_frame, text="Notes / Message:", font=FONT, 
             bg="#f7e797", fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(15, 2))
    e_notes = tk.Entry(form_frame, font=FONT, width=40)
    e_notes.pack(pady=(0, 20))
    
    # Buttons
    tk.Button(form_frame, text="SUBMIT REQUEST", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1, padx=30, pady=8,
              command=save_borrow_request).pack(pady=(10, 10))
    
    tk.Button(form_frame, text="← BACK", bg=BTN_BROWN, fg="white",
              font=FONT, relief="solid", borderwidth=1, padx=30, pady=8,
              command=show_user_borrow_screen).pack(pady=(5, 10))