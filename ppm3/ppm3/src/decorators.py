import sys
from .loading import Loading


def operation_termination(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nOperation is terminated.")
            sys.exit(0)

    return wrapper


def loading_animation(message="Loading"):
    loading = Loading()

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                loading.start(message=message)
                # Start loading animation
                result = func(*args, **kwargs)
                loading.stop()  # Stop loading animation
                return result
            except Exception as e:
                loading.stop()
                print("\nAn error occurred:", e)
                sys.exit(0)
            finally:
                loading.stop()

        return wrapper

    return decorator
