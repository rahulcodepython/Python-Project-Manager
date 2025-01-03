import sys


def operation_termination(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n Operation is terminated.")
            sys.exit(0)

    return wrapper
