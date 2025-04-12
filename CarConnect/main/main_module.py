from CarConnect.dao.admin_service import AdminService
from CarConnect.dao.customer_service import CustomerService
from CarConnect.dao.vehicle_service import VehicleService
from CarConnect.dao.reservation_service import ReservationService
from CarConnect.entity.admin import Admin
from CarConnect.entity.customer import Customer
from CarConnect.entity.vehicle import Vehicle
from CarConnect.entity.reservation import Reservation
from CarConnect.exceptions import DatabaseConnectionException
from CarConnect.util.db_conn_util import DBConnUtil
from CarConnect.exceptions.admin_not_found_exception import AdminNotFoundException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.authentication_exception import AuthenticationException
from CarConnect.exceptions.vehicle_not_found_exception import VehicleNotFoundException
from CarConnect.exceptions.reservation_exception import ReservationException
from CarConnect.exceptions.customer_not_found_exception import CustomerNotFoundException

db = DBConnUtil()
admin_service = AdminService(db)
customer_service = CustomerService(db)
vehicle_service = VehicleService(db)
reservation_service = ReservationService(db)

def admin_menu():
    print("\n--- Admin Menu ---")
    print("1. Register Admin")
    print("2. Get Admin by ID")
    print("3. Get Admin by Username")
    print("4. Update Admin")
    print("5. Delete Admin")

    choice = input("Enter choice: ")

    if choice == '1':
        try:
            first = input("First name: ")
            last = input("Last name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role('super admin', 'fleet manager'): ")

            admin = Admin(None, first, last, email, phone, username, password, role, None)
            admin_service.register_admin(admin)
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except DatabaseConnectionException as e:
            print(f"Database Error: {e}")

    elif choice == '2':
        try:
            admin_id = input("Admin ID: ")
            admin = admin_service.get_admin_by_id(admin_id)
            print(admin)
        except AdminNotFoundException as e:
            print(e)
        except DatabaseConnectionException as e:
            print(e)
        except InvalidInputException as e:
            print(e)

    elif choice == '3':
        try:
            username = input("Enter Username: ")
            admin = admin_service.get_admin_by_username(username)
            print(admin)
        except AdminNotFoundException as e:
            print(e)
        except DatabaseConnectionException as e:
            print(e)
        except InvalidInputException as e:
            print(e)

    elif choice == '4':
        try:
            admin_id = input("Admin ID: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("New Email: ")
            phone = input("New Phone: ")
            username = input("New Username: ")
            role = input("Role('super admin', 'fleet manager'): ")
            admin_service.update_admin(admin_id,first_name,last_name ,email, phone,username, role)
            print("Admin updated.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except DatabaseConnectionException as e:
            print(f"Registration Failed: {e}")

    elif choice == '5':
        try:
            admin_id = input("Admin ID: ")
            admin_service.delete_admin(admin_id)
        except AdminNotFoundException as e:
            print(f"Admin Not Found: {e}")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except DatabaseConnectionException as e:
            print(f"Registration Failed: {e}")

def customer_menu():
    print("\n--- Customer Menu ---")
    print("1. Register Customer")
    print("2. Get Customer by ID")
    print("3. Get Customer by Username")
    print("4. Update Customer")
    print("5. Delete Customer")
    print("6. Authenticate Customer")

    choice = input("Enter choice: ")

    if choice == '1':
        try:
            first = input("First name: ")
            last = input("Last name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")
            username = input("Username: ")
            password = input("Password: ")

            customer = Customer(None, first, last, email, phone, address, username, password, None)
            customer_service.register_customer(customer)
            print("Customer registered.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")

    elif choice == '2':
        try:
            customer_id = input("Customer ID: ")
            customer = customer_service.get_customer_by_id(customer_id)
            print(customer)
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Customer Error: {e}")

    elif choice == '3':
        try:
            username = input("Enter Username: ")
            customer = customer_service.get_customer_by_username(username)
            print(customer)
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Customer Error: {e}")

    elif choice == '4':
        try:
            customer_id = input("Customer ID: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("New Email: ")
            phone = input("New Phone: ")
            address = input("New Address: ")
            username = input("Username: ")
            customer_service.update_customer(customer_id,first_name,last_name, email, phone, address,username)
            print("Customer updated.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Customer Error: {e}")


    elif choice == '5':
        try:
            customer_id = input("Customer ID: ")
            customer_service.delete_customer(customer_id)
            print("Customer deleted.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Customer Error: {e}")

    elif choice == '6':
        try:
            username = input("Username: ")
            password = input("Password: ")
            customer = customer_service.authenticate_customer(username, password)
            print(customer)
            print("Authentication successful!")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except AuthenticationException as e:
            print(f"Error:{e}")

def vehicle_menu():
    print("\n--- Vehicle Menu ---")
    print("1. Add Vehicle")
    print("2. Get Vehicle by ID")
    print("3. List Available Vehicles")
    print("4. Update Vehicle")
    print("5. Remove Vehicle")

    choice = input("Enter choice: ")

    if choice == '1':
        try:
            model = input("Model: ")
            make = input("Make: ")
            year = input("Year: ")
            color = input("Color: ")
            reg_no = input("Registration Number: ")
            availability = input("Availability (1/0): ")
            daily_rate = input("Daily Rate: ")

            vehicle = Vehicle(None, model, make, year, color, reg_no, availability, daily_rate)
            vehicle_service.add_vehicle(vehicle)
            print("Vehicle added.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except DatabaseConnectionException as e:
            print(f"Registration Failed: {e}")

    elif choice == '2':
        try:
            vehicle_id = input("Vehicle ID: ")
            if not vehicle_id.isdigit():
                raise InvalidInputException("Vehicle Id must be Integer")
            vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
            print(vehicle)
        except VehicleNotFoundException as e:
            print(f"Not Found: {e}")
        except DatabaseConnectionException as e:
            print(f"Database Error: {e}")

    elif choice == '3':
        try:
            vehicles = vehicle_service.get_available_vehicles()
            for v in vehicles:
                print(v)
        except DatabaseConnectionException as e:
            print(f"Database Error: {e}")

    elif choice == '4':
        try:
            vehicle_id = input("Vehicle ID: ")
            rate = input("New Daily Rate: ")
            availability = input("Availability (1/0): ")
            vehicle_service.update_vehicle(vehicle_id, rate, availability)
            print("Vehicle updated.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except VehicleNotFoundException as e:
            print(f"Not Found: {e}")
        except DatabaseConnectionException as e:
            print(f"Database Error: {e}")

    elif choice == '5':
        try:
            vehicle_id = input("Vehicle ID: ")
            vehicle_service.remove_vehicle(vehicle_id)
            print("Vehicle removed.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except VehicleNotFoundException as e:
            print(f"Not Found: {e}")
        except DatabaseConnectionException as e:
            print(f"Database Error: {e}")

def reservation_menu():
    print("\n--- Reservation Menu ---")
    print("1. Create Reservation")
    print("2. Get Reservation by ID")
    print("3. Get Reservations by Customer ID")
    print("4. Update Reservation Status")
    print("5. Cancel Reservation")
    print("6. Reservation History Report")
    print("7. Generate Vehicle Report")
    print("8. Generate Revenue Report")

    choice = input("Enter choice: ")

    if choice == '1':
        try:
            customer_id = input("Customer ID: ")
            vehicle_id = input("Vehicle ID: ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            total_cost = input("Total Cost: ")
            status = input("Status('pending', 'confirmed', 'completed', 'cancelled'): ")

            reservation = Reservation(None, customer_id, vehicle_id, start_date, end_date, total_cost, status)
            reservation_service.create_reservation(reservation)
            print("Reservation created.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")

    elif choice == '2':
        try:
            reservation_id = input("Reservation ID: ")
            reservation = reservation_service.get_reservation_by_id(reservation_id)
            print(reservation)
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except ReservationException as e:
            print(f"Error: {e}")

    elif choice == '3':
        try:
            customer_id = input("Customer ID: ")
            reservations = reservation_service.get_reservations_by_customer_id(customer_id)
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except ReservationException as e:
            print(f"Error: {e}")

    elif choice == '4':
        try:
            reservation_id = input("Reservation ID: ")
            status = input("New Status('pending', 'confirmed', 'completed', 'cancelled'): ")
            reservation_service.update_reservation(reservation_id, status)
            print("Reservation updated.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except ReservationException as e:
            print(f"Error: {e}")

    elif choice == '5':
        try:
            reservation_id = input("Reservation ID: ")
            reservation_service.cancel_reservation(reservation_id)
            print("Reservation canceled.")
        except InvalidInputException as e:
            print(f"Input Error: {e}")
        except ReservationException as e:
            print(f"Error: {e}")

    elif choice == '6':
        reservation_service.generate_reservation_history_report()

    elif choice == '7':
        reservation_service.generate_vehicle_utilization_report()

    elif choice == '8':
        reservation_service.generate_revenue_report()

def main():
    while True:
        print("\n===== CarConnect Main Menu =====")
        print("1. Admin Services")
        print("2. Customer Services")
        print("3. Vehicle Services")
        print("4. Reservation Services")
        print("0. Exit")

        option = input("Select option: ")

        if option == '1':
            admin_menu()
        elif option == '2':
            customer_menu()
        elif option == '3':
            vehicle_menu()
        elif option == '4':
            reservation_menu()
        elif option == '0':
            print("Exiting CarConnect...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
