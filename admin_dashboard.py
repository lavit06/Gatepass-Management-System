import tkinter as tk
from tkinter import ttk
import mysql.connector


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="oefhz_gp"
        )
        self.cursor = self.db.cursor()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        self.create_gateman_form()

    def create_gateman_form(self):
        ttk.Label(self.main_frame, text="Add Gateman Account", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ttk.Label(self.main_frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.main_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, columnspan=2, sticky="w")
        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, columnspan=2, sticky="w")
        ttk.Button(self.main_frame, text="Add Gateman", command=self.add_gateman).grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        ttk.Button(self.main_frame, text="View All Gatemen", command=self.view_all_gatemen).grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")
        ttk.Button(self.main_frame, text="Search Entries by Pass Number", command=self.search_entry).grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

    def add_gateman(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            sql = "INSERT INTO gateman (Username, Password) VALUES (%s, %s)"
            values = (username, password)
            self.cursor.execute(sql, values)
            self.db.commit()
            print("Gateman account added successfully!")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        except mysql.connector.Error as e:
            print("Error adding gateman account:", e)

    def view_all_gatemen(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="All Gatemen", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        sql = "SELECT * FROM gateman"
        self.cursor.execute(sql)
        gatemen = self.cursor.fetchall()
        tree = ttk.Treeview(self.main_frame, columns=("Username", "Password"), show="headings")
        tree.heading("#1", text="Username")
        tree.heading("#2", text="Password")
        for gateman in gatemen:
            tree.insert("", "end", values=gateman[1:])
        tree.grid(row=1, column=0, columnspan=3, pady=5)
        ttk.Button(self.main_frame, text="Home", command=self.create_gateman_form).grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

    def search_entry(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Search Entries by Pass Number", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        ttk.Label(self.main_frame, text="Pass Number:").grid(row=1, column=0, pady=5, sticky="e")
        self.pass_number_entry = ttk.Entry(self.main_frame, width=30)
        self.pass_number_entry.grid(row=1, column=1, pady=5, columnspan=2, sticky="w")
        ttk.Button(self.main_frame, text="Search", command=self.search_result).grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")
        ttk.Button(self.main_frame, text="Show All Entries", command=self.show_all_entries).grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        ttk.Button(self.main_frame, text="Home", command=self.create_gateman_form).grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

    def search_result(self):
        pass_number = self.pass_number_entry.get()
        if pass_number:
            self.clear_main_frame()
            ttk.Label(self.main_frame, text=f"Search Result for Pass Number: {pass_number}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
            sql = "SELECT * FROM gatepass_entry WHERE Pass_Number = %s"
            self.cursor.execute(sql, (pass_number,))
            entries = self.cursor.fetchall()
            headers = ("Gateman ID", "Pass Number", "Date and Time", "Valid Until", "Contact Number", "Visitor Name", "Aadhar Card", "Company Name", "Company Address", "Purpose of Visit", "Admin In", "Officer Name", "Designation", "Vehicle Number", "Photo Path")
            tree = ttk.Treeview(self.main_frame, columns=headers, show="headings")
            for col, header in enumerate(headers):
                tree.heading(col, text=header)
                tree.column(col, width=120)  # Adjust column width
            for entry in entries:
                tree.insert("", "end", values=entry)
            tree.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")
        else:
            print("Pass number is required for search.")

    def show_all_entries(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="All Entries", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        sql = "SELECT * FROM gatepass_entry"
        self.cursor.execute(sql)
        entries = self.cursor.fetchall()
        headers = ("Gateman ID", "Pass Number", "Date and Time", "Valid Until", "Contact Number", "Visitor Name", "Aadhar Card", "Company Name", "Company Address", "Purpose of Visit", "Admin In", "Officer Name", "Designation", "Vehicle Number", "Photo Path")
        tree = ttk.Treeview(self.main_frame, columns=headers, show="headings")
        for col, header in enumerate(headers):
            tree.heading(col, text=header)
            tree.column(col, width=120)  # Adjust column width
        for entry in entries:
            tree.insert("", "end", values=entry)
        tree.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")
        ttk.Button(self.main_frame, text="Home", command=self.create_gateman_form).grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
