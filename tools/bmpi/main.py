import argparse
from bmpi import deploy

def main():
    parser = argparse.ArgumentParser(description="BMPI CLI tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", required=True)

    deploy.setup(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
