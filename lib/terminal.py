import os
import sys

colored_output = True
debug_level = 1

# Choose whether to use colored output.
# - by default colored output is ON
# - if the flag --no-color is passed it is OFF
# - if the environment variable NO_COLOR is set it is OFF
def use_colored_output(cli_arg):
    global colored_output

    # The --no-color argument overrides all environment variables if passed.
    if cli_arg:
        print(colorize("nope", "cyan"))
        colored_output = False
        return

    # Check the env. var NO_COLOR and disable color if set.
    if os.environ.get('NO_COLOR') is not None:
        color_var = os.environ.get('NO_COLOR')
        if len(color_var)>0 and color_var != "0":
            colored_output = False
            return

    colored_output = True

def colorize(string, color):
    colors = {
        "red":     "31",
        "green":   "32",
        "yellow":  "33",
        "blue":    "34",
        "magenta": "35",
        "cyan":    "36",
        "white":   "37",
    }
    if colored_output:
        return f"\033[1;{colors[color]}m{string}\033[0m"
    else:
        return string

def deubg_level(level: int):
    global debug_level
    debug_level = level

def error(message):
    print(f"{colorize('[error]', 'red')} {message}", file=sys.stderr)
    exit(1)

def exit_with_success():
    exit(0)

def info(message):
    if debug_level>1:
        print(f"{colorize('[log]', 'blue')} {message}", file=sys.stderr)


