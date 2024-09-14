# Imports
from Admin import *
from Doctor import *
from Patient import  *

def main():

    admin = Admin('admin','123','B1 1AB') 

    while True:
        if admin.login():
            running = True 
            break
        else:
            print('Incorrect username or password.')

    while running:
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- View patients')
        print(' 3- Assign doctor to a patient')
        print(' 4- Discharge patients')
        print(' 5- View discharged patient')
        print(' 6- Update admin details')
        print(' 7- Group patients by family')
        print(" 8- Add patients")
        print(" 9- Relocate a patient from one doctor to another")
        print(" 10- View management report")
        print(" 11- Add symptoms")
        print(" 12- Quit")

        try:
            op = int(input("Input: "))
        except ValueError:
            print("Invalid choice. please choose number only")
            continue

        if op == 1:
            admin.doctor_management(doctors)
            
        elif op == 2:
            admin.view_patient(patients)

        elif op == 3:
            admin.assign_doctor_to_patient()
            
        elif op == 4:
            admin.discharge(patients, discharged_patients)

        elif op == 5:
            admin.view_discharge(discharged_patients)


        elif op == 6:

            admin.update_details()
     
        elif op == 7:
            admin.family_patients()
            
        elif op == 8:
            admin.add_new_patient()
            
            
        elif op == 9:
            admin.relocate_patient()
            
        elif op == 10:
            admin.management_report()
            
            

                    
        elif op == 11:
            admin.add_symptoms()          



        elif op == 12:
            print("the system is going to be off: ")
            print("bye bye")
            running = False

        else:
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()