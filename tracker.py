import csv
from database import get_all_applications, update_status
from database import search_database
from database import create_database
from database import add_to_database
from database import delete_application
import database
def add_application():

    company = input("Company Name: ")
    position = input("Position: ")
    status = input("Status: ")
    notes = input("Notes: ")

    add_to_database(company, position, status, notes)
    print("Application saved.")


def view_applications():
    rows = database.get_all_applications()
    for row in rows:
        print(
            f"Company: {row[0]} | "
            f"Position: {row[1]} | "
            f"Status: {row[2]} | "
            f"Notes: {row[3]}"
        )            
def search_applications():

    search_term = input("Enter company name: ")
    found = False

    try:
        with open("applications.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                # skip empty rows
                if not row:
                    continue
                # debug print removed; perform case-insensitive search
                if search_term.lower() in row[0].lower():
                    found = True
                    print("Match Found")
                    print(
                        f"Company: {row[0]} | "
                        f"Position: {row[1]} | "
                        f"Status: {row[2]} | "
                        f"Notes: {row[3]}"
                    )
    except FileNotFoundError:
        print("No applications file found.")

    if not found:
        print("No applications found.")


def update_application_status():
    company_name = input("Company Name: ")
    new_status = input("New Status: ")
    update_status(
        company_name,
        new_status
    )
    print("Status updated.")

def export_applications():

    rows = get_all_applications()

    with open(
        "job_report.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Company",
            "Position",
            "Status",
            "Notes"
        ])

        writer.writerows(rows)

    print(
        "Applications exported to job_report.csv"
    )
def remove_application():

    company_name = input(
        "Enter company name to delete: "
    )

    confirmation = input(
        f"Are you sure you want to delete {company_name}? (y/n): "
    )

    if confirmation.lower() == "y":

        deleted_rows = delete_application(
            company_name
        )

        if deleted_rows > 0:

            print(
                "Application deleted."
            )

        else:

            print(
                f"No application found for {company_name}."
            )

    else:

        print(
            "Deletion cancelled."
        )

def view_statistics():

    total = 0
    status_count = {}

    try:
        with open("applications.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                total += 1
                status = row[2] if len(row) > 2 else "Unknown"
                status_count[status] = status_count.get(status, 0) + 1
    except FileNotFoundError:
        print("No applications file found.")
        return

    print(f"\nTotal Applications: {total}")
    print(f"Status Distribution:")
    for status, count in status_count.items():
        print(f"  {status}: {count}")
    interviews = status_count.get("Interview", 0)
    if total > 0:
        response_rate = (interviews / total) * 100
        print(f"\nResponse Rate: {response_rate:.1f}%")

create_database()


while True:

    print("\nJob Application Tracker")
    print("1. Add Application")
    print("2. View Applications")
    print('3. Search Applications')
    print("4. View Statistics")
    print("5. Update Application Status")
    print("6. Export Applications")
    print("7. Remove Application")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_application()

    elif choice == "2":
        view_applications()
    elif choice == "3":
        search_applications()
    elif choice == "4":
        view_statistics()
    elif choice == "5":
        update_application_status()
    elif choice == "6":
        export_applications()
    elif choice == "7":
        remove_application()
    elif choice == "8":
        print("Goodbye!")
        break