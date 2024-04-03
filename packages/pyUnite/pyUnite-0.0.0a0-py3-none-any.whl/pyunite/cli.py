import sys
import importlib.metadata

def parse_args():
    """
    Parse command-line arguments.
        The formatting used for the parsing:
            | an arguement with a value is given as --arg=value
            | an arguement without a value is given as --arg and will be set to True
            | an arguement that starts with a - is always an alias for a diffrent argument.
            | an arguement that doesnt start with -- or - will be ignored.
    """
    rawArgs = sys.argv[1:]
    parsedArgs = {}
    for arg in rawArgs:
        if arg.startswith("--"):
            if "=" in arg:
                key, value = arg.split("=")
                parsedArgs[key] = value
            else:
                parsedArgs[arg[2:]] = True
        elif arg.startswith("-"):
            if arg[1:] == "h":
                parsedArgs["help"] = True
            elif arg[1:] == "v":
                parsedArgs["version"] = True
            else:
                continue
        else:
            continue

    return parsedArgs

def get_arg(argName):
    """
    Get the value of an arguement.
    """
    if not argName in args:
        return False
    else:
        return args[argName]


def print_help():
    print("Usage: pyunite [args]")
    print()
    print("Actions:")
    print("  -h, --help\t\tShow this help message and exit.")
    print("  -v, --version\tShow version and exit.")

def print_version():
    version = importlib.metadata.version('pyUnite')
    print(f"pyUnite version {version}")
    print("View latest version at https://github.com/riley0122/pyunite/releases/latest")

args = parse_args()

def cli():
    """Main CLI entry point."""
    if get_arg("help"):
        print_help()
        exit(0)
    elif get_arg("version"):
        print_version()
        exit(0)