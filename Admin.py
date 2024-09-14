from Doctor import *
from Patient import *
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

doctors =[]
patients = []
discharged_patients = []


class Admin:
    def __init__(self, username, password, address=''):
        self.__username = username
        self.__password = password
        self.__address = address

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password



    def login(self):
        print("-----Login-----")
        
        # Load admin details from file
        admin_username, admin_password, _ = self.load_admin_details()

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # Check if input username and password match admin details loaded from file
        if username == admin_username and password == admin_password:
            return True
        else:
            return False

    def admin_details(self):
        if self.__username is None or self.__password is None or self.__address is None:
            # Load admin details from file if not already loaded
            self.__username, self.__password, self.__address = self.load_admin_details()
            
        print(f"Username : {self.__username}")
        print(f"Password : {self.__password}")
        print(f"Address : {self.__address}")

    def save_admin_details(self):
        with open('admin.txt', 'w') as file:
            file.write(f"{self.__username},{self.__password},{self.__address}")

    def load_admin_details(self):
        try:
            with open('admin.txt', 'r') as file:
                username, password, address = file.read().strip().split(',')
                return username, password, address
        except FileNotFoundError:
            return None, None, None

    def update_details(self):
        print('Choose the field to be updated:')
        print('1 Username')
        print('2 Password')
        print('3 Address')
        op = int(input('Input: '))

        try:
            if op == 1:
                self.load_admin_details()
                new_username = input('Enter the new username: ')
                confirm_username = input('Confirm username: ')
                if new_username == confirm_username:
                    print("Username matched.")
                    self.__username = new_username
                    print("Username updated.")
                    self.admin_details()
                    self.save_admin_details()  # Update admin details in the file
                else:
                    print("Username not matched.")

            elif op == 2:
                self.load_admin_details()
                new_password = input('Enter the new password: ')
                if new_password == input('Enter the new password again: '):
                    self.__password = new_password
                    print("Password updated.")
                    self.admin_details()
                    self.save_admin_details()  # Update admin details in the file

            elif op == 3:
                self.load_admin_details()
                new_address = input('Enter the new address: ')
                if new_address == input('Enter the new address again: '):
                    self.__address = new_address
                    print("Address updated.")
                    self.admin_details()
                    self.save_admin_details()  # Update admin details in the file

            else:
                raise ValueError("Invalid choice")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def find_index(self,index,doctors):
        if index in range(0,len(doctors)):
            return True
        else:
            return False
        
    def get_doctor_details(self):
        first_name = input("Enter doctor's first name: ")
        last_name = input("Enter doctor's last name: ")
        speciality = input("Mention the doctor's speciality: ")
        return (first_name, last_name, speciality)

    def view(self, list1):
        for idx, list1 in enumerate(list1, 1):
            print(f'{idx:<4} | {list1}')


    def doctor_management(self, doctors):
        while True:
            print("-----Doctor Management-----")
            print('Choose the operation:')
            print(' 1 - Register')
            print(' 2 - View')
            print(' 3 - Update')
            print(' 4 - Delete')
            print(' 0 - Back ')
            try:
                op = int(input("Input: "))
            except ValueError:
                print("Invalid choice. Please choose a number.")
                continue

            if op == 1:
                print("-----Register-----")
                print("Enter the doctor's details:")
                first_name, surname, speciality = self.get_doctor_details()
                name_exists = any(d.get_first_name() == first_name and d.get_surname() == surname for d in doctors)
                if name_exists:
                    print('Name already exists.')
                else:
                    new_doctor = Doctor(first_name, surname, speciality)
                    doctors = Doctor.load_from_file('doctor.txt')
                    doctors.append(new_doctor)
                    Doctor.save_to_file('doctor.txt', doctors)
                    print('Doctor registered.')

            elif op == 2:
                print("-----List of Doctors-----")
                print('ID   |           Full Name           |  Speciality   ')
                doctors = Doctor.load_from_file('doctor.txt')
                self.view(doctors)

            elif op == 3:
                while True:
                    print("-----Update Doctor`s Details-----")
                    print('ID   |           Full Name           |  Speciality   ')
                    doctors = Doctor.load_from_file('doctor.txt')
                    self.view(doctors)
                    try:
                        index = int(input('Enter the ID of the doctor: ')) - 1
                        if self.find_index(index, doctors):
                            print('Choose the field to be updated:')
                            print(' 1 First name')
                            print(' 2 Surname')
                            print(' 3 Speciality')
                            field = int(input('Input: '))
                            if field == 1:
                                new_first_name = input("Enter the new first name: ")
                                doctors[index].set_first_name(new_first_name)
                                print("First name changed successfully.")
                            elif field == 2:
                                new_last_name = input("Enter the new last name: ")
                                doctors[index].set_surname(new_last_name)
                                print("Surname changed successfully.")
                            elif field == 3:
                                new_speciality = input("Enter the new speciality: ")
                                doctors[index].set_speciality(new_speciality)
                                print("Speciality changed successfully.")
                            else:
                                print("Invalid choice.")
                            Doctor.save_to_file('doctor.txt', doctors)
                            break
                        else:
                            print("Doctor not found.")
                    except ValueError:
                        print('The ID entered is incorrect.')

            elif op == 4:
                print("-----Delete Doctor-----")
                print('ID   |           Full Name           |  Speciality   ')
                doctors = Doctor.load_from_file('doctor.txt')
                self.view(doctors)
                try:
                    doctor_index = int(input('Enter the ID of the doctor to be deleted: ')) - 1
                    if self.find_index(doctor_index, doctors):
                        doctors.pop(doctor_index)
                        Doctor.save_to_file('doctor.txt', doctors)
                        print('Doctor deleted.')
                    else:
                        print('The ID entered was not found.')
                except ValueError:
                    print('The ID entered is incorrect.')

            elif op == 0:
                break

            else:
                print('Invalid operation chosen.')
                
    def view_patient(self, patients):
        print("-----View Patients-----")
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        patients = Patient.load_from_file('patient.txt')
        self.view(patients)
        
    def add_new_patient(self):
        first_name = input("Enter first name: ")
        surname = input("Enter surname: ")
        age = int(input("Enter age: "))
        mobile = input("Enter mobile: ")
        postcode = input("Enter postcode: ")
        symptoms = input("Enter symptoms (comma-separated): ").split(',')

        new_patient = Patient(first_name, surname, age, mobile, postcode)
        new_patient.set_symptoms(symptoms)

        patients = Patient.load_from_file('patient.txt')
        patients.append(new_patient)
        Patient.save_to_file('patient.txt', patients)
        print("New patient added")
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        patients = Patient.load_from_file('patient.txt')
        self.view(patients)
        
        
        
    def assign_doctor_to_patient(self):
        print("-----Assign-----")

        print("-----All-Patients-----")
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        patients = Patient.load_from_file('patient.txt')
        for i, patient in enumerate(patients, start=1):
            doctor_name = patient.get_doctor() or 'Not Assigned'
            symptoms_str = ', '.join(patient.print_symptoms())
            print(f"{i:<4} | {patient.full_name():<30} | {doctor_name:<30} | {patient.get_age():<4} | {patient.get_mobile():<13} | {patient.get_postcode():<8} | {symptoms_str}")

        non_assigned_patients = [patient for patient in patients if not patient.get_doctor()]
        if not non_assigned_patients:
            print("All patients are already assigned to a doctor.")
            return

        print("\n\n-----------------List of patients not assigned--------------------\n\n")
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        for i, patient in enumerate(non_assigned_patients, start=1):
            doctor_name = patient.get_doctor() or 'Not Assigned'
            symptoms_str = ', '.join(patient.print_symptoms())
            print(f"{i:<4} | {patient.full_name():<30} | {doctor_name:<30} | {patient.get_age():<4} | {patient.get_mobile():<13} | {patient.get_postcode():<8} | {symptoms_str}")

        patient_index = input('Please enter the patient ID: ')

        try:
            patient_index = int(patient_index) - 1
            if patient_index not in range(len(non_assigned_patients)):
                print('The ID entered was not found.')
                return
        except ValueError:
            print('The ID entered is incorrect.')
            return

        selected_patient = non_assigned_patients[patient_index]

        print("-----Doctors Selection-----")
        print('Select the doctor that fits these symptoms:')
        print(", ".join(selected_patient.print_symptoms()))

        print('--------------------------------------------------')
        print('ID   |           Full Name           |  Speciality   ')
        doctors = Doctor.load_from_file('doctor.txt')
        for i, doctor in enumerate(doctors, start=1):
            print(f"{i:<4} | {doctor.full_name():<30} | {doctor.get_speciality()}")

        doctor_index = input('Please enter the doctor ID: ')

        try:
            doctor_index = int(doctor_index) - 1
            if doctor_index not in range(len(doctors)):
                print('The ID entered was not found.')
                return
        except ValueError:
            print('The ID entered is incorrect.')
            return

        selected_doctor = doctors[doctor_index]

        if selected_patient.get_doctor():
            print('This patient is already assigned to a doctor.')
            return

        date_input = input("Enter appointment date (YYYY-MM-DD HH:MM): ")
        try:
            appointment_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            print("The date entered is incorrect. Please use the format YYYY-MM-DD HH:MM")
            return

        selected_patient.link(selected_doctor.full_name(), appointment_date)
        selected_doctor.add_appointment(selected_patient.full_name(), appointment_date)

        print('The patient is now assigned to the doctor.')

        Patient.save_to_file('patient.txt', patients)
        Doctor.save_to_file('doctor.txt', doctors)
        
        
    def discharge(self, patients, discharged_patients):
        patients = Patient.load_from_file('patient.txt')
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')

        self.view(patients)
        do_you_want = input("Do you want to discharge a patient (Y/N): ")
        if do_you_want.upper() == 'Y':
            print("-----Discharge Patient-----")

            try:
                patient_index = int(input('Please enter the patient ID: ')) - 1
                if self.find_index(patient_index, patients):
                    discharge_patient = patients.pop(patient_index)
                    discharged_patients.append(discharge_patient)
                    print('The patient is discharged successfully.')
                    Patient.save_to_file('patient.txt', patients)
                    Patient.save_to_file('discharged_patient.txt', discharged_patients)
                else:
                    print("Invalid patient ID.")
            except ValueError:
                print('The ID entered is incorrect.')

    def view_discharge(self, discharged_patients):
        print("-----Discharged Patients-----")
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        discharged_patients = Patient.load_from_file('discharged_patient.txt')
        self.view(discharged_patients)
        
        
    
        
    def family_patients(self):
        patients = Patient.load_from_file('patient.txt')
        temp_last_name = {}

        for patient in patients:
            patient_last_name = patient.get_surname()
            
            if patient_last_name not in temp_last_name:
                temp_last_name[patient_last_name] = [patient]
            else:
                temp_last_name[patient_last_name].append(patient)
        
        for last_name, patients in temp_last_name.items():
            print(f"\nThe patients with family name '{last_name}' are:")
            for patient in patients:
                print(f"  - {patient.full_name()}")
                
    def relocate_patient(self):
        try:
            print("-----Relocate Patients-----")

            patients = Patient.load_from_file("patient.txt")
            doctors = Doctor.load_from_file("doctor.txt")

            assigned_patients = [patient for patient in patients if patient.get_doctor() != '']


            print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
            for i, patient in enumerate(assigned_patients, start=1):
                symptoms_str = ', '.join(patient.print_symptoms())
                print(f"{i:<4} | {patient.full_name():<30} | {patient.get_doctor():<30} | {patient.get_age():<4} | {patient.get_mobile():<13} | {patient.get_postcode():<8} | {symptoms_str}")


            p_index = int(input('Please enter the patient ID: ')) - 1
            if p_index not in range(len(assigned_patients)):
                print('The ID entered was not found.')
                return

            print("\n-----Doctors Select-----")
            print('ID   |           Full Name           |  Specialty   ')
            for i, doctor in enumerate(doctors, start=1):
                print(f"{i:<4} | {doctor.full_name():<30} | {doctor.get_speciality()}")

            d_index = int(input('Please enter the doctor ID: ')) - 1
            if d_index not in range(len(doctors)):
                print('The ID entered was not found.')
                return

            date_input = input("Enter appointment date (YYYY-MM-DD HH:MM): ")
            try:
                appointment_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
            except ValueError:
                print("The date entered is incorrect. Please use the format YYYY-MM-DD HH:MM")
                return

            patient_to_relocate = assigned_patients[p_index]
            old_doctor_name = patient_to_relocate.get_doctor()
            new_doctor_name = doctors[d_index].full_name()

            for doctor in doctors:
                if doctor.full_name() == old_doctor_name:
                    doctor.remove_patient(patient_to_relocate.full_name())
                    break

            patient_to_relocate.link(new_doctor_name, [appointment_date])
            
            doctors[d_index].add_patient(patient_to_relocate.full_name(), [appointment_date])

            Patient.save_to_file("patient.txt", patients)
            Doctor.save_to_file("doctor.txt", doctors)

            print('\nThe patient has been relocated to another doctor.')
        except ValueError:
            print('The ID entered is incorrect.')
            
    def add_symptoms(self):
        print("-----Add Symptoms-----")

        # Load patients
        patients = Patient.load_from_file("patient.txt")

        # Display patients for selection
        print('ID   |          Full Name             |      Doctor`s Full Name        | Age  |    Mobile     | Postcode | Symptoms')
        for i, patient in enumerate(patients, start=1):
            symptoms_str = ', '.join(patient.print_symptoms())
            print(f"{i:<4} | {patient.full_name():<30} | {patient.get_doctor():<30} | {patient.get_age():<4} | {patient.get_mobile():<13} | {patient.get_postcode():<8} | {symptoms_str}")

        try:
            p_index = int(input('Please enter the patient ID: ')) - 1
            if p_index not in range(len(patients)):
                print('The ID entered was not found.')
                return
        except ValueError:
            print('The ID entered is incorrect.')
            return

        patient = patients[p_index]

        print("\nCurrent Symptoms:")
        current_symptoms = patient.print_symptoms()
        if current_symptoms:
            print("\n".join(f"{i+1}. {symptom}" for i, symptom in enumerate(current_symptoms)))
            
        remove_option = input("Do you want to remove the previous symptoms? (yes/no): ").strip().lower()
        if remove_option == "yes" or remove_option == 'y':
            confirm_remove = input("Are you sure you want to remove the previous symptoms? (yes/no): ").strip().lower()
            if confirm_remove == "yes" or confirm_remove == 'y':
                patient.set_symptoms([])  # Clear current symptoms

        new_symptoms = input("Enter new symptoms separated by commas: ").split(',')
        new_symptoms = [symptom.strip() for symptom in new_symptoms if symptom.strip()]
        patient.add_symptoms(new_symptoms)
        Patient.save_to_file("patient.txt", patients)

        print('Symptoms updated successfully.')

    def management_report(self):
        doctors = Doctor.load_from_file("doctor.txt")
        patients = Patient.load_from_file("patient.txt")

        while True:
            print("\nChoose an option:")
            print("a) Total number of doctors in the system")
            print("b) Total number of patients per doctor")
            print("c) Total number of appointments per month per doctor")
            print("d) Total number of patients based on the illness type")
            print("e) Exit")

            choice = input("Input: ").strip().lower()

            if choice == 'a':
                print(f"The total number of doctors is {len(doctors)}")

            elif choice == 'b':
                doctor_patient_count = {doctor.full_name(): 0 for doctor in doctors}
                for patient in patients:
                    doctor_name = patient.get_doctor()
                    if doctor_name in doctor_patient_count:
                        doctor_patient_count[doctor_name] += 1

                print("\nThe number of patients for each doctor:")
                for doctor_name, patient_count in doctor_patient_count.items():
                    print(f"{doctor_name}: {patient_count}")

                plt.figure(figsize=(12, 6))
                plt.bar(doctor_patient_count.keys(), doctor_patient_count.values())
                plt.xlabel('Doctor')
                plt.ylabel('Number of Patients')
                plt.title('Total Number of Patients per Doctor')
                plt.xticks(rotation=45)
                plt.show()

            elif choice == 'c':
                doctor_appointment_count = defaultdict(int)
                for doctor in doctors:
                    appointments = doctor.get_appointments()
                    for appointment_date in appointments.values():
                        month_year = appointment_date.strftime("%B %Y")
                        doctor_appointment_count[(doctor.full_name(), month_year)] += 1

                print("\nTotal number of appointments per month per doctor:")
                if not doctor_appointment_count:
                    print("No appointments found.")
                else:
                    doctor_names, months_years, counts = zip(*[(d, my, c) for (d, my), c in doctor_appointment_count.items()])
                    for doctor_name in set(doctor_names):
                        plt.plot(months_years, [counts[i] for i in range(len(counts)) if doctor_names[i] == doctor_name], label=doctor_name)
                    plt.xlabel('Month')
                    plt.ylabel('Number of Appointments')
                    plt.title('Total Number of Appointments per Month per Doctor')
                    plt.legend()
                    plt.xticks(rotation=45)
                    plt.show()

            elif choice == 'd':
                total_number_of_patients_based_on_illness = {}
                for patient in patients:
                    patient_symptoms = patient.print_symptoms()
                    for symptom in patient_symptoms:
                        total_number_of_patients_based_on_illness[symptom] = total_number_of_patients_based_on_illness.get(symptom, 0) + 1

                print("\nTotal number of patients based on the illness:")
                if not total_number_of_patients_based_on_illness:
                    print("None")
                else:
                    for symptom, count in total_number_of_patients_based_on_illness.items():
                        print(f"{symptom}: {count} patients")

                    labels = total_number_of_patients_based_on_illness.keys()
                    sizes = total_number_of_patients_based_on_illness.values()
                    plt.figure(figsize=(12, 6))
                    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
                    plt.title('Total Number of Patients based on Illness Type')
                    plt.axis('equal')
                    plt.show()


            elif choice == 'e':
                break
            else:
                print("Invalid choice. Please try again.")

        return doctors, patients
    
    
    