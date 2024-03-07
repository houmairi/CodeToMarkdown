import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory")
    if selected_directory:
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

def collect_code():
    selected_files = [file_tree.item(item)["values"][0] for item in file_tree.selection()]
    if not selected_files:
        messagebox.showwarning("Warning", "No files selected.")
        return

    output_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Output File", defaultextension=".txt")
    if not output_file:
        return

    with open(output_file, "w") as output:
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            output.write(f"<{file_name}>\n```\n")
            with open(file_path, "r") as f:
                code = f.read()
                output.write(code + "\n```\n")

    messagebox.showinfo("Success", "Code collected and saved successfully.")

# Create the main window
window = tk.Tk()
window.title("Code Collector")

# Create and pack the directory selection button
select_directory_button = tk.Button(window, text="Select Directory", command=select_directory)
select_directory_button.pack(pady=10)

# Create and pack the file treeview
file_tree = ttk.Treeview(window, columns=("Path",), show="tree", selectmode="extended")
file_tree.heading("#0", text="Files")
file_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Create and pack the collect code button
collect_button = tk.Button(window, text="Collect Code", command=collect_code)
collect_button.pack(pady=5)

# Start the GUI event loop
window.mainloop()