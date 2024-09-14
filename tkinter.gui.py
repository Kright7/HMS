import tkinter as tk
from tkinter import messagebox, simpledialog, Canvas
from Doctor import Doctor
from Patient import Patient
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")
        self.username = None
        self.password = None
        self.address = None
        self.load_admin_details()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.doctors = Doctor.load_from_file('doctor.txt')
        self.patients = Patient.load_from_file('patient.txt')
        self.selected_patient = tk.IntVar()  # Define selected_patient attribute
        self.selected_doctor = tk.IntVar()   # Define selected_doctor attribute
        self.loading_screen()

    def loading_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Hospital Management System", font=("Helvetica", 24)).pack(pady=20)

        canvas = tk.Canvas(self.main_frame, width=400, height=100)
        canvas.pack(pady=20)

        progress_rect = canvas.create_rectangle(0, 50, 0, 100, fill="blue")
        loading_text = tk.Label(self.main_frame, text="Loading...", font=("Helvetica", 16))
        loading_text.pack(pady=10)

        def update_progress(progress):
            canvas.coords(progress_rect, 0, 50, 4 * progress, 100)
            loading_text.config(text=f"Loading... {progress}%")
            if progress < 100:
                self.root.after(30, update_progress, progress + 1)
            else:
                self.login_screen()

        self.root.after(30, update_progress, 0)

    def login_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Admin Login", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(self.main_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        show_password_checkbox.pack()

        tk.Button(self.main_frame, text="Login", command=self.authenticate).pack(pady=20)

        
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        admin_username, admin_password, _ = self.load_admin_details()

        if username == admin_username and password == admin_password:
            self.main_menu()
        else:
            messagebox.showerror("Login Error", "Invalid Username or Password")

    def main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Hospital Management System", font=("Helvetica", 24)).pack(pady=20)

        operations = [
            "Register/View/Update/Delete Doctor",
            "Add/View Patient",
            "Assign Doctor to a Patient",
            "Discharge Patient",
            "View Discharged Patient",
            "Update Admin Information",
            "Show Patients of the Same Family",
            "Relocate Patient from One Doctor to Another",
            "Add Symptoms",
            "Management Report",
            "Exit"
        ]

        for operation in operations:
            tk.Button(self.main_frame, text=operation, width=40, command=lambda op=operation: self.handle_operation(op)).pack(pady=5)

    def handle_operation(self, operation):
        if operation == "Register/View/Update/Delete Doctor":
            self.doctor_management()
        elif operation == "Add/View Patient":
            self.patient_management()
        elif operation == "Assign Doctor to a Patient":
            self.assign_doctor_to_patient()
        elif operation == "Discharge Patient":
            self.discharge_patient()   
        elif operation == "View Discharged Patient":
            self.view_discharged_patients()
        elif operation == "Update Admin Information":
            self.update_admin_menu()
        
        elif operation == "Show Patients of the Same Family":
            self.family_patients()    
         
        elif operation == "Relocate Patient from One Doctor to Another":
            self.relocate_patient() 
            
        elif operation == "Add Symptoms":
            self.add_symptoms() 
              
        elif operation == "Management Report":
            self.management_report(self.doctors, self.patients)
            
        elif operation == "Exit":
            self.exit_application()
        else:
            messagebox.showinfo("Operation", f"Selected Operation: {operation}")

    def load_admin_details(self):
        try:
            with open('admin.txt', 'r') as file:
                username, password, address = file.read().strip().split(',')
                return username, password, address
        except FileNotFoundError:
            return None, None, None
        
    def save_admin_details(self):
        with open('admin.txt', 'w') as file:
            file.write(f"{self.username},{self.password},{self.address}")
    
    def update_admin_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Update Admin Information", font=("Helvetica", 18)).pack(pady=10)

        tk.Button(self.main_frame, text="Update Username", command=lambda: self.update_admin('username')).pack(pady=5)
        tk.Button(self.main_frame, text="Update Password", command=lambda: self.update_admin('password')).pack(pady=5)
        tk.Button(self.main_frame, text="Update Address", command=lambda: self.update_admin('address')).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def update_admin(self, field):
        new_value = simpledialog.askstring(f"Update {field.capitalize()}", f"Enter the new {field}:", parent=self.root)
        if new_value is not None:  # Check if dialog is canceled
            confirm_value = simpledialog.askstring(f"Confirm {field.capitalize()}", f"Confirm {field}:", parent=self.root)
            if confirm_value is not None:  # Check if dialog is canceled
                if new_value == confirm_value:
                    # Load existing admin details
                    username, password, address = self.load_admin_details()
                    
                    # Update the specified field
                    if field == 'username':
                        username = new_value
                    elif field == 'password':
                        password = new_value
                    elif field == 'address':
                        address = new_value
                    
                    # Save the updated admin details
                    with open('admin.txt', 'w') as file:
                        file.write(f"{username},{password},{address}")
                    
                    messagebox.showinfo("Success", f"{field.capitalize()} updated successfully!")
                else:
                    messagebox.showerror("Error", f"{field.capitalize()} not matched.")
                
    def doctor_management(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Doctor Management", font=("Helvetica", 18)).pack(pady=10)

        tk.Button(self.main_frame, text="Register Doctor", width=30, command=self.register_doctor).pack(pady=5)
        tk.Button(self.main_frame, text="View Doctors", width=30, command=self.view_doctors).pack(pady=5)
        tk.Button(self.main_frame, text="Update Doctor", width=30, command=self.update_doctor).pack(pady=5)
        tk.Button(self.main_frame, text="Delete Doctor", width=30, command=self.delete_doctor).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Menu", width=30, command=self.main_menu).pack(pady=5)

    def register_doctor(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Register Doctor", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="First Name").pack()
        self.first_name_entry = tk.Entry(self.main_frame)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Surname").pack()
        self.surname_entry = tk.Entry(self.main_frame)
        self.surname_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Speciality").pack()
        self.speciality_entry = tk.Entry(self.main_frame)
        self.speciality_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Submit", command=self.save_doctor).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Doctor Management", command=self.doctor_management).pack(pady=5)

    def save_doctor(self):
        first_name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        speciality = self.speciality_entry.get()

        if first_name and surname and speciality:
            name_exists = any(d.get_first_name() == first_name and d.get_surname() == surname for d in self.doctors)
            if name_exists:
                messagebox.showerror('Error', 'Name already exists.')
            else:
                new_doctor = Doctor(first_name, surname, speciality)
                self.doctors.append(new_doctor)
                Doctor.save_to_file('doctor.txt', self.doctors)
                messagebox.showinfo('Success', 'Doctor registered successfully!')
                self.doctor_management()
        else:
            messagebox.showerror('Error', 'All fields are required!')

    def view_doctors(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Doctors List", font=("Helvetica", 18)).pack(pady=10)

        doctors_list = tk.Listbox(self.main_frame, width=50, height=10)
        doctors_list.pack(pady=5)

        for idx, doctor in enumerate(self.doctors):
            doctors_list.insert(tk.END, f"{idx+1}. {doctor.get_first_name()} {doctor.get_surname()} - {doctor.get_speciality()}")

        tk.Button(self.main_frame, text="Back to Doctor Management", command=self.doctor_management).pack(pady=5)

    def update_doctor(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Update Doctor", font=("Helvetica", 18)).pack(pady=10)

        # Display the list of doctors with their IDs
        tk.Label(self.main_frame, text="List of Doctors:", font=("Helvetica", 12)).pack()
        doctors = Doctor.load_from_file('doctor.txt')
        for i, doctor in enumerate(doctors, start=1):
            tk.Label(self.main_frame, text=f"{i}. {doctor.full_name()} - ID: {i}", font=("Helvetica", 10)).pack()

        tk.Label(self.main_frame, text="Doctor ID").pack()
        self.doctor_id_entry = tk.Entry(self.main_frame)
        self.doctor_id_entry.pack(pady=5)

        tk.Label(self.main_frame, text="New First Name").pack()
        self.first_name_entry = tk.Entry(self.main_frame)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="New Surname").pack()
        self.surname_entry = tk.Entry(self.main_frame)
        self.surname_entry.pack(pady=5)

        tk.Label(self.main_frame, text="New Speciality").pack()
        self.speciality_entry = tk.Entry(self.main_frame)
        self.speciality_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Update", command=self.modify_doctor).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Doctor Management", command=self.doctor_management).pack(pady=5)
        
    def modify_doctor(self):
        doctor_id = self.doctor_id_entry.get()
        first_name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        speciality = self.speciality_entry.get()

        try:
            index = int(doctor_id) - 1
            if index < 0 or index >= len(self.doctors):
                messagebox.showerror('Error', 'Doctor not found!')
                return

            if first_name:
                self.doctors[index].set_first_name(first_name)
            if surname:
                self.doctors[index].set_surname(surname)
            if speciality:
                self.doctors[index].set_speciality(speciality)

            Doctor.save_to_file('doctor.txt', self.doctors)
            messagebox.showinfo('Success', 'Doctor updated successfully!')
            self.doctor_management()

        except ValueError:
            messagebox.showerror('Error', 'Invalid ID!')

    def delete_doctor(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Delete Doctor", font=("Helvetica", 18)).pack(pady=10)

        # Display the list of doctors with their IDs
        tk.Label(self.main_frame, text="List of Doctors:", font=("Helvetica", 12)).pack()
        doctors = Doctor.load_from_file('doctor.txt')
        for i, doctor in enumerate(doctors, start=1):
            tk.Label(self.main_frame, text=f"{i}. {doctor.full_name()} - ID: {i}", font=("Helvetica", 10)).pack()

        tk.Label(self.main_frame, text="Doctor ID").pack()
        self.doctor_id_entry = tk.Entry(self.main_frame)
        self.doctor_id_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Delete", command=self.remove_doctor).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Doctor Management", command=self.doctor_management).pack(pady=5)
    def remove_doctor(self):
        doctor_id = self.doctor_id_entry.get()
        try:
            index = int(doctor_id) - 1
            if index < 0 or index >= len(self.doctors):
                messagebox.showerror('Error', 'Doctor not found!')
                return

            del self.doctors[index]
            Doctor.save_to_file('doctor.txt', self.doctors)
            messagebox.showinfo('Success', 'Doctor deleted successfully!')
            self.doctor_management()

        except ValueError:
            messagebox.showerror('Error', 'Invalid ID!')

    def patient_management(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Patient Management", font=("Helvetica", 18)).pack(pady=10)

        tk.Button(self.main_frame, text="Add Patient", width=30, command=self.add_patient).pack(pady=5)
        tk.Button(self.main_frame, text="View Patients", width=30, command=self.view_patients).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Menu", width=30, command=self.main_menu).pack(pady=5)

    def add_patient(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Add Patient", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="First Name").pack()
        self.first_name_entry = tk.Entry(self.main_frame)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Surname").pack()
        self.surname_entry = tk.Entry(self.main_frame)
        self.surname_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Age").pack()
        self.age_entry = tk.Entry(self.main_frame)
        self.age_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Mobile").pack()
        self.mobile_entry = tk.Entry(self.main_frame)
        self.mobile_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Postcode").pack()
        self.postcode_entry = tk.Entry(self.main_frame)
        self.postcode_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Symptoms (comma-separated)").pack()
        self.symptoms_entry = tk.Entry(self.main_frame)
        self.symptoms_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Submit", command=self.save_patient).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Patient Management", command=self.patient_management).pack(pady=5)

    def save_patient(self):
        first_name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        age = self.age_entry.get()
        mobile = self.mobile_entry.get()
        postcode = self.postcode_entry.get()
        symptoms = self.symptoms_entry.get().split(',')

        if first_name and surname and age and mobile and postcode and symptoms:
            new_patient = Patient(first_name, surname, age, mobile, postcode)
            new_patient.set_symptoms(symptoms)

            patients = Patient.load_from_file('patient.txt')
            patients.append(new_patient)
            Patient.save_to_file('patient.txt', patients)
            messagebox.showinfo('Success', 'Patient added successfully!')
            self.patient_management()
        else:
            messagebox.showerror('Error', 'All fields are required!')
            
    def view_patients(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Patients List", font=("Helvetica", 18)).pack(pady=10)

        patients_list = tk.Listbox(self.main_frame, width=75, height=10)
        patients_list.pack(pady=5)

        self.patients = Patient.load_from_file('patient.txt')
        for idx, patient in enumerate(self.patients):
            patients_list.insert(tk.END, f"{idx+1}. {patient.get_first_name()} {patient.get_surname()} - {patient.get_age()}, {patient.get_mobile()}, {patient.get_postcode()}, Symptoms: {', '.join(patient.print_symptoms())}")

        tk.Button(self.main_frame, text="Back to Patient Management", command=self.patient_management).pack(pady=5)

    
    
    def assign_doctor_to_patient(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Assign Doctor to a Patient", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Select a Patient:", font=("Helvetica", 12)).pack()
        self.selected_patient = tk.StringVar()
        patients = Patient.load_from_file('patient.txt')
        patient_options = [patient.full_name() for patient in patients]
        tk.OptionMenu(self.main_frame, self.selected_patient, *patient_options).pack(pady=5)

        tk.Label(self.main_frame, text="Select a Doctor:", font=("Helvetica", 12)).pack()
        self.selected_doctor = tk.StringVar()
        doctors = Doctor.load_from_file('doctor.txt')
        doctor_options = [doctor.full_name() for doctor in doctors]
        tk.OptionMenu(self.main_frame, self.selected_doctor, *doctor_options).pack(pady=5)

        tk.Button(self.main_frame, text="Assign", command=self.confirm_assignment).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def confirm_assignment(self):
        selected_patient_name = self.selected_patient.get()
        selected_doctor_name = self.selected_doctor.get()

        if not selected_patient_name or not selected_doctor_name:
            messagebox.showerror('Error', 'Please select both a patient and a doctor.')
            return

        patients = Patient.load_from_file('patient.txt')
        doctors = Doctor.load_from_file('doctor.txt')
        selected_patient = next((p for p in patients if p.full_name() == selected_patient_name), None)
        selected_doctor = next((d for d in doctors if d.full_name() == selected_doctor_name), None)

        if not selected_patient or not selected_doctor:
            messagebox.showerror('Error', 'Selected patient or doctor not found.')
            return

        if selected_patient.get_doctor():
            messagebox.showinfo('Info', 'This patient is already assigned to a doctor.')
            return

        # Assuming appointment date needs to be entered
        appointment_date = simpledialog.askstring("Appointment Date", "Enter appointment date (YYYY-MM-DD HH:MM):")
        if not appointment_date:
            return  # User canceled

        try:
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror('Error', 'Invalid date format. Please use YYYY-MM-DD HH:MM')
            return

        selected_patient.link(selected_doctor.full_name(), appointment_date)
        selected_doctor.add_appointment(selected_patient.full_name(), appointment_date)

        # Save changes to files
        Patient.save_to_file('patient.txt', patients)
        Doctor.save_to_file('doctor.txt', doctors)

        messagebox.showinfo('Success', 'Doctor assigned to patient successfully!')
        self.main_menu()



    def discharge_patient(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Discharge Patient", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Select a Patient:", font=("Helvetica", 12)).pack()
        self.selected_patient = tk.StringVar()
        patients = Patient.load_from_file('patient.txt')
        patient_options = []
        for patient in patients:
            patient_options.append(patient.full_name())
        tk.OptionMenu(self.main_frame, self.selected_patient, *patient_options).pack(pady=5)

        tk.Button(self.main_frame, text="Discharge", command=self.confirm_discharge).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def confirm_discharge(self):
        selected_patient_name = self.selected_patient.get()

        if not selected_patient_name:
            messagebox.showerror('Error', 'Please select a patient.')
            return

        patients = Patient.load_from_file('patient.txt')
        discharged_patients = Patient.load_from_file('discharged_patient.txt')
        selected_patient = next((p for p in patients if p.full_name() == selected_patient_name), None)

        if not selected_patient:
            messagebox.showerror('Error', 'Selected patient not found.')
            return

        patients.remove(selected_patient)
        discharged_patients.append(selected_patient)

        # Save changes to files
        Patient.save_to_file('patient.txt', patients)
        Patient.save_to_file('discharged_patient.txt', discharged_patients)

        messagebox.showinfo('Success', 'Patient discharged successfully!')
        self.main_menu()

    def view_discharged_patients(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Discharged Patients", font=("Helvetica", 18)).pack(pady=10)

        discharged_patients = Patient.load_from_file('discharged_patient.txt')

        if not discharged_patients:
            tk.Label(self.main_frame, text="No discharged patients.", font=("Helvetica", 12)).pack(pady=5)
        else:
            discharged_patients_list = tk.Listbox(self.main_frame, width=50, height=10)
            discharged_patients_list.pack(pady=5)

            for idx, patient in enumerate(discharged_patients):
                discharged_patients_list.insert(tk.END, f"{idx+1}. {patient.full_name()}. {patient.get_age()}. {patient.get_mobile()}. {patient.get_postcode()}. {', '.join(patient.print_symptoms())}")
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)


    def family_patients(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Patients of the Same Family", font=("Helvetica", 18)).pack(pady=10)

        patients = Patient.load_from_file('patient.txt')
        temp_last_name = {}

        for patient in patients:
            patient_last_name = patient.get_surname()
            
            if patient_last_name not in temp_last_name:
                temp_last_name[patient_last_name] = [patient]
            else:
                temp_last_name[patient_last_name].append(patient)
        
        for last_name, patients in temp_last_name.items():
            family_label = tk.Label(self.main_frame, text=f"The patients with family name '{last_name}' are:", font=("Helvetica", 12))
            family_label.pack()
            for patient in patients:
                patient_label = tk.Label(self.main_frame, text=f"- {patient.full_name()}", font=("Helvetica", 10))
                patient_label.pack()
                
        tk.Button(self.main_frame, text="Back to Menu", width=30, command=self.main_menu).pack(pady=5)

    def relocate_patient(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Relocate Patient", font=("Helvetica", 18)).pack(pady=10)

        patients = Patient.load_from_file('patient.txt')
        assigned_patients = [patient for patient in patients if patient.get_doctor()]
        
        if not assigned_patients:
            tk.Label(self.main_frame, text="No patients are currently assigned to a doctor.", font=("Helvetica", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)
            return

        tk.Label(self.main_frame, text="Select a Patient:", font=("Helvetica", 12)).pack()
        self.selected_patient = tk.StringVar()
        patient_options = [patient.full_name() for patient in assigned_patients]
        tk.OptionMenu(self.main_frame, self.selected_patient, *patient_options).pack(pady=5)

        tk.Label(self.main_frame, text="Select a Doctor:", font=("Helvetica", 12)).pack()
        self.selected_doctor = tk.StringVar()
        doctors = Doctor.load_from_file('doctor.txt')
        doctor_options = [doctor.full_name() for doctor in doctors]
        tk.OptionMenu(self.main_frame, self.selected_doctor, *doctor_options).pack(pady=5)

        tk.Button(self.main_frame, text="Relocate", command=self.confirm_relocation).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def confirm_relocation(self):
        selected_patient_name = self.selected_patient.get()
        selected_doctor_name = self.selected_doctor.get()

        if not selected_patient_name or not selected_doctor_name:
            messagebox.showerror('Error', 'Please select both a patient and a doctor.')
            return

        patients = Patient.load_from_file('patient.txt')
        doctors = Doctor.load_from_file('doctor.txt')
        selected_patient = next((p for p in patients if p.full_name() == selected_patient_name), None)
        selected_doctor = next((d for d in doctors if d.full_name() == selected_doctor_name), None)

        if not selected_patient or not selected_doctor:
            messagebox.showerror('Error', 'Selected patient or doctor not found.')
            return

        # Assuming appointment date needs to be entered
        appointment_date = simpledialog.askstring("Appointment Date", "Enter appointment date (YYYY-MM-DD HH:MM):")
        if not appointment_date:
            return  # User canceled

        try:
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror('Error', 'Invalid date format. Please use YYYY-MM-DD HH:MM')
            return

        # Remove patient from old doctor and assign to new doctor
        old_doctor_name = selected_patient.get_doctor()
        if old_doctor_name:
            old_doctor = next((d for d in doctors if d.full_name() == old_doctor_name), None)
            if old_doctor:
                old_doctor.remove_patient(selected_patient.full_name())

        selected_patient.link(selected_doctor.full_name(), appointment_date)
        selected_doctor.add_patient(selected_patient.full_name(), appointment_date)

        # Save changes to files
        Patient.save_to_file('patient.txt', patients)
        Doctor.save_to_file('doctor.txt', doctors)

        messagebox.showinfo('Success', 'Patient relocated successfully!')
        self.main_menu()

    def add_symptoms(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Add Symptoms", font=("Helvetica", 18)).pack(pady=10)

        patients = Patient.load_from_file("patient.txt")

        tk.Label(self.main_frame, text="Select a Patient:", font=("Helvetica", 12)).pack()
        self.selected_patient = tk.StringVar()
        patient_options = [patient.full_name() for patient in patients]
        tk.OptionMenu(self.main_frame, self.selected_patient, *patient_options).pack(pady=5)

        tk.Button(self.main_frame, text="Confirm", command=self.confirm_symptoms).pack(pady=20)
        tk.Button(self.main_frame, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def confirm_symptoms(self):
        selected_patient_name = self.selected_patient.get()

        if not selected_patient_name:
            messagebox.showerror('Error', 'Please select a patient.')
            return

        patients = Patient.load_from_file('patient.txt')
        selected_patient = next((p for p in patients if p.full_name() == selected_patient_name), None)

        if not selected_patient:
            messagebox.showerror('Error', 'Selected patient not found.')
            return

        current_symptoms = selected_patient.print_symptoms()
        if current_symptoms:
            messagebox.showinfo('Current Symptoms', '\n'.join(current_symptoms))

        add_symptoms_input = simpledialog.askstring("Add Symptoms", "Enter new symptoms separated by commas:")

        if not add_symptoms_input:
            return 

        new_symptoms = [symptom.strip() for symptom in add_symptoms_input.split(',') if symptom.strip()]
        selected_patient.add_symptoms(new_symptoms)
        Patient.save_to_file("patient.txt", patients)

        messagebox.showinfo('Success', 'Symptoms updated successfully!')
        self.main_menu()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def management_report(self, doctors, patients):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Management Report", font=("Helvetica", 18)).pack(pady=10)

        def total_doctors():
            messagebox.showinfo("Total Doctors", f"The total number of doctors is {len(doctors)}")

        def total_patients_per_doctor():
            doctor_patient_count = {doctor.full_name(): 0 for doctor in doctors}
            for patient in patients:
                doctor_name = patient.get_doctor()
                if doctor_name in doctor_patient_count:
                    doctor_patient_count[doctor_name] += 1

            messagebox.showinfo("Patients per Doctor", "\n".join([f"{doctor}: {count}" for doctor, count in doctor_patient_count.items()]))

            plt.figure(figsize=(12, 6))
            plt.bar(doctor_patient_count.keys(), doctor_patient_count.values())
            plt.xlabel('Doctor')
            plt.ylabel('Number of Patients')
            plt.title('Total Number of Patients per Doctor')
            plt.xticks(rotation=45)
            plt.show()

        def total_appointments_per_month_per_doctor():
            doctor_appointment_count = defaultdict(int)
            for doctor in doctors:
                appointments = doctor.get_appointments()
                for appointment_date in appointments.values():
                    month_year = appointment_date.strftime("%B %Y")
                    doctor_appointment_count[(doctor.full_name(), month_year)] += 1

            messagebox.showinfo("Appointments per Month per Doctor", "\n".join([f"{doctor}, {month_year}: {count}" for (doctor, month_year), count in doctor_appointment_count.items()]))

            if doctor_appointment_count:
                doctor_names, months_years, counts = zip(*[(d, my, c) for (d, my), c in doctor_appointment_count.items()])
                for doctor_name in set(doctor_names):
                    plt.plot(months_years, [counts[i] for i in range(len(counts)) if doctor_names[i] == doctor_name], label=doctor_name)
                plt.xlabel('Month')
                plt.ylabel('Number of Appointments')
                plt.title('Total Number of Appointments per Month per Doctor')
                plt.legend()
                plt.xticks(rotation=45)
                plt.show()

        def total_patients_based_on_illness():
            total_number_of_patients_based_on_illness = {}
            for patient in patients:
                patient_symptoms = patient.print_symptoms()
                for symptom in patient_symptoms:
                    total_number_of_patients_based_on_illness[symptom] = total_number_of_patients_based_on_illness.get(symptom, 0) + 1

            messagebox.showinfo("Patients based on Illness", "\n".join([f"{symptom}: {count}" for symptom, count in total_number_of_patients_based_on_illness.items()]))

            if total_number_of_patients_based_on_illness:
                labels = total_number_of_patients_based_on_illness.keys()
                sizes = total_number_of_patients_based_on_illness.values()
                plt.figure(figsize=(12, 6))
                plt.pie(sizes, labels=labels, autopct='%1.1f%%')
                plt.title('Total Number of Patients based on Illness Type')
                plt.axis('equal')
                plt.show()
                
        def back_to_menu():
            self.clear_main_frame()
            self.main_menu()
            
        tk.Button(self.main_frame, text="Total Doctors", command=total_doctors).pack(pady=5)
        tk.Button(self.main_frame, text="Total Patients per Doctor", command=total_patients_per_doctor).pack(pady=5)
        tk.Button(self.main_frame, text="Total Appointments per Month per Doctor", command=total_appointments_per_month_per_doctor).pack(pady=5)
        tk.Button(self.main_frame, text="Total Patients based on Illness", command=total_patients_based_on_illness).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Menu", command = back_to_menu).pack(pady=5)

        
    def exit_application(self):
        print("The system is going to be off:")
        print("Bye bye")

        messagebox.showinfo("Exit", "The system is going to be off. Bye bye")

        root.destroy()

root = tk.Tk()
app = HospitalManagementSystem(root)
root.mainloop()
