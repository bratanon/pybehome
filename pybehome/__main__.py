import argparse
import logging

from pybehome import PyBeHome

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

COMMAND_LOCATION = 'location'
COMMAND_DEVICES = 'devices'
COMMAND_SET_ARM_STATE = 'set_arm_state'


def main():
    """Start PyBeHome command line."""
    parser = argparse.ArgumentParser(
        description='Read or change status of WeBeHome devices')
    parser.add_argument(
        'username',
        help='Username')
    parser.add_argument(
        'password',
        help='Password')

    commandsparser = parser.add_subparsers(
        help='commands',
        dest='command')
    commandsparser.add_parser(
        COMMAND_LOCATION,
        help='Get information about the active location')
    commandsparser.add_parser(
        COMMAND_DEVICES,
        help='Get all devices')

    # Set alarm
    set_alarm = commandsparser.add_parser(
        COMMAND_SET_ARM_STATE,
        help='set alarm status')
    set_alarm.add_argument(
        'new_status',
        choices=[
            'ArmHome',
            'ArmAway',
            'Disarm'],
        help='new status')

    args = parser.parse_args()

    pybehome = PyBeHome(args.username, args.password)
    pybehome.login()

    if args.command == COMMAND_LOCATION:
        print(pybehome.get_location())
    if args.command == COMMAND_DEVICES:
        print(pybehome.get_devices())
    if args.command == COMMAND_SET_ARM_STATE:
        print(pybehome.set_arm_state(args.new_status))

    pybehome.token_destroy()


if __name__ == "__main__":
    main()
