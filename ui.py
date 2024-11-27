from tkinter import ttk
from file_monitor import select_directory
from utils import export_logs
from processus_monitor import start_process_monitoring

def setup_ui(root):
    # Configure ttk styles
    style = ttk.Style()
    style.configure("TNotebook", background="#edf2f7")
    style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=(10, 5))
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("TButton", font=("Helvetica", 11), padding=5)
    style.configure("Treeview", fieldbackground="#ffffff", background="#ffffff", borderwidth=1)
    style.configure("TFrame", background="#edf2f7")
    style.map("TButton", background=[("active", "#4caf50")])
    style.configure("RoundedFrame.TFrame", background="#ffffff", relief="solid", borderwidth=0)
    style.map("RoundedFrame.TFrame", background=[("active", "#f0f0f0")])

    # Sidebar
    sidebar_frame = ttk.Frame(root, width=200, padding=10, style="TFrame")
    sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)

    file_logs_button = ttk.Button(sidebar_frame, text="File Logs", style="TButton", command=lambda: notebook.select(file_tab))
    file_logs_button.pack(fill="x", pady=5)

    process_logs_button = ttk.Button(sidebar_frame, text="Process Logs", style="TButton", command=lambda: notebook.select(process_tab))
    process_logs_button.pack(fill="x", pady=5)

    separator = ttk.Separator(sidebar_frame, orient="horizontal")
    separator.pack(fill="x", pady=10)

    select_directory_button = ttk.Button(sidebar_frame, text="Select Directory", command=select_directory)
    select_directory_button.pack(fill="x", pady=5)

    export_file_button = ttk.Button(sidebar_frame, text="Export File Logs", command=lambda: export_logs("file"))
    export_file_button.pack(side="bottom", fill="x", pady=5)

    export_process_button = ttk.Button(sidebar_frame, text="Export Process Logs", command=lambda: export_logs("process"))
    export_process_button.pack(side="bottom", fill="x", pady=5)

    # Add additional UI components...
