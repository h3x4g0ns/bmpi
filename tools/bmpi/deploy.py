import json

def run_command(args):
    deploy_template = "bazel build --crosstool_top=//:arm_toolchain //tasks/{name}:{name}"
    with open(args.config, "r") as f:
        dump = json.load(f)
    applications = dump["applications"]
    cmds = []
    for app in applications:
        cmds.append(deploy_template.format(name=app))
    deploy_cmd = "cd common && "
    deploy_cmd += " && ".join(cmds)
    print(deploy_cmd)

def setup(subparsers):
    parser = subparsers.add_parser("deploy", help="deploy applications to device")
    parser.add_argument("-c", "--config", help="config file for device", required=True)
    parser.add_argument("-d", "--device", help="target device name", required=True)
    parser.set_defaults(func=run_command)
