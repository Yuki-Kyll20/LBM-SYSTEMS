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

# ==================================================
# ADMIN COLLECTION — Matches YOUR Table Structure
# ==================================================
def show_admin_collection_screen():
    clear_all()

    # Main frame
    main_frame = tk.Frame(root, bg=BG_MAIN, width=1440, height=900)
    main_frame.pack(fill="both", expand=True)

    # Header
    header = tk.Frame(main_frame, bg="#f5e9c8", padx=15, pady=12)
    header.pack(fill="x")
    tk.Label(header, text="★ MY COLLECTION – (ADMIN BOOKS)",
             font=FONT_TITLE, bg="#f5e9c8", fg=TEXT_DARK).pack(side="left")
    tk.Button(header, text="BACK", bg=BTN_YELLOW, fg=TEXT_DARK,
              font=FONT, command=Main.show_navigation_dashboard,
              relief="solid", borderwidth=1).pack(side="right")

    # Content
    content = tk.Frame(main_frame, bg=BG_CONTENT, padx=20, pady=20)
    content.pack(fill="both", expand=True)

    tk.Label(content, text="MY COLLECTION", font=FONT_HEADING,
             bg=BG_CONTENT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))

    # Table container
    table_frame = tk.Frame(content, bg=BG_CARD, relief="solid", borderwidth=1)
    table_frame.pack(fill="both", expand=True)
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_columnconfigure(1, weight=1)
    table_frame.grid_columnconfigure(2, weight=1)
    table_frame.grid_columnconfigure(3, weight=1)
    table_frame.grid_rowconfigure(1, weight=1)

    # Headers
    headers = ["USER NAME", "BOOK TITLE", "ADDED DATE", "ACTIONS"]
    for col, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=FONT, bg="#e8d5b0", fg=TEXT_DARK,
                 relief="solid", borderwidth=1, width=20).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    canvas = tk.Canvas(table_frame, bg=BG_CARD, highlightthickness=0)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    rows_frame = tk.Frame(canvas, bg=BG_CARD)
    rows_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    rows_window = canvas.create_window((0, 0), window=rows_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(rows_window, width=event.width))
    canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")
    scrollbar.grid(row=1, column=4, sticky="ns")

    # Load data
    def load_data():
        for widget in rows_frame.winfo_children():
            widget.destroy()

        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.User_Name, c.Book_Title, c.Added_Date, c.Status, c.Collection_ID
                FROM collection c
                ORDER BY c.Added_Date DESC
            """)
            rows = cur.fetchall()

            for idx, row in enumerate(rows):
                uname, btitle, adate, status, rec_id = row

                display_status = "[ACTIVE]" if status == "Active" else "[IN-ACTIVE]"
                status_color = BTN_GREEN if status == "Active" else BTN_RED

                tk.Label(rows_frame, text=uname or "", font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=0, sticky="nsew", padx=1, pady=1)
                tk.Label(rows_frame, text=btitle or "", font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=1, sticky="nsew", padx=1, pady=1)
                tk.Label(rows_frame, text=str(adate or ""), font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=idx, column=2, sticky="nsew", padx=1, pady=1)

                # Status + Delete
                action_frame = tk.Frame(rows_frame, bg="#fff3d4")
                action_frame.grid(row=idx, column=3, sticky="nsew", padx=1, pady=1)
                
                tk.Label(action_frame, text=display_status, bg=status_color, fg=TEXT_DARK,
                         font=FONT, relief="solid", borderwidth=1).pack(pady=1, fill="x")
                tk.Button(action_frame, text="DELETE", bg=BTN_RED, fg="white",
                         font=FONT, relief="solid", borderwidth=1,
                         command=lambda rid=rec_id: delete_record(rid)).pack(pady=1, fill="x")

            # Empty row if no data — improved message
            if not rows:
                tk.Label(rows_frame, text="No books in collection yet.",
                         font=FONT, bg="#fff3d4", fg=TEXT_DARK,
                         relief="solid", borderwidth=1).grid(row=0, column=0, columnspan=4, sticky="nsew", pady=20)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def delete_record(rec_id):
        if not messagebox.askyesno("Confirm", "Delete this record?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM collection WHERE Collection_ID=%s", (rec_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Record removed from collection")
                load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    load_data()
