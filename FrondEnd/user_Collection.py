import tkinter as tk
from tkinter import messagebox, ttk
import Main

# ========== SHORTCUTS ==========
root = Main.root
clear_all = Main.clear_all
get_db_connection = Main.get_db_connection
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

# ==================================================
# USER COLLECTION — Matches YOUR Design & Database
# ==================================================
def show_user_collection_screen():
    clear_all()

    # Main frame
    main_frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    main_frame.pack(fill="both", expand=True)

    # Header
    header = tk.Frame(main_frame, bg="#f5e9c8", padx=15, pady=12)
    header.pack(fill="x")
    tk.Label(header, text="★ MY COLLECTION – (USERS BOOKS)",
             font=FONT_TITLE, bg="#f5e9c8", fg=TEXT_DARK).pack(side="left")
    tk.Button(header, text="BACK", bg=BTN_YELLOW, fg=TEXT_DARK,
              font=FONT, command=Main.show_navigation_dashboard,
              relief="solid", borderwidth=1).pack(side="right")

    # Content
    content = tk.Frame(main_frame, bg=BG_CONTENT, padx=20, pady=20)
    content.pack(fill="both", expand=True)

    top_bar = tk.Frame(content, bg=BG_CONTENT)
    top_bar.pack(fill="x", pady=(0, 10))
    tk.Label(top_bar, text="MY COLLECTION", font=FONT_HEADING,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(side="left")
    tk.Button(top_bar, text="+ Add To Collections", bg=BTN_GREEN, fg=TEXT_DARK,
              font=FONT, relief="solid", borderwidth=1,
              command=open_add_book_dialog).pack(side="right")

    # Table container
    table_frame = tk.Frame(content, bg=BG_CARD, relief="solid", borderwidth=1)
    table_frame.pack(fill="both", expand=True)
    for column in range(4):
        table_frame.grid_columnconfigure(column, weight=1)
    table_frame.grid_rowconfigure(1, weight=1)

    # Headers — Exactly matches your design
    headers = ["ID", "BOOK TITLE", "ADDED DATE", "ACTIONS"]
    for col, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=FONT, bg="#e8d5b0", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, width=18).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    canvas = tk.Canvas(table_frame, bg=BG_CARD, highlightthickness=0)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    rows_frame = tk.Frame(canvas, bg=BG_CARD)
    rows_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    rows_window = canvas.create_window((0, 0), window=rows_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(rows_window, width=event.width))
    canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")
    scrollbar.grid(row=1, column=4, sticky="ns")

    def load_data():
        for widget in rows_frame.winfo_children():
            widget.destroy()

        user_name = current_user.get("username", "")
        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT Collection_ID, Book_Title, Added_Date, Status
                FROM collection WHERE User_Name=%s ORDER BY Added_Date DESC
            """, (user_name,))
            rows = cur.fetchall()

            for idx, row in enumerate(rows):
                rec_id, btitle, adate, status = row

                display_status = "[ACTIVE]" if status == "Active" else "[IN-ACTIVE]"
                status_color = BTN_GREEN if status == "Active" else BTN_RED

                tk.Label(rows_frame, text=str(rec_id), font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=0, sticky="nsew", padx=1, pady=1)
                tk.Label(rows_frame, text=btitle or "", font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=1, sticky="nsew", padx=1, pady=1)
                tk.Label(rows_frame, text=str(adate or ""), font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=2, sticky="nsew", padx=1, pady=1)

                action_frame = tk.Frame(rows_frame, bg="#fff3d4")
                action_frame.grid(row=idx, column=3, sticky="nsew", padx=1, pady=1)
                
                tk.Label(action_frame, text=display_status, bg=status_color, fg=TEXT_DARK,
                         font=FONT, relief="solid", borderwidth=1).pack(pady=1, fill="x")
                tk.Button(action_frame, text="REMOVE", bg=BTN_RED, fg="white",
                         font=FONT, relief="solid", borderwidth=1,
                         command=lambda rid=rec_id: remove_record(rid)).pack(pady=1, fill="x")

            # Empty row if no data
            if not rows:
                tk.Label(rows_frame, text="No books in your collection yet.\nClick '+ Add To Collections' to start!",
                         font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=0, column=0, columnspan=4, sticky="nsew", pady=20)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def remove_record(rec_id):
        if not messagebox.askyesno("Confirm", "Remove from your collection?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM collection WHERE Collection_ID=%s AND User_Name=%s",
                    (rec_id, current_user.get("username", ""))
                )
                if cur.rowcount == 0:
                    messagebox.showwarning("Not Removed", "This collection entry is no longer available.")
                    return
                conn.commit()
                messagebox.showinfo("Removed", "Book removed from collection")
                load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def open_add_book_dialog():
        win = tk.Toplevel(root)
        win.title("Add Book to Collection")
        win.geometry("500x250")
        win.configure(bg=BG_CONTENT)
        win.transient(root)
        win.grab_set()

        tk.Label(win, text="Book:", font=FONT, bg=BG_CONTENT, fg=TEXT_DARK).pack(pady=(30, 5))
        book_select = ttk.Combobox(win, font=FONT, width=38, state="readonly")
        book_select.pack(pady=5)

        conn = get_db_connection()
        if not conn:
            win.destroy()
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT Book_Title FROM Books ORDER BY Book_Title")
            book_select["values"] = [row[0] for row in cur.fetchall()]
        except Exception as e:
            win.destroy()
            messagebox.showerror("Error", f"Cannot load books:\n{e}")
            return
        finally:
            conn.close()

        def save_new():
            btitle = book_select.get().strip()
            if not btitle:
                messagebox.showwarning("Warning", "Select a book!")
                return
            uname = current_user.get("username", "")
            if not uname:
                messagebox.showerror("Error", "Please log in again before editing your collection.")
                return
            conn = get_db_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT Collection_ID FROM collection "
                        "WHERE User_Name=%s AND Book_Title=%s AND Status='Active'",
                        (uname, btitle)
                    )
                    if cur.fetchone():
                        messagebox.showwarning("Already Added", "This book is already in your collection.")
                        return
                    cur.execute("""
                        INSERT INTO collection (User_Name, Book_Title, Added_Date, Status)
                        VALUES (%s, %s, CURDATE(), 'Active')
                    """, (uname, btitle))
                    conn.commit()
                    messagebox.showinfo("Added", "Book added to your collection!")
                    win.destroy()
                    load_data()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    conn.close()

        tk.Button(win, text="ADD BOOK", bg=BTN_GREEN, fg=TEXT_DARK,
                  font=FONT, command=save_new, relief="solid", borderwidth=1).pack(pady=15)

    load_data()
