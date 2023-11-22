import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
call_list = []
callers = []
caller_call_lists = {}
caller_listboxes = {}
caller_load_more_buttons = {}

# Function to load CSV file
def load_csv_file():
    global call_list
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = pd.read_csv(file_path)
            if 'Name' in data.columns and 'Phone Number' in data.columns:
                call_list = data[['Name', 'Phone Number']].values.tolist()
                random.shuffle(call_list)
                assign_calls_to_all()  # Assign initial calls to all callers
                enable_load_more_buttons()  # Enable 'Load More' buttons
                messagebox.showinfo("Success", "File loaded and initial calls assigned!")
            else:
                messagebox.showerror("Error", "CSV file does not have the required columns (Name, Phone Number).")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to assign calls to all callers
def assign_calls_to_all():
    for caller in callers:
        assign_calls(caller)

# Function to enable 'Load More' buttons
def enable_load_more_buttons():
    for button in caller_load_more_buttons.values():
        button['state'] = 'normal'

# Function to assign calls to a specific caller
def assign_calls(caller):
    if len(call_list) < 3:
        messagebox.showwarning("Warning", f"Not enough contacts left for {caller}.")
        return

    highlight_previous_calls(caller)  # Highlight previous calls in yellow

    caller_call_lists[caller] = caller_call_lists.get(caller, [])  # Initialize if not exist
    for _ in range(3):
        contact = call_list.pop()
        caller_call_lists[caller].append(contact)
        update_caller_listbox(caller)

    if len(call_list) == 0:
        disable_all_load_more_buttons()
        messagebox.showinfo("Info", "All contacts have been assigned.")

# Function to highlight previous calls in yellow
def highlight_previous_calls(caller):
    listbox = caller_listboxes[caller]
    for i in range(listbox.size()):
        listbox.itemconfig(i, bg='yellow')

# Function to update listbox for a caller
def update_caller_listbox(caller):
    listbox = caller_listboxes[caller]
    listbox.delete(0, tk.END)  # Clear existing contacts
    for contact in caller_call_lists[caller]:
        listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")
        listbox.itemconfig(listbox.size() - 1, bg='white')  # Set background color of new entry

# Function to create 'Load More' button command
def create_load_more_command(caller):
    return lambda: assign_calls(caller)

# Function to disable all 'Load More' buttons
def disable_all_load_more_buttons():
    for button in caller_load_more_buttons.values():
        button['state'] = 'disabled'

# Function to create Main Window
def create_main_window():
    global caller_listboxes, caller_load_more_buttons
    main_window = tk.Tk()
    main_window.title("Call Assignment System")

    load_button = tk.Button(main_window, text="Load CSV File", command=load_csv_file)
    load_button.pack(pady=10)

    for caller in callers:
        caller_frame = tk.LabelFrame(main_window, text=caller)
        caller_frame.pack(padx=10, pady=10, fill="both", expand=True)

        caller_listbox = tk.Listbox(caller_frame)
        caller_listbox.pack(padx=10, pady=10, fill="both", expand=True)
        caller_listboxes[caller] = caller_listbox

        load_more_button = tk.Button(caller_frame, text="Load More", command=create_load_more_command(caller), state='disabled')
        load_more_button.pack(pady=5)
        caller_load_more_buttons[caller] = load_more_button

    main_window.mainloop()

# Function for Login
def login():
    caller_name = name_entry.get()
    if caller_name:
        callers.append(caller_name)
        name_entry.delete(0, tk.END)  # Clear the entry for next caller
        messagebox.showinfo("Success", f"{caller_name} added. Add next caller or close window to start.")
    else:
        messagebox.showwarning("Warning", "Please enter your name.")

# Create Login Window
login_window = tk.Tk()
login_window.title("Login")

name_label = tk.Label(login_window, text="Enter caller name:")
name_label.pack()

name_entry = tk.Entry(login_window)
name_entry.pack()

login_button = tk.Button(login_window, text="Add Caller", command=login)
login_button.pack()

close_button = tk.Button(login_window, text="Start Calling", command=lambda: [login_window.destroy(), create_main_window()])
close_button.pack()

login_window.mainloop()
