# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import time
# import os  # Import os to get file stats
# from datetime import datetime

# class Watcher(FileSystemEventHandler):
#     def on_modified(self, event):
#         if not event.is_directory:
#             file_stats = os.stat(event.src_path)  # Get the file's stats
#             mod_time = time.ctime(file_stats.st_mtime)  # Get modification time
#             print(f"File modified: {event.src_path}, Time: {mod_time}")

#     def on_created(self, event):
#         if not event.is_directory:
#             file_stats = os.stat(event.src_path)  # Get the file's stats
#             create_time = time.ctime(file_stats.st_ctime)  # Get creation time
#             print(f"File created: {event.src_path}, Time: {create_time}")

#     def on_deleted(self, event):
#         if not event.is_directory:
#             print(f"File deleted: {event.src_path}")

# if __name__ == "__main__":
#     path_to_monitor = "./logs"  # Change this to the directory you want to monitor
#     event_handler = Watcher()
#     observer = Observer()
#     observer.schedule(event_handler, path_to_monitor, recursive=True)
#     observer.start()
#     print(f"Monitoring changes in: {path_to_monitor}")
    
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class Watcher(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            mod_time = time.ctime(os.path.getmtime(event.src_path))
            print(f"File modified: {event.src_path}, Time: {mod_time}")

    def on_created(self, event):
        if not event.is_directory:
            create_time = time.ctime(os.path.getctime(event.src_path))
            print(f"File created: {event.src_path}, Time: {create_time}")

    def on_deleted(self, event):
        if not event.is_directory:
            delete_time = time.ctime(time.time())  # Use current time for deletion
            print(f"File deleted: {event.src_path}, Time: {delete_time}")

if __name__ == "__main__":
    # Ask the user for a directory to monitor (can be the root directory)
    path_to_monitor = input("Enter the path to monitor (e.g., C:\\ or D:\\folder\\): ")
    
    if not os.path.exists(path_to_monitor):
        print(f"The specified path {path_to_monitor} does not exist.")
    else:
        event_handler = Watcher()
        observer = Observer()
        observer.schedule(event_handler, path_to_monitor, recursive=True)
        observer.start()
        print(f"Monitoring changes in: {path_to_monitor}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
