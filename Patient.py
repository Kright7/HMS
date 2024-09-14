from datetime import datetime
from person import Person

class Patient(Person):
    def __init__(self, first_name, surname, age, mobile, postcode, assigned="", symptoms=None, appointments=None):
        super().__init__(first_name, surname)
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = assigned
        self.__symptoms = symptoms if symptoms is not None else []
        self.appointments = appointments if appointments is not None else []

    def link(self, doctor_name, appointment_date):
        self.__doctor = doctor_name
        if isinstance(appointment_date, list):  # Ensure appointment_date is a list
            self.appointments = appointment_date
        else:
            self.appointments = [appointment_date]

    def get_doctor(self):
        return self.__doctor

    def set_symptoms(self, symptoms):
        self.__symptoms = symptoms

    def add_symptoms(self, symptoms):
        self.__symptoms.extend(symptoms)

    def print_symptoms(self):
        return self.__symptoms

    @staticmethod
    def save_to_file(patient, patients):
        with open(patient, 'w') as file:
            for patient in patients:
                symptoms_str = '|'.join(patient.print_symptoms())
                appointments_str = '|'.join(appt.strftime("%Y-%m-%d %H:%M") for appt in patient.appointments)
                file.write(f"{patient.get_first_name()},{patient.get_surname()},{patient.get_age()},{patient.get_mobile()},{patient.get_postcode()},{patient.get_doctor()},{symptoms_str},{appointments_str}\n")

    @staticmethod
    def load_from_file(patient):
        patients = []
        try:
            with open(patient, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) >= 8:
                        first_name, surname, age, mobile, postcode, doctor, symptoms_str, appointments_str = data[:8]
                        symptoms = symptoms_str.split('|') if symptoms_str else []
                        appointments = [datetime.strptime(appt.strip(), "%Y-%m-%d %H:%M") for appt in appointments_str.split('|') if appt.strip()]
                        patient = Patient(first_name, surname, int(age), mobile, postcode, assigned=doctor, symptoms=symptoms, appointments=appointments)
                        patients.append(patient)
        except FileNotFoundError:
            print(f"The file {patient} does not exist.")
        return patients

    def get_age(self):
        return self.__age

    def get_mobile(self):
        return self.__mobile

    def get_postcode(self):
        return self.__postcode

    def __str__(self):
        doctor_info = self.__doctor if self.__doctor else ''
        symptoms_str = ', '.join(self.print_symptoms())
        return f'{self.full_name():<30} | {doctor_info:<30} | {self.__age:<4} | {self.__mobile:<13} | {self.__postcode:<8} | {symptoms_str}'


