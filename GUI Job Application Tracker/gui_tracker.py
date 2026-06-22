import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database
import csv
import os
window = tk.Tk()
selected_id = None
database.create_database()
window.title("Job Application Tracker")

window.geometry("1000x700")

title_label = tk.Label(window, text="Job Application Tracker", font=("Arial", 16))
title_label.pack(pady=20)

form_status_label = tk.Label(window, text="", font=("Arial", 10, "italic"), fg="blue")
form_status_label.pack(pady=(0, 10))

# Search section
search_container = tk.Frame(window)
search_container.pack(pady=5, fill="x", anchor="w")

search_input_frame = tk.Frame(search_container)
search_input_frame.pack(pady=(0, 5), anchor="w")

search_label = tk.Label(
    search_input_frame,
    text="Search:"
)

search_label.grid(row=0, column=0, padx=(0, 5))

search_entry = tk.Entry(
    search_input_frame,
    width=30
)

search_entry.grid(row=0, column=1, padx=(0, 10))
search_input_frame.columnconfigure(0, weight=0)
search_input_frame.columnconfigure(1, weight=1)

company_label = tk.Label(
    window,
    text="Company:"
)

company_label.pack()

company_entry = tk.Entry(
    window,
    width=40
)

company_entry.pack(pady=5)

position_label = tk.Label(
    window,
    text="Position:"
)

position_label.pack()

# Position combobox with common roles plus 'Other'
positions_list = [
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Mobile Developer",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Site Reliability Engineer",
    "QA Engineer",
    "QA Tester",
    "Product Manager",
    "Project Manager",
    "UX Designer",
    "UI Designer",
    "Systems Administrator",
    "Security Engineer",
    "Business Analyst",
    "Technical Writer",
    "Researcher",
    "Sales",
    "Marketing",
    "Customer Support",
    "HR",
    "Finance",
    "Manager",
    "Director",
    "Intern",
    "Contractor",
    "Consultant",
    "Other",
]

position_combobox = ttk.Combobox(window, values=positions_list, width=37, state="readonly")
position_combobox.pack(pady=5)

# Entry to capture custom position when 'Other' is selected
position_other_entry = tk.Entry(window, width=40)
position_other_entry.pack(pady=2)
position_other_entry.config(state="disabled")


def on_position_select(event=None):
    if position_combobox.get() == "Other":
        position_other_entry.config(state="normal")
        position_other_entry.focus_set()
    else:
        position_other_entry.delete(0, tk.END)
        position_other_entry.config(state="disabled")

position_combobox.bind("<<ComboboxSelected>>", on_position_select)

status_label = tk.Label(window, text="Status:")
status_label.pack()

status_combobox = ttk.Combobox(
    window,
    values=["Applied", "Interview", "Offer", "Rejected", "Active"],
    width=37,
    state="readonly"
)
status_combobox.pack(pady=5)

basis_label = tk.Label(
    window,
    text="Basis:"
)

basis_label.pack()

basis_combobox = ttk.Combobox(
    window,
    values=["Full Time/Onsite", "Part Time/Remote", "Full Time/Remote", "Part Time/Onsite", "Internship", "Contract", "Freelance", "Other"],
    width=37,
    state="readonly"
)

basis_combobox.pack(pady=5)


def load_applications():
    rows = database.get_all_applications()

    for row in tree.get_children():
        tree.delete(row)

    for application in rows:
        status = application[3]
        tags = ()
        if status == "Interview":
            tags = ("interview",)
        elif status == "Offer":
            tags = ("offer",)
        elif status == "Rejected":
            tags = ("rejected",)
        tree.insert("", tk.END, values=(application[0], application[1], application[2], application[3], application[4], application[5]), tags=tags)


def get_summary():
    return database.get_application_summary()


def open_statistics_window():
    summary = get_summary()

    stats_window = tk.Toplevel(window)
    stats_window.title("Application Statistics")
    stats_window.geometry("360x220")
    stats_window.resizable(False, False)
    stats_window.transient(window)
    stats_window.grab_set()

    header_label = tk.Label(stats_window, text="Application Statistics", font=("Arial", 14, "bold"))
    header_label.pack(pady=(12, 8))

    stats_frame = tk.Frame(stats_window)
    stats_frame.pack(padx=20, pady=5, fill="x")

    tk.Label(stats_frame, text=f"Total Applications: {summary['total']}", font=("Arial", 11, "bold")).pack(anchor="w", pady=2)
    tk.Label(stats_frame, text=f"Applied: {summary['Applied']}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(stats_frame, text=f"Interview: {summary['Interview']}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(stats_frame, text=f"Offer: {summary['Offer']}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(stats_frame, text=f"Rejected: {summary['Rejected']}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(stats_frame, text=f"Active: {summary['Active']}", font=("Arial", 10)).pack(anchor="w", pady=2)

    close_button = tk.Button(stats_window, text="Close", width=12, command=stats_window.destroy)
    close_button.pack(pady=(12, 10))


def export_to_csv():
    rows = database.get_all_applications()

    if not rows:
        messagebox.showwarning("No Data", "No applications to export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile="applications.csv"
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Company", "Position", "Status", "Basis", "Date Added"])
            writer.writerows(rows)

        messagebox.showinfo("Export Successful", f"Applications exported to:\n{file_path}")
        os.startfile(file_path)
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")


def validate_application_inputs(company, position, status, basis):
    if not company.strip():
        messagebox.showwarning("Invalid Input", "Company name is required.")
        return False

    if not position.strip():
        messagebox.showwarning("Invalid Input", "Position is required.")
        return False

    if not status.strip():
        messagebox.showwarning("Invalid Input", "Status is required.")
        return False

    if not basis.strip():
        messagebox.showwarning("Invalid Input", "Basis is required.")
        return False

    return True


def add_application():
    global selected_id

    if selected_id is not None:
        messagebox.showinfo(
            "Edit In Progress",
            "You are editing an existing application. Click Update Application to save changes or Clear to start a new entry."
        )
        return

    company = company_entry.get().strip()
    position = position_combobox.get().strip()
    if position == "Other":
        position = position_other_entry.get().strip()
    status = status_combobox.get().strip()
    basis = basis_combobox.get().strip()

    if not validate_application_inputs(company, position, status, basis):
        return

    database.add_to_database(company, position, status, basis)

    messagebox.showinfo("Success", "Application saved successfully.")

    clear_fields()
    load_applications()


def update_application():
    global selected_id

    if selected_id is None:
        messagebox.showwarning(
            "No Selection",
            "Please select an application and click Edit before updating."
        )
        return

    company = company_entry.get().strip()
    position = position_combobox.get().strip()
    if position == "Other":
        position = position_other_entry.get().strip()
    status = status_combobox.get().strip()
    basis = basis_combobox.get().strip()

    if not validate_application_inputs(company, position, status, basis):
        return

    database.update_application(selected_id, company, position, status, basis)

    messagebox.showinfo("Success", "Application updated successfully.")

    selected_id = None
    clear_fields()
    load_applications()


def delete_application():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an application to delete.")
        return

    values = tree.item(selected_item[0], "values")
    application_id = values[0]
    company = values[1]

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the application for {company}?")
    if confirm:
        database.delete_application(application_id)
        load_applications()
        messagebox.showinfo("Deleted", "Application deleted successfully.")
    else:
        messagebox.showinfo("Cancelled", "Deletion cancelled.")

    clear_fields()

button_frame = tk.Frame(window)
button_frame.pack(pady=15)

add_button = tk.Button(
    button_frame,
    text="Add Application",
    width=16,
    command=add_application
)

update_button = tk.Button(
    button_frame,
    text="Update Application",
    width=16,
    command=update_application,
    state="disabled"
)


delete_button = tk.Button(
    button_frame,
    text="Delete Application",
    width=16,
    command=delete_application
)

def search_applications(event=None):
    search_term = search_entry.get().strip()

    if not search_term:
        load_applications()
        return

    rows = database.search_applications(search_term)

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        status = row[3]
        tags = ()
        if status == "Interview":
            tags = ("interview",)
        elif status == "Offer":
            tags = ("offer",)
        elif status == "Rejected":
            tags = ("rejected",)
        tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=tags)

search_entry.bind("<KeyRelease>", search_applications)

view_stats_button = tk.Button(
    button_frame,
    text="View Statistics",
    width=14,
    command=open_statistics_window
)

view_stats_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(
    button_frame,
    text="Export CSV",
    width=12,
    command=export_to_csv
)

export_button.pack(side=tk.LEFT, padx=5)

show_all_button = tk.Button(
    button_frame,
    text="Show All",
    width=12,
    command=load_applications
)

show_all_button.pack(side=tk.LEFT, padx=5)

def edit_application():

    global selected_id

    selected_item = tree.selection()

    if not selected_item:

        messagebox.showwarning(
            "No Selection",
            "Please select an application to edit."
        )

        return

    values = tree.item(
        selected_item[0],
        "values"
    )

    selected_id = values[0]

    company = values[1]
    position = values[2]
    status = values[3]
    basis = values[4]

    company_entry.delete(0, tk.END)
    company_entry.insert(0, company)

    position_combobox.set(position)

    status_combobox.set(status)

    basis_combobox.set(basis)

    form_status_label.config(text=f"Editing application ID {selected_id}")
    add_button.config(state="disabled")
    update_button.config(state="normal")

edit_button = tk.Button(
    button_frame,
    text="Edit Application",
    width=16,
    command=edit_application
)
edit_button.pack(side=tk.LEFT, padx=5)

def clear_fields():
    global selected_id

    selected_id = None
    company_entry.delete(0, tk.END)
    position_combobox.set("")
    position_other_entry.delete(0, tk.END)
    position_other_entry.config(state="disabled")
    status_combobox.set("")
    basis_combobox.set("")
    form_status_label.config(text="")
    add_button.config(state="normal")
    update_button.config(state="disabled")
    company_entry.focus_set()

clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=16,
    command=clear_fields
)

add_button.pack(side=tk.LEFT, padx=5)
update_button.pack(side=tk.LEFT, padx=5)
edit_button.pack(side=tk.LEFT, padx=5)
delete_button.pack(side=tk.LEFT, padx=5)
clear_button.pack(side=tk.LEFT, padx=5)

# Create sorting variable
sort_column = "Company"
sort_reverse = False

def on_heading_click(col):
    global sort_column, sort_reverse
    if sort_column == col:
        sort_reverse = not sort_reverse
    else:
        sort_column = col
        sort_reverse = False
    sort_applications()

def sort_applications():
    # Get all items with their tags
    items = [(tree.item(item, "values"), tree.item(item, "tags")) for item in tree.get_children()]
    
    # Column index mapping
    col_index = {"ID": 0, "Company": 1, "Position": 2, "Status": 3, "Basis": 4, "Date Added": 5}
    
    # Sort by the selected column
    try:
        items.sort(key=lambda x: x[0][col_index[sort_column]], reverse=sort_reverse)
    except:
        items.sort(key=lambda x: str(x[0][col_index[sort_column]]), reverse=sort_reverse)
    
    # Refresh tree with sorted items
    for item in tree.get_children():
        tree.delete(item)
    
    for values, tags in items:
        tree.insert("", tk.END, values=values, tags=tags)

tree = ttk.Treeview(
    window,
    columns=(
        "ID",
        "Company",
        "Position",
        "Status",
        "Basis",
        "Date Added"
    ),
    show="headings"
)
tree.heading("ID", text="ID", command=lambda: on_heading_click("ID"))

tree.column("ID", width=50)

tree.heading("Company", text="Company", command=lambda: on_heading_click("Company"))

tree.heading("Position", text="Position", command=lambda: on_heading_click("Position"))

tree.heading("Status", text="Status", command=lambda: on_heading_click("Status"))

tree.heading("Basis", text="Basis", command=lambda: on_heading_click("Basis"))

tree.heading("Date Added", text="Date Added", command=lambda: on_heading_click("Date Added"))

tree.column("Company", width=150)

tree.column("Position", width=150)

tree.column("Status", width=100)

tree.column("Basis", width=150)

tree.column("Date Added", width=150)

# Configure tag colors
tree.tag_configure("interview", background="#FFFF99")
tree.tag_configure("offer", background="#99FF99")
tree.tag_configure("rejected", background="#FF9999")

tree.pack(
    pady=20,
    fill="both",
    expand=True
)

load_applications()

company_entry.bind(
    "<Return>",
    lambda event: position_combobox.focus_set()
)

position_combobox.bind(
    "<Return>",
    lambda event: position_other_entry.focus_set() if position_combobox.get() == "Other" else status_combobox.focus_set()
)

status_combobox.bind(
    "<Return>",
    lambda event: basis_combobox.focus_set()
)

company_entry.focus_set()

window.mainloop()