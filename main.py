import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
call_list = []
callers = []
current_caller_index = 0


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
                messagebox.showinfo("Success", "File loaded successfully!")
                assign_calls_button['state'] = 'normal'  # Enable the assign calls button
            else:
                messagebox.showerror("Error", "CSV file does not have the required columns (Name, Phone Number).")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to assign calls
def assign_calls():
    if len(call_list) < 3:
        messagebox.showwarning("Warning", "Not enough contacts left.")
        return

    contact_listbox.delete(0, tk.END)  # Clear existing contacts
    for _ in range(3):
        contact = call_list.pop()
        contact_listbox.insert(tk.END, f"{contact[0]} - {contact[1]}")

    if len(call_list) == 0:
        messagebox.showinfo("Info", "All contacts have been assigned.")
        next_caller_button['state'] = 'disabled'  # Disable the next caller button if list is empty


# Function to switch to the next caller
def next_caller():
    global current_caller_index
    current_caller_index = (current_caller_index + 1) % len(callers)
    update_caller_info()
    contact_listbox.delete(0, tk.END)  # Clear existing contacts
    assign_calls_button['state'] = 'disabled'  # Disable assign calls button until new file is loaded


# Function to update caller information on the interface
def update_caller_info():
    caller_info_label.config(text=f"Current Caller: {callers[current_caller_index]}")


# Function to create Main Window
def create_main_window():
    global contact_listbox, assign_calls_button, next_caller_button, caller_info_label
    main_window = tk.Tk()
    main_window.title("Call Assignment System")

    load_button = tk.Button(main_window, text="Load CSV File", command=load_csv_file)
    load_button.pack(pady=10)

    assign_calls_button = tk.Button(main_window, text="Assign Calls", command=assign_calls, state='disabled')
    assign_calls_button.pack(pady=10)

    next_caller_button = tk.Button(main_window, text="Next Caller", command=next_caller)
    next_caller_button.pack(pady=10)

    caller_info_label = tk.Label(main_window, text="Current Caller: ")
    caller_info_label.pack(pady=10)

    contact_listbox = tk.Listbox(main_window)
    contact_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    update_caller_info()
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

close_button = tk.Button(login_window, text="Start Calling",
                         command=lambda: [login_window.destroy(), create_main_window()])
close_button.pack()

login_window.mainloop()
