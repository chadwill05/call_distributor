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
caller_call_count = {}

# Function to load CSV file
def load_csv_file():
    global call_list
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = pd.read_csv(file_path)
            if all(col in data.columns for col in ['Name', 'Phone Number', 'Company']):
                call_list = data[['Name', 'Phone Number', 'Company']].values.tolist()
                random.shuffle(call_list)
                assign_calls_to_all()
                enable_load_more_buttons()
                messagebox.showinfo("Success", "File loaded and initial calls assigned!")
            else:
                messagebox.showerror("Error", "CSV file does not have the required columns (Name, Phone Number, Company).")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def assign_calls_to_all():
    for caller in callers:
        assign_calls(caller, initial=True)

def assign_calls(caller, initial=False):
    if len(call_list) < 3:
        messagebox.showwarning("Warning", f"Not enough contacts left for {caller}.")
        return

    caller_call_lists[caller] = caller_call_lists.get(caller, [])
    for _ in range(3):
        if call_list:
            contact = call_list.pop()
            caller_call_lists[caller].append(contact)
            update_caller_listbox(caller)

    update_caller_count(caller)

    if len(call_list) == 0:
        disable_all_load_more_buttons()
        messagebox.showinfo("Info", "All contacts have been assigned.")

def update_caller_listbox(caller):
    listbox = caller_listboxes[caller]
    listbox.delete(0, tk.END)
    for contact in caller_call_lists[caller]:
        listbox.insert(tk.END, f"{contact[0]} - {contact[1]} - {contact[2]}")  # Include company


def update_caller_count(caller):
    count = len(caller_call_lists[caller])
    caller_call_count[caller].config(text=f"Calls assigned: {count}")

def create_load_more_command(caller):
    return lambda: assign_calls(caller)

def disable_all_load_more_buttons():
    for button in caller_load_more_buttons.values():
        button['state'] = 'disabled'

def enable_load_more_buttons():
    for button in caller_load_more_buttons.values():
        button['state'] = 'normal'

def create_main_window():
    global caller_listboxes, caller_load_more_buttons, caller_call_count
    main_window = tk.Tk()
    main_window.title("Call Assignment System")
    main_window.geometry("900x600")  # Set the size of the window

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

        call_count_label = tk.Label(caller_frame, text="Calls assigned: 0")
        call_count_label.pack(pady=5)
        caller_call_count[caller] = call_count_label

    main_window.mainloop()

def login():
    caller_name = name_entry.get()
    if caller_name:
        callers.append(caller_name)
        name_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"{caller_name} added. Add next caller or close window to start.")
    else:
        messagebox.showwarning("Warning", "Please enter your name.")

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
