import subprocess
import sys
import selectors
from .default import PPM_Default


class Run:
    def __init__(self) -> None:
        self.ppm = PPM_Default()
        self.script = ""

    def create_script(self):
        run_script = ""

        with open(self.ppm.meta_data_file_name, "r") as file:
            contents = file.readlines()
            line = contents[contents.index("[command]\n") + 1]
            line_content = line.split(" ")

            if line_content[0] == "run":
                run_script = f"{line_content[2][1:]} {line_content[3].split('"')[0]}"

            else:
                self.ppm.animation.stop(
                    "No run command found in the configuration file"
                )
                sys.exit(0)

        self.script = self.ppm.generate_script([run_script])

    def interpret_code(self):
        # Start the subprocess
        process = subprocess.Popen(
            self.script,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        # Set up a selector to handle non-blocking I/O
        sel = selectors.DefaultSelector()
        sel.register(process.stdout, selectors.EVENT_READ)
        sel.register(sys.stdin, selectors.EVENT_READ)

        try:
            while True:
                for key, _ in sel.select():
                    if key.fileobj is process.stdout:
                        # Read a line of output from the process and print it
                        output_line = process.stdout.readline()
                        if output_line:
                            print(output_line, end="")

                    elif key.fileobj is sys.stdin:
                        # Read user input and send it to the process
                        user_input = sys.stdin.readline()
                        if user_input:
                            process.stdin.write(user_input)
                            process.stdin.flush()  # Ensure input is sent

                # Break if the process has finished
                if process.poll() is not None:
                    break

            # Print any remaining output or error after process exits
            remaining_output = process.stdout.read()
            if remaining_output:
                print(remaining_output, end="")
            error_output = process.stderr.read()
            if error_output:
                print("Error:", error_output)

        except KeyboardInterrupt:
            print("Runner interrupted by user.")
            process.terminate()
            process.wait()

        finally:
            sel.unregister(process.stdout)
            sel.unregister(sys.stdin)

    def run(self):
        self.ppm.check_configuration_file_file()
        self.create_script()
        try:
            self.interpret_code()
        except KeyboardInterrupt:
            print("Runner interrupted, exiting.")
            sys.exit(1)
