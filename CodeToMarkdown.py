import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select Files")
    file_listbox.delete(0, tk.END)
    for file in selected_files:
        file_listbox.insert(tk.END, file)

def collect_code():
    if not selected_files:
        messagebox.showwarning("Warning", "No files selected.")
        return

    output_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Output File", defaultextension=".txt")
    if not output_file:
        return

    with open(output_file, "w") as output:
        for file in selected_files:
            file_name = os.path.basename(file)
            output.write(f"<{file_name}>\n```\n")
            with open(file, "r") as f:
                code = f.read()
                output.write(code + "\n```")

    messagebox.showinfo("Success", "Code collected and saved successfully.")

# Create the main window
window = tk.Tk()
window.title("Code Collector")

# Create and pack the file listbox
file_listbox = tk.Listbox(window, width=50)
file_listbox.pack(pady=10)

# Create and pack the buttons
select_button = tk.Button(window, text="Select Files", command=select_files)
select_button.pack(pady=5)

collect_button = tk.Button(window, text="Collect Code", command=collect_code)
collect_button.pack(pady=5)

# Start the GUI event loop
window.mainloop()