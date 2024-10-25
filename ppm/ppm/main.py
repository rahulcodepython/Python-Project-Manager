# import argparse


# def hello():
#     print("Hello World")


# def run():
#     for i in range(1, 11):
#         print(i)


# def main():
#     parser = argparse.ArgumentParser(prog="ppm")
#     subparsers = parser.add_subparsers(dest="command")

#     # Add 'hello' command
#     hello_parser = subparsers.add_parser("hello", help="Prints Hello World")
#     hello_parser.set_defaults(func=hello)

#     # Add 'run' command
#     run_parser = subparsers.add_parser("run", help="Prints numbers from 1 to 10")
#     run_parser.set_defaults(func=run)


#     # Parse arguments and call the appropriate function
#     args = parser.parse_args()
#     if args.command:
#         args.func()
#     else:
#         parser.print_help()
def main():
    print("Hello World")
