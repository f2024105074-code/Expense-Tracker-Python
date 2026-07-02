import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


# 1. Database Initialization
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()

# 2. Main Window Setup
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("600x500")

# UI Inputs
lbl_amount = tk.Label(root, text="Amount (Rs.):", font=("Arial", 12))
lbl_amount.pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

lbl_category = tk.Label(root, text="Category:", font=("Arial", 12))
lbl_category.pack(pady=5)
category_box = ttk.Combobox(
    root,
    values=["Food", "Transport", "Entertainment", "Bills", "Others"],
    font=("Arial", 12),
)
category_box.pack(pady=5)
category_box.set("Food")


# 3. Functions for Logic
def add_expense():
    amount = entry_amount.get()
    category = category_box.get()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not amount:
        messagebox.showerror("Error", "Please enter an amount!")
        return

    try:
        amount = float(amount)
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date_now),
        )
        conn.commit()
        conn.close()

        entry_amount.delete(0, tk.END)
        messagebox.showinfo("Success", "Expense added successfully!")
        view_expenses()
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")


def view_expenses():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    rows = cursor.fetchall()

    total = 0
    for row in rows:
        tree.insert("", tk.END, values=(row[1], row[2], row[3]))
        total += row[1]

    conn.close()
    lbl_total.config(text=f"Total Expenses: Rs. {total}")

    # --- Member 1: Delete Selected Expense Function ---
    def delete_expense():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an expense from the list to delete!")
            return

        item_details = tree.item(selected_item)
        values = item_details['values']

        if values:
            amount_to_del = values[0]
            category_to_del = values[1]
            date_to_del = values[2]

            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM expenses 
                WHERE amount = ? AND category = ? AND date = ?
            """, (amount_to_del, category_to_del, date_to_del))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Expense deleted successfully!")
            view_expenses()


def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense from the list to delete!")
        return

    item_details = tree.item(selected_item)
    values = item_details['values']

    if values:
        amount_to_del = values[0]
        category_to_del = values[1]
        date_to_del = values[2]

        import sqlite3
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM expenses 
            WHERE amount = ? AND category = ? AND date = ?
        """, (amount_to_del, category_to_del, date_to_del))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expense deleted successfully!")
        view_expenses()

# Buttons and Table UI
btn_add = tk.Button(
    root, text="Add Expense", command=add_expense, font=("Arial", 12), bg="green", fg="white"
)
btn_add.pack(pady=10)

lbl_total = tk.Label(root, text="Total Expenses: Rs. 0", font=("Arial", 12, "bold"))
lbl_total.pack(pady=5)
# Delete Button UI
btn_delete = tk.Button(root, text="Delete Selected", command=delete_expense, font=("Arial", 12), bg="red", fg="white")
btn_delete.pack(pady=5)
tree = ttk.Treeview(root, columns=("Amount", "Category", "Date"), show="headings", height=8)
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Date", text="Date")
tree.pack(pady=10, fill=tk.X, padx=20)

view_expenses()
root.mainloop()