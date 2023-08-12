from AutoKGC.tools.config_manager import ConfigManager


def add_arguments(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--init",
        action="store_true"
    )


def main(args):
    config_manager = ConfigManager()
    if args.init:
        config_manager.init_local_config()
