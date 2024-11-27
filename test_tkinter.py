import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler # gérer les event like creating , deleting
import psutil
import threading
import pandas as pd

os.environ['TCL_LIBRARY'] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files\Python313\tcl\tk8.6"

# Tkinter application setup inistailisation de l'interface 
root = tk.Tk()
root.title("Mini Journalisateur")
root.geometry("1000x650")
root.configure(bg="#edf2f7") 

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

# Global variables
monitoring = True # Contrôle si la surveillance est active ou non.
file_observer = None # Objet utilisé pour surveiller les fichiers.
running_processes = {} # Dictionnaire pour suivre les processus actifs.



def select_directory():
    global file_observer
    path_to_monitor = filedialog.askdirectory(title="Select a directory to monitor")
    if path_to_monitor:
        start_file_monitoring(path_to_monitor)
        start_process_monitoring()
        messagebox.showinfo("Monitoring Started", f"Monitoring started for: {path_to_monitor}")
    else:
        messagebox.showwarning("No Directory Selected", "Please select a directory to monitor.")

def toggle_monitoring():
    global monitoring
    monitoring = not monitoring
    toggle_label.config(text="Monitoring Paused" if not monitoring else "Monitoring Active")
    toggle_button.config(text="Resume" if not monitoring else "Pause")

def start_file_monitoring(path_to_monitor):
    global file_observer
    event_handler = FileMonitorHandler() # An instance of a class handler les evenements (creation , modification)
    file_observer = Observer()
    file_observer.schedule(event_handler, path_to_monitor, recursive=True) # tells the file_observer to start monitoring a specific path for changes.
    file_observer.start()

def monitor_processes():
    while True:
        if monitoring:
            #récupération les processus actif
            current_processes = {proc.info['pid']: proc.info for proc in psutil.process_iter(['pid', 'name', 'create_time'])}

            # New processes
            for pid, proc_info in current_processes.items():
                if pid not in running_processes:
                    running_processes[pid] = {
                        'name': proc_info['name'],
                        'start_time': datetime.fromtimestamp(proc_info['create_time']),
                        'status': 'Running'
                    }
                    action = "Started"
                    process_table.insert("", "end", values=(action, proc_info['name'], pid, running_processes[pid]['start_time']))

            # Stopped processes
            for pid in list(running_processes.keys()):
                if pid not in current_processes:
                    stop_time = datetime.now()
                    action = "Stopped"
                    process_table.insert("", "end", values=(action, running_processes[pid]['name'], pid, stop_time), tags=("stopped",))
                    del running_processes[pid]

        time.sleep(1) #pause before cheking again

def start_process_monitoring(): 
    process_thread = threading.Thread(target=monitor_processes, daemon=True)
    process_thread.start()

class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if monitoring and not event.is_directory:
            mod_time = time.ctime(os.path.getmtime(event.src_path))
            action = "Modified"
            file_table.insert("", "end", values=(action, event.src_path, mod_time))

    def on_created(self, event):
        if monitoring and not event.is_directory and os.path.exists(event.src_path):
            create_time = time.ctime(os.path.getctime(event.src_path))
            action = "Created"
            file_table.insert("", "end", values=(action, event.src_path, create_time))

    def on_deleted(self, event):
        if monitoring and not event.is_directory:
            delete_time = time.ctime(time.time())
            action = "Deleted"
            file_table.insert("", "end", values=(action, event.src_path, delete_time))




# Tkinter layout
## Sidebar
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

toggle_label = ttk.Label(sidebar_frame, text="Monitoring Active", font=("Helvetica", 12))
toggle_label.pack(pady=5)

toggle_button = ttk.Button(sidebar_frame, text="Pause", command=toggle_monitoring)
toggle_button.pack(fill="x", pady=5)

separator_export = ttk.Separator(sidebar_frame, orient="horizontal")
separator_export.pack(fill="x", pady=10)

export_file_button = ttk.Button(sidebar_frame, text="Export File Logs", command=lambda: export_logs("file"))
export_file_button.pack(side="bottom",fill="x", pady=5)

export_process_button = ttk.Button(sidebar_frame, text="Export Process Logs", command=lambda: export_logs("process"))
export_process_button.pack(side="bottom",fill="x", pady=5)

## Content Area
content_frame = ttk.Frame(root, padding=2, style="RoundedFrame.TFrame")
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

notebook = ttk.Notebook(content_frame)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

file_tab = ttk.Frame(notebook)
process_tab = ttk.Frame(notebook)
notebook.add(file_tab, text="File Logs")
notebook.add(process_tab, text="Process Logs")

file_frame = ttk.Frame(file_tab, padding=10)
file_frame.pack(fill="both", expand=True, padx=5, pady=5)

process_frame = ttk.Frame(process_tab, padding=10)
process_frame.pack(fill="both", expand=True, padx=5, pady=5)

## File Logs Table
file_table = ttk.Treeview(file_frame, columns=("Action", "Path", "Time"), show="headings")
file_table.heading("Action", text="Action")
file_table.heading("Path", text="Path")
file_table.heading("Time", text="Time")
file_table.pack(fill="both", expand=True, padx=5, pady=5)

file_scroll = ttk.Scrollbar(file_frame, orient="vertical", command=file_table.yview)
file_table.configure(yscroll=file_scroll.set)
file_scroll.pack(side="right", fill="y")

## Process Logs Table
process_table = ttk.Treeview(process_frame, columns=("Action", "Name", "PID", "Time"), show="headings")
process_table.heading("Action", text="Action")
process_table.heading("Name", text="Name")
process_table.heading("PID", text="PID")
process_table.heading("Time", text="Time")
process_table.pack(fill="both", expand=True, padx=5, pady=5)

process_scroll = ttk.Scrollbar(process_frame, orient="vertical", command=process_table.yview)
process_table.configure(yscroll=process_scroll.set)
process_scroll.pack(side="right", fill="y")

process_table.tag_configure("stopped", foreground="red")

def export_logs(log_type):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        if log_type == "file":
            data = [file_table.item(item)["values"] for item in file_table.get_children()]
            df = pd.DataFrame(data, columns=["Action", "Path", "Time"])
        elif log_type == "process":
            data = [process_table.item(item)["values"] for item in process_table.get_children()]
            df = pd.DataFrame(data, columns=["Action", "Name", "PID", "Time"])
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Success", f"{log_type.capitalize()} logs exported successfully to {file_path}")
# Start application
root.mainloop()
