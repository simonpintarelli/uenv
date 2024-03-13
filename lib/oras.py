import subprocess

import terminal

def run_command(args):
    try:
        command = ['oras'] + args

        terminal.info(f"calling oras: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            check=True,  # Raise exception if command fails
            encoding='utf-8'  # Decode output from bytes to string
        )

        # Print standard output
        terminal.info("Output:\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        # Print error message along with captured standard error
        terminal.error("An error occurred:\n", e.stderr)

