import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import cv2
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class GatemanLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Gateman Login")

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="user_name", #replace with your database user name
            passwd="your_password", #replace with your database password
            database="database_name" #replace with your database name
        )
        self.cursor = self.db.cursor()

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Create login form
        self.create_login_form()

    def create_login_form(self):
        ttk.Label(self.main_frame, text="Gateman Login", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.main_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        # Get username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check username and password in the database
        sql = "SELECT * FROM gateman WHERE Username = %s AND Password = %s"
        self.cursor.execute(sql, (username, password))
        gateman = self.cursor.fetchone()

        if gateman:
            # Close login window
            self.root.withdraw()
            # Open Gateman Dashboard
            self.open_gateman_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_gateman_dashboard(self, username):
        # Open Gateman Dashboard window
        dashboard_window = tk.Toplevel(self.root)
        GatemanDashboardWindow(dashboard_window, username, self.db)


class GatemanDashboardWindow:
    def __init__(self, root, username, db):
        self.root = root
        self.root.title("Gateman Dashboard")
        self.username = username
        self.db = db
        self.cursor = self.db.cursor()

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Welcome message
        ttk.Label(self.main_frame, text=f"Welcome, {self.username}!", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Create gatepass entry form
        self.create_gatepass_entry_form()

        # Create search form
        self.create_search_form()

        # Create listing button
        ttk.Button(self.main_frame, text="List All Entries", command=self.list_all_entries).grid(row=20, column=0, columnspan=2, pady=10)

        # Logout button
        ttk.Button(self.main_frame, text="Logout", command=self.logout).grid(row=21, column=0, columnspan=2, pady=10)

    def create_gatepass_entry_form(self):
        ttk.Label(self.main_frame, text="Gatepass Entry Form", font=("Arial", 14, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

        # Gateman ID
        ttk.Label(self.main_frame, text="Gateman ID:").grid(row=2, column=0, pady=5, sticky="e")
        self.gateman_id = self.get_gateman_id()
        ttk.Label(self.main_frame, text=self.gateman_id).grid(row=2, column=1, pady=5, sticky="w")

        # Pass Number
        ttk.Label(self.main_frame, text="Pass Number:").grid(row=3, column=0, pady=5, sticky="e")
        pass_number = self.generate_pass_number()
        self.pass_number_label = ttk.Label(self.main_frame, text=pass_number)
        self.pass_number_label.grid(row=3, column=1, pady=5, sticky="w")

        # Date and Time
        ttk.Label(self.main_frame, text="Date and Time:").grid(row=4, column=0, pady=5, sticky="e")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label = ttk.Label(self.main_frame, text=date_time)
        self.date_time_label.grid(row=4, column=1, pady=5, sticky="w")

        # Valid Until
        ttk.Label(self.main_frame, text="Valid Until:").grid(row=5, column=0, pady=5, sticky="e")
        valid_until = (datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
        self.valid_until_label = ttk.Label(self.main_frame, text=valid_until)
        self.valid_until_label.grid(row=5, column=1, pady=5, sticky="w")

        # Contact Number
        ttk.Label(self.main_frame, text="Contact Number:").grid(row=6, column=0, pady=5, sticky="e")
        self.contact_number_entry = ttk.Entry(self.main_frame, width=30)
        self.contact_number_entry.grid(row=6, column=1, pady=5)

        # Visitor Name
        ttk.Label(self.main_frame, text="Visitor Name:").grid(row=7, column=0, pady=5, sticky="e")
        self.visitor_name_entry = ttk.Entry(self.main_frame, width=30)
        self.visitor_name_entry.grid(row=7, column=1, pady=5)

        # Aadhar Card
        ttk.Label(self.main_frame, text="Aadhar Card:").grid(row=8, column=0, pady=5, sticky="e")
        self.aadhar_card_entry = ttk.Entry(self.main_frame, width=30)
        self.aadhar_card_entry.grid(row=8, column=1, pady=5)

        # Company Name
        ttk.Label(self.main_frame, text="Company Name:").grid(row=9, column=0, pady=5, sticky="e")
        self.company_name_entry = ttk.Entry(self.main_frame, width=30)
        self.company_name_entry.grid(row=9, column=1, pady=5)

        # Company Address
        ttk.Label(self.main_frame, text="Company Address:").grid(row=10, column=0, pady=5, sticky="e")
        self.company_address_entry = ttk.Entry(self.main_frame, width=30)
        self.company_address_entry.grid(row=10, column=1, pady=5)

        # Purpose of Visit
        ttk.Label(self.main_frame, text="Purpose of Visit:").grid(row=11, column=0, pady=5, sticky="e")
        self.purpose_entry = ttk.Entry(self.main_frame, width=30)
        self.purpose_entry.grid(row=11, column=1, pady=5)

        # Admin In
        ttk.Label(self.main_frame, text="Admin In:").grid(row=12, column=0, pady=5, sticky="e")
        admin_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.admin_in_label = ttk.Label(self.main_frame, text=admin_in)
        self.admin_in_label.grid(row=12, column=1, pady=5, sticky="w")

        # Officer Name
        ttk.Label(self.main_frame, text="Officer Name:").grid(row=13, column=0, pady=5, sticky="e")
        self.officer_name_entry = ttk.Combobox(self.main_frame, width=27)
        self.officer_name_entry.grid(row=13, column=1, pady=5, sticky="w")

        # Designation
        ttk.Label(self.main_frame, text="Designation:").grid(row=14, column=0, pady=5, sticky="e")
        self.designation_entry = ttk.Combobox(self.main_frame, width=27)
        self.designation_entry.grid(row=14, column=1, pady=5, sticky="w")

        # Vehicle Number
        ttk.Label(self.main_frame, text="Vehicle Number:").grid(row=15, column=0, pady=5, sticky="e")
        self.vehicle_number_entry = ttk.Entry(self.main_frame, width=30)
        self.vehicle_number_entry.grid(row=15, column=1, pady=5)

        ttk.Button(self.main_frame, text="Capture Photo", command=self.capture_photo).grid(row=16, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Submit", command=self.submit_form).grid(row=17, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Print", command=self.print_form).grid(row=18, column=0, columnspan=2, pady=10)

    def create_search_form(self):
        ttk.Label(self.main_frame, text="Search Entry by Pass Number", font=("Arial", 14, "bold")).grid(row=19, column=0, columnspan=2, pady=10)
        self.pass_number_search_entry = ttk.Entry(self.main_frame, width=30)
        self.pass_number_search_entry.grid(row=20, column=0, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Search", command=self.search_by_pass_number).grid(row=20, column=1, padx=5, pady=5)

    def search_by_pass_number(self):
        pass_number = self.pass_number_search_entry.get()
        sql = "SELECT * FROM gatepass_entry WHERE Pass_Number = %s"
        self.cursor.execute(sql, (pass_number,))
        entry = self.cursor.fetchone()
        if entry:
            messagebox.showinfo("Entry Found", f"Pass Number: {entry[2]}\nDate and Time: {entry[3]}\nVisitor Name: {entry[6]}")
        else:
            messagebox.showinfo("Entry Not Found", f"No entry found for Pass Number: {pass_number}")

    def list_all_entries(self):
        sql = "SELECT * FROM gatepass_entry"
        self.cursor.execute(sql)
        entries = self.cursor.fetchall()
        if entries:
            entry_list = "\n".join([f"Pass Number: {entry[2]}, Date and Time: {entry[3]}, Visitor Name: {entry[6]}" for entry in entries])
            messagebox.showinfo("All Entries", entry_list)
        else:
            messagebox.showinfo("No Entries", "No entries found.")

    def logout(self):
        self.root.destroy()
        GatemanLogin(tk.Tk())

    # Other methods remain unchanged

    def get_gateman_id(self):
        # Get Gateman ID based on username
        sql = "SELECT Gateman_ID FROM gateman WHERE Username = %s"
        self.cursor.execute(sql, (self.username,))
        gateman_id = self.cursor.fetchone()[0]
        return gateman_id

    def generate_pass_number(self):
        # Generate pass number based on current year and count of entries for the year
        current_year = datetime.now().year
        sql = "SELECT COUNT(*) FROM gatepass_entry WHERE YEAR(Date_and_Time) = %s"
        self.cursor.execute(sql, (current_year,))
        count = self.cursor.fetchone()[0]
        pass_number = f"{current_year}{count + 1:04d}"
        return pass_number

    def capture_photo(self):
        # Generate a unique filename for the photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f"photo_{timestamp}.png"
        photo_path = os.path.join("captured", photo_filename)

        # Capture photo using OpenCV
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        if return_value:
            cv2.imwrite(photo_path, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            messagebox.showinfo("Capture Photo", "Photo captured successfully!")
            camera.release()
            return photo_path
        else:
            messagebox.showerror("Error", "Failed to capture photo.")

    def submit_form(self):
        # Get form data
        gateman_id = self.gateman_id
        pass_number = self.pass_number_label.cget("text")
        date_time = self.date_time_label.cget("text")
        valid_until = self.valid_until_label.cget("text")
        contact_number = self.contact_number_entry.get()
        visitor_name = self.visitor_name_entry.get()
        aadhar_card = self.aadhar_card_entry.get()
        company_name = self.company_name_entry.get()
        company_address = self.company_address_entry.get()
        purpose = self.purpose_entry.get()
        admin_in = self.admin_in_label.cget("text")
        officer_name = self.officer_name_entry.get()
        designation = self.designation_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        photo_path = self.capture_photo()  # Capture photo and get its path

        # Insert form data into the database
        sql = "INSERT INTO gatepass_entry (Gateman_ID, Pass_Number, Date_and_Time, Valid_Until, Contact_Number, Visitor_Name, Aadhar_Card, Company_Name, Company_Address, Purpose_of_Visit, Admin_In, Officer_Name, Designation, Vehicle_Number, Photo_Path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (gateman_id, pass_number, date_time, valid_until, contact_number, visitor_name, aadhar_card, company_name, company_address, purpose, admin_in, officer_name, designation, vehicle_number, photo_path)
        self.cursor.execute(sql, values)
        self.db.commit()

        # Show success message
        messagebox.showinfo("Success", "Gatepass entry submitted successfully!")

    def print_form(self):
        # Get form data
        gateman_id = self.gateman_id
        pass_number = self.pass_number_label.cget("text")
        date_time = self.date_time_label.cget("text")
        valid_until = self.valid_until_label.cget("text")
        contact_number = self.contact_number_entry.get()
        visitor_name = self.visitor_name_entry.get()
        aadhar_card = self.aadhar_card_entry.get()
        company_name = self.company_name_entry.get()
        company_address = self.company_address_entry.get()
        purpose = self.purpose_entry.get()
        admin_in = self.admin_in_label.cget("text")
        officer_name = self.officer_name_entry.get()
        designation = self.designation_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        photo_path = "temp_photo.png"  # Temporary photo path

        # Generate PDF with form data
        file_path = os.path.join("pdf", f"Gatepass_{pass_number}.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, "ORDNANCE EQUIPMENT FACTORY HAZRATPUR")
        c.drawString(100, 730, "PRINT PASS")
        c.drawString(100, 710, "Gatepass Entry Form")
        c.drawString(100, 690, f"Gateman Name: {self.username}")
        c.drawString(100, 670, f"Pass Number: {pass_number}")
        c.drawString(100, 650, f"Date and Time: {date_time}")
        c.drawString(100, 630, f"Valid Until: {valid_until}")
        c.drawString(100, 610, f"Contact Number: {contact_number}")
        c.drawString(100, 590, f"Visitor Name: {visitor_name}")
        c.drawString(100, 570, f"Aadhar Card: {aadhar_card}")
        c.drawString(100, 550, f"Company Name: {company_name}")
        c.drawString(100, 530, f"Company Address: {company_address}")
        c.drawString(100, 510, f"Purpose of Visit: {purpose}")
        c.drawString(100, 490, f"Admin In: {admin_in}")
        c.drawString(100, 470, f"Officer Name: {officer_name}")
        c.drawString(100, 450, f"Designation: {designation}")
        c.drawString(100, 430, f"Vehicle Number: {vehicle_number}")
        c.drawString(100, 410, f"Photo Path: {photo_path}")  # Add photo path
        c.save()
        messagebox.showinfo("Print", f"Form printed and saved at {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    GatemanLogin(root)
    root.mainloop()
