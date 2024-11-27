import psutil
import time
import os
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setting up the file event logger
file_log_file = 'file_logs.txt'
file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(file_log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
file_logger.addHandler(file_handler)

# Setting up the process event logger
process_log_file = 'processus_logs.txt'
process_logger = logging.getLogger('process_logger')
process_logger.setLevel(logging.INFO)
process_handler = logging.FileHandler(process_log_file)
process_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
process_logger.addHandler(process_handler)

# Dictionary to store process information with PID as the key
running_processes = {}

# Function to log file events (created, modified, deleted)
class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        log_message = f"File modified: {event.src_path} at {datetime.now()}"
        print(log_message)  # Print to console for real-time feedback
        file_logger.info(log_message)  # Log to the file

    def on_created(self, event):
        if event.is_directory:
            return
        log_message = f"File created: {event.src_path} at {datetime.now()}"
        print(log_message)  # Print to console for real-time feedback
        file_logger.info(log_message)  # Log to the file

    def on_deleted(self, event):
        if event.is_directory:
            return
        log_message = f"File deleted: {event.src_path} at {datetime.now()}"
        print(log_message)  # Print to console for real-time feedback
        file_logger.info(log_message)  # Log to the file

# Function to monitor processes
def monitor_processes():
    while True:
        # Get the list of all currently running processes
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                create_time = proc.info['create_time']
                
                # Check if process is new (not in our dictionary)
                if pid not in running_processes:
                    running_processes[pid] = {
                        'name': name,
                        'start_time': datetime.fromtimestamp(create_time),
                        'status': 'Running'
                    }
                    log_message = f"Process Started: {name} (PID: {pid}) at {running_processes[pid]['start_time']}"
                    print(log_message)  # Print to console for real-time feedback
                    process_logger.info(log_message)  # Log to the file
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Check for stopped processes
        for pid in list(running_processes.keys()):
            try:
                proc = psutil.Process(pid)
                if not proc.is_running():
                    # Log process exit time
                    stop_time = datetime.now()
                    log_message = f"Process Stopped: {running_processes[pid]['name']} (PID: {pid}) at {stop_time}"
                    print(log_message)  # Print to console for real-time feedback
                    process_logger.info(log_message)  # Log to the file
                    del running_processes[pid]  # Remove process from the tracking list
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Wait for 1 second before checking again
        time.sleep(1)

if __name__ == "__main__":
    # Ask user for the path to monitor (can be modified to monitor entire system)
    path_to_monitor = input("Enter the path to monitor (e.g., C:\\ or D:\\folder\\): ")

    # Set up the file system event handler
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_monitor, recursive=True)
    observer.start()
    
    print(f"Monitoring changes in: {path_to_monitor}")
    file_logger.info(f"Started monitoring changes in: {path_to_monitor}")
    
    # Start the process monitoring in a separate thread or process
    try:
        monitor_processes()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
