import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


# 1. DATABASE INITIALIZATION

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


# 2. MAIN WINDOW SETUP & STYLING

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("600x650")
root.configure(bg="#f0f0f0")  # Background styling


# 3. FUNCTIONS FOR LOGIC


# --- Core Function: Add Expense ---
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


# --- Core Function: View & Refresh Expenses ---
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

    # ---  Delete Selected Expense Function ---
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

# --- Delete Selected Expense Function ---
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror(
            "Error", "Please select an expense from the list to delete!"
        )
        return

    item_details = tree.item(selected_item)
    values = item_details["values"]

    if values:
        amount_to_del = values[0]
        category_to_del = values[1]
        date_to_del = values[2]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM expenses 
            WHERE amount = ? AND category = ? AND date = ?
        """,
            (amount_to_del, category_to_del, date_to_del),
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expense deleted successfully!")
        view_expenses()


# Clear All Expenses Function
def clear_all_expenses():
    confirm = messagebox.askyesno(
        "Confirm", "Are you sure you want to delete ALL expenses?"
    )

    if confirm:
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "All expenses cleared!")
        view_expenses()



# 4. USER INTERFACE (UI) ELEMENTS

# Inputs Section
lbl_amount = tk.Label(root, text="Amount (Rs.):", font=("Arial", 12), bg="#f0f0f0")
lbl_amount.pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

lbl_category = tk.Label(root, text="Category:", font=("Arial", 12), bg="#f0f0f0")
lbl_category.pack(pady=5)
category_box = ttk.Combobox(
    root,
    values=["Food", "Transport", "Entertainment", "Bills", "Others"],
    font=("Arial", 12),
)
category_box.pack(pady=5)
category_box.set("Food")


# Buttons Section
btn_add = tk.Button(
    root,
    text="Add Expense",
    command=add_expense,
    font=("Arial", 12),
    bg="green",
    fg="white",
    width=20,
)
btn_add.pack(pady=5)

#  Button
btn_delete = tk.Button(
    root,
    text="Delete Selected",
    command=delete_expense,
    font=("Arial", 12),
    bg="red",
    fg="white",
    width=20,
)
btn_delete.pack(pady=5)

#  Button
btn_clear = tk.Button(
    root,
    text="Clear All",
    command=clear_all_expenses,
    font=("Arial", 12),
    bg="orange",
    fg="black",
    width=20,
)
btn_clear.pack(pady=5)

# Total Display Label
lbl_total = tk.Label(
    root, text="Total Expenses: Rs. 0", font=("Arial", 12, "bold"), bg="#f0f0f0"
)
lbl_total.pack(pady=10)

# Table / List View Section
tree = ttk.Treeview(
    root, columns=("Amount", "Category", "Date"), show="headings", height=8
)

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

# Load data on start and run application
view_expenses()
root.mainloop()