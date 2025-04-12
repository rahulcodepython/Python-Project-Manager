import threading
import time
import sys


class Loading:
    """
    A class to display a loading animation in the console.

    Attributes:
        stop_event (threading.Event): Event to signal stopping the animation.
        animation_thread (Optional[threading.Thread]): Thread running the animation.
    """

    def __init__(self) -> None:
        """
        Initialize the Loading class with a stop event and animation thread.
        """
        self.stop_event: threading.Event = threading.Event()
        self.animation_thread: threading.Thread | None = None

    def _animate(self, message: str) -> None:
        """
        Private method to handle the animation loop.

        Args:
            message (str): The message to display alongside the animation.
        """
        frames: list[str] = ["   ", ".  ", ".. ", "...", ".. ", ".  "]
        while not self.stop_event.is_set():
            for frame in frames:
                if self.stop_event.is_set():
                    break
                sys.stdout.write(f"\r{message} {frame}")
                sys.stdout.flush()
                time.sleep(0.3)

    def start(self, message: str = "Loading") -> None:
        """
        Start the loading animation.

        Args:
            message (str): The message to display alongside the animation.
        """
        # Stop any existing animation before starting a new one
        if self.animation_thread and self.animation_thread.is_alive():
            self.stop()

        # Clear the stop event and start a new animation thread
        self.stop_event.clear()
        self.animation_thread = threading.Thread(
            target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self, message: str | None = None) -> None:
        """
        Stop the loading animation.

        Args:
            message (Optional[str]): An optional message to display after stopping.
        """
        if self.animation_thread:
            # Signal the animation thread to stop
            self.stop_event.set()
            self.animation_thread.join()

            # Clear the animation from the console
            sys.stdout.write("\n")
            sys.stdout.flush()

            # Print the optional message if provided
            if message:
                print(message)
