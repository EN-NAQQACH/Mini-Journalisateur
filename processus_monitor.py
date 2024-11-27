from tkinter import ttk

def setup_ui(root):
    # Configure styles
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    # Main content
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Process Logs Tab
    process_tab = ttk.Frame(notebook)
    notebook.add(process_tab, text="Process Logs")

    process_table = ttk.Treeview(process_tab, columns=("Action", "Name", "PID", "Time"), show="headings")
    process_table.heading("Action", text="Action")
    process_table.heading("Name", text="Name")
    process_table.heading("PID", text="PID")
    process_table.heading("Time", text="Time")
    process_table.pack(expand=True, fill="both", padx=10, pady=10)

    # Return process_table for further use
    return process_table
