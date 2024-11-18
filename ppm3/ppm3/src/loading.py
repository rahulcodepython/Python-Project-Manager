import threading
import time
import sys


class Loading:
    def __init__(self):
        self.stop_event = threading.Event()
        self.animation_thread = None

    def _animate(self, message: str):
        for frame in ["   ", ".  ", ".. ", "...", ".. ", ".  "]:
            if self.stop_event.is_set():
                break
            sys.stdout.write(f"\r{message} {frame}")
            sys.stdout.flush()
            time.sleep(0.3)

    def start(self, message="Loading"):
        # Stop any existing animation before starting a new one
        if self.animation_thread and self.animation_thread.is_alive():
            self.stop()

        # Clear the stop event and start a new animation thread
        self.stop_event.clear()
        self.animation_thread = threading.Thread(target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self, message=None):
        # Set the stop event to terminate the animation loop
        if self.animation_thread:
            self.stop_event.set()
            self.animation_thread.join()
            sys.stdout.write("\n")  # Clear the animation
            print(message) if message else None
            sys.stdout.flush()
