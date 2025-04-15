import sys
from typing import Callable, Any
from .loading import Loading


def operation_termination(func: Callable) -> Callable:
    """
    Decorator to handle KeyboardInterrupt exceptions and terminate the program gracefully.

    Args:
        func (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapped function.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nOperation is terminated.")
            sys.exit(0)

    return wrapper


def loading_animation(message: str = "Loading") -> Callable:
    """
    Decorator to display a loading animation while the wrapped function is executing.

    Args:
        message (str): The message to display with the loading animation. Defaults to "Loading".

    Returns:
        Callable: The decorator function.
    """
    loading: Loading = Loading()

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Start loading animation
                loading.start(message=message)
                result = func(*args, **kwargs)
                loading.stop()
                return result
            except Exception as e:
                loading.stop()
                print("\nAn error occurred:", e)
                sys.exit(0)

        return wrapper

    return decorator
