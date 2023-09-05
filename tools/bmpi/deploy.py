import os

def run_command(args):
    print("Executing Command 1")
    print(args)

def setup(subparsers):
    parser = subparsers.add_parser("deploy", help="deploy applications to device")
    parser.add_argument("-c", "--config", help="config file for device", required=True)
    parser.add_argument("-d", "--device", help="target device name", required=True)
    parser.set_defaults(func=run_command)
