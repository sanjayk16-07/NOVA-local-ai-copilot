import time
from app.watcher import start_watcher

observer = start_watcher("data/sample-project")

print("NOVA: Watchdog is running...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
