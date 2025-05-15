import sqlite3
from tkinter import *
from tkinter import ttk

# Create the admin window
admin = Tk()
admin.geometry("800x500")
admin.title("Admin Panel")
admin.resizable(0, 0)

# Connect to SQLite Database
conn = sqlite3.connect("./Database/store.db")  # Change to your actual database name
cursor = conn.cursor()

# Fetch all data from a table
table_name = "employee"  # Change this to your table name
cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()

# Get column names dynamically
cursor.execute(f"PRAGMA table_info({table_name})")
columns = [column[1] for column in cursor.fetchall()]

conn.close()

# Create Table Display
frame = Frame(admin)
frame.pack(fill=BOTH, expand=1)

tree = ttk.Treeview(frame, columns=columns, show="headings")

# Add column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)  # Adjust column width

# Insert data into the table
for row in rows:
    tree.insert("", "end", values=row)

tree.pack(fill=BOTH, expand=1)

# Exit Button
def exit_admin():
    admin.destroy()

btn_exit = Button(admin, text="Exit", command=exit_admin)
btn_exit.pack(pady=10)

admin.mainloop()
