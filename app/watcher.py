from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.files import read_project_files


class ProjectWatcher(FileSystemEventHandler):

    def refresh(self):
        documents = read_project_files("data/sample-project")

        print(
            f"NOVA: Project context refreshed → "
            f"{len(documents)} files"
        )

    def on_modified(self, event):
        if not event.is_directory:
            print(f"NOVA: File modified → {event.src_path}")
            self.refresh()

    def on_created(self, event):
        if not event.is_directory:
            print(f"NOVA: File created → {event.src_path}")
            self.refresh()

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"NOVA: File deleted → {event.src_path}")
            self.refresh()


def start_watcher(path: str):
    observer = Observer()

    observer.schedule(
        ProjectWatcher(),
        path,
        recursive=True,
    )

    observer.start()

    return observer