from tkinter import filedialog, messagebox
import pandas as pd

def export_logs(log_type, table):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = [table.item(item)["values"] for item in table.get_children()]
        columns = {
            "file": ["Action", "Path", "Time"],
            "process": ["Action", "Name", "PID", "Time"]
        }[log_type]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Success", f"{log_type.capitalize()} logs exported successfully to {file_path}")
