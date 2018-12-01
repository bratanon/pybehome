import argparse
import logging

from pybehome import PyBeHome
from pybehome.constants import (ARM_HOME, ARM_AWAY, DISARM)

_LOGGER = logging.getLogger(__name__)

COMMAND_LOCATION = 'location'
COMMAND_DEVICES = 'devices'
COMMAND_ARM = 'arm'


def main():
    """Start PyBeHome command line."""
    parser = argparse.ArgumentParser('PyBeHome: Command Line Utility')
    parser.add_argument(
        '-u', '--username',
        help='Username', required=True)
    parser.add_argument(
        '-p', '--password',
        help='Password', required=True)
    parser.add_argument(
        '-l', '--location',
        help='Location id')

    commandsparser = parser.add_subparsers(
        help='commands',
        dest='command')

    commandsparser.add_parser(
        COMMAND_LOCATION,
        help='Get location data')
    commandsparser.add_parser(
        COMMAND_DEVICES,
        help='Get all device data')

    set_alarm = commandsparser.add_parser(
        COMMAND_ARM,
        help='Set alarm level')

    set_alarm.add_argument(
        'level',
        choices=[
            ARM_HOME,
            ARM_AWAY,
            DISARM],
        help='Alarm level')

    parser.add_argument(
        '--debug',
        help='Enable debug logging',
        required=False, default=False, action="store_true")

    parser.add_argument(
        '--quiet',
        help='Output only warnings and errors',
        required=False, default=False, action="store_true")

    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)

    pybehome = PyBeHome(args.username, args.password)
    pybehome.login()

    if args.command == COMMAND_LOCATION:
        pybehome.update_location()
        print(pybehome.get_location())
    if args.command == COMMAND_DEVICES:
        pybehome.update_devices()
        for device in pybehome.get_devices():
            print(device)
    if args.command == COMMAND_ARM:
        print(pybehome.set_alarm_state(args.level))

    pybehome.token_destroy()


if __name__ == "__main__":
    main()
