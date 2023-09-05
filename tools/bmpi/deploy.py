import json

def run_command(args):
    with open(args.config, "r") as f:
        dump = json.load(f)
    applications = dump["applications"]
    for app in applications:
        print(f"deploying {app} onto {args.device}")

def setup(subparsers):
    parser = subparsers.add_parser("deploy", help="deploy applications to device")
    parser.add_argument("-c", "--config", help="config file for device", required=True)
    parser.add_argument("-d", "--device", help="target device name", required=True)
    parser.set_defaults(func=run_command)
