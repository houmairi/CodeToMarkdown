import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import json

def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory")
    if selected_directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(tk.END, selected_directory)
        display_files(selected_directory)

def display_files(directory):
    file_tree.delete(*file_tree.get_children())
    traverse_directory(directory, "")

def traverse_directory(directory, parent):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            item_id = file_tree.insert(parent, "end", text=item, values=(item_path,))
            traverse_directory(item_path, item_id)
        else:
            file_tree.insert(parent, "end", text=item, values=(item_path,))

def add_selected_files():
    selected_files = [file_tree.item(item)["values"][0] for item in file_tree.selection()]
    for file_path in selected_files:
        selected_file_tree.insert("", "end", text=os.path.basename(file_path), values=(file_path,))

def remove_selected_files():
    selected_items = selected_file_tree.selection()
    for item in selected_items:
        selected_file_tree.delete(item)

def select_save_location():
    save_location = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Save Location")
    if save_location:
        save_location_entry.delete(0, tk.END)
        save_location_entry.insert(tk.END, save_location)

def collect_code():
    selected_files = [selected_file_tree.item(item)["values"][0] for item in selected_file_tree.get_children()]
    if not selected_files:
        messagebox.showwarning("Warning", "No files selected.")
        return

    output_filename = filename_entry.get()
    if not output_filename:
        messagebox.showwarning("Warning", "Please enter a filename.")
        return

    output_directory = save_location_entry.get()
    if not output_directory:
        messagebox.showwarning("Warning", "Please select a save location.")
        return

    output_file = os.path.join(output_directory, output_filename)

    with open(output_file, "w") as output:
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            output.write(f"<{file_name}>\n```\n")
            with open(file_path, "r") as f:
                code = f.read()
                output.write(code + "\n```\n\n")

    messagebox.showinfo("Success", "Code collected and saved successfully.")

def save_profile():
    profile_name = profile_entry.get()
    if not profile_name:
        messagebox.showwarning("Warning", "Please enter a profile name.")
        return

    selected_files = [selected_file_tree.item(item)["values"][0] for item in selected_file_tree.get_children()]

    profile_data = {
        "directory": directory_entry.get(),
        "filename": filename_entry.get(),
        "save_location": save_location_entry.get(),
        "selected_files": selected_files
    }

    profiles[profile_name] = profile_data
    update_profile_dropdown()
    save_profiles_to_file()
    messagebox.showinfo("Success", "Profile saved successfully.")

def load_profile(event):
    selected_profile = profile_dropdown.get()
    if selected_profile in profiles:
        profile_data = profiles[selected_profile]
        directory_entry.delete(0, tk.END)
        directory_entry.insert(tk.END, profile_data["directory"])
        filename_entry.delete(0, tk.END)
        filename_entry.insert(tk.END, profile_data["filename"])
        save_location_entry.delete(0, tk.END)
        save_location_entry.insert(tk.END, profile_data["save_location"])
        display_files(profile_data["directory"])
        selected_file_tree.delete(*selected_file_tree.get_children())
        for file_path in profile_data["selected_files"]:
            selected_file_tree.insert("", "end", text=os.path.basename(file_path), values=(file_path,))

def update_profile_dropdown():
    profile_dropdown["values"] = list(profiles.keys())

def save_profiles_to_file():
    with open("profiles.json", "w") as file:
        json.dump(profiles, file)

def load_profiles_from_file():
    global profiles
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    else:
        profiles = {}

# Create the main window
window = tk.Tk()
window.title("Code Collector")

# Create and pack the directory selection button and entry
directory_frame = tk.Frame(window)
directory_frame.pack(pady=10)
directory_label = tk.Label(directory_frame, text="Directory:")
directory_label.pack(side=tk.LEFT)
directory_entry = tk.Entry(directory_frame, width=50)
directory_entry.pack(side=tk.LEFT, padx=5)
select_directory_button = tk.Button(directory_frame, text="Select", command=select_directory)
select_directory_button.pack(side=tk.LEFT)

# Create and pack the file treeview
file_tree_frame = tk.Frame(window)
file_tree_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
file_tree = ttk.Treeview(file_tree_frame, columns=("Path",), show="tree", selectmode="extended")
file_tree.heading("#0", text="Files")
file_tree.pack(fill="both", expand=True)

# Create and pack the selected files treeview
selected_file_tree_frame = tk.Frame(window)
selected_file_tree_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
selected_file_tree = ttk.Treeview(selected_file_tree_frame, columns=("Path",), show="tree")
selected_file_tree.heading("#0", text="Selected Files")
selected_file_tree.pack(fill="both", expand=True)

# Create and pack the add/remove buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
add_button = tk.Button(button_frame, text="Add", command=add_selected_files)
add_button.pack(side=tk.LEFT, padx=5)
remove_button = tk.Button(button_frame, text="Remove", command=remove_selected_files)
remove_button.pack(side=tk.LEFT)

# Create and pack the input-related widgets below the displays
input_frame = tk.Frame(window)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Create and pack the filename entry
filename_frame = tk.Frame(input_frame)
filename_frame.pack(pady=5, anchor=tk.W)
filename_label = tk.Label(filename_frame, text="Filename:")
filename_label.pack(side=tk.LEFT)
filename_entry = tk.Entry(filename_frame, width=30)
filename_entry.pack(side=tk.LEFT, padx=5)
filename_entry.insert(tk.END, "output.txt")

# Create and pack the save location entry and button
save_location_frame = tk.Frame(input_frame)
save_location_frame.pack(pady=5, anchor=tk.W)
save_location_label = tk.Label(save_location_frame, text="Save Location:")
save_location_label.pack(side=tk.LEFT)
save_location_entry = tk.Entry(save_location_frame, width=50)
save_location_entry.pack(side=tk.LEFT, padx=5)
select_save_location_button = tk.Button(save_location_frame, text="Select", command=select_save_location)
select_save_location_button.pack(side=tk.LEFT)

# Create and pack the collect code button
collect_button = tk.Button(input_frame, text="Collect Code", command=collect_code)
collect_button.pack(pady=10, anchor=tk.W)

# Create and pack the profile entry and save button
profile_frame = tk.Frame(input_frame)
profile_frame.pack(pady=5, anchor=tk.W)
profile_label = tk.Label(profile_frame, text="Profile Name:")
profile_label.pack(side=tk.LEFT)
profile_entry = tk.Entry(profile_frame, width=30)
profile_entry.pack(side=tk.LEFT, padx=5)
save_profile_button = tk.Button(profile_frame, text="Save Profile", command=save_profile)
save_profile_button.pack(side=tk.LEFT)

# Create and pack the profile dropdown
profile_dropdown = ttk.Combobox(input_frame, state="readonly")
profile_dropdown.pack(pady=5, anchor=tk.W)
profile_dropdown.bind("<<ComboboxSelected>>", load_profile)

# Load profiles from file
load_profiles_from_file()

# Update profile dropdown with loaded profiles
update_profile_dropdown()

# Start the GUI event loop
window.mainloop()