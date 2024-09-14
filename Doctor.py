from datetime import datetime
from person import Person

class Doctor(Person):
    def __init__(self, first_name, surname, speciality):
        super().__init__(first_name, surname)
        self.__speciality = speciality
        self.__patients = {}
        self.__appointments = []

    def get_speciality(self):
        return self.__speciality

    def set_speciality(self, new_speciality):
        self.__speciality = new_speciality

    def add_patient(self, patient_name, appointment_date):
        self.__patients[patient_name] = appointment_date

    def remove_patient(self, patient_name):
        if patient_name in self.__patients:
            del self.__patients[patient_name]

    @staticmethod
    def save_to_file(doctor, doctors):
        with open(doctor, 'w') as file:
            for doctor in doctors:
                file.write(f"{doctor.get_first_name()},{doctor.get_surname()},{doctor.get_speciality()}\n")

    @staticmethod
    def load_from_file(doctor):
        doctors = []
        try:
            with open(doctor, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        doctor = Doctor(data[0], data[1], data[2])
                        doctors.append(doctor)
        except FileNotFoundError:
            print(f"The file {doctor} does not exist.")
        return doctors

    def get_appointments(self):
        return self.__patients

    def get_num_pat(self):
        return len(self.__patients)

    def add_appointment(self, patient_name, appointment_date):
        self.__appointments.append((patient_name, appointment_date))

    def set_appointments(self, appointments):
        self.__appointments = appointments
        
   

    def __str__(self):
        return f'{self.full_name():<30}|{self.__speciality:<15}'