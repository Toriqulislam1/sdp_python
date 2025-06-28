import sqlite3
from tkinter import *
from tkinter import ttk

# Create main admin window
admin = Tk()
admin.geometry("900x600")
admin.title("Admin Panel")
admin.resizable(0, 0)

# Connect to SQLite database
db_path = "./Database/store.db"  # Change path if needed
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [table[0] for table in cursor.fetchall()]
conn.close()

# Dropdown Label
label = Label(admin, text="Select Table:", font=("Arial", 12))
label.pack(pady=10)

# Table selection dropdown
selected_table = StringVar()
dropdown = ttk.Combobox(admin, textvariable=selected_table, values=tables, state="readonly", width=40)
dropdown.pack()

# Frame to hold Treeview
frame = Frame(admin)
frame.pack(fill=BOTH, expand=1, padx=20, pady=20)

tree = ttk.Treeview(frame, show="headings")
tree.pack(fill=BOTH, expand=1, side=LEFT)

scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)


# Function to load selected table data
def load_table_data(event=None):
    table_name = selected_table.get()

    # Clear existing tree columns
    for col in tree["columns"]:
        tree.heading(col, text="")
    tree.delete(*tree.get_children())

    # Fetch column names
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    tree["columns"] = columns

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Fetch and display table data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    conn.close()


dropdown.bind("<<ComboboxSelected>>", load_table_data)


# Exit Button
def exit_admin():
    admin.destroy()

btn_exit = Button(admin, text="Exit", font=("Arial", 12), command=exit_admin, bg="#d9534f", fg="white")
btn_exit.pack(pady=10)

admin.mainloop()
