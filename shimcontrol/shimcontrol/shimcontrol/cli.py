import argparse
import sys

from tabulate import tabulate

from shimcontrol.lib import ADCCommandSet, DACCommandSet, dac_code_to_voltage

def subcommand(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)

            return False

        return True

    return func


@subcommand
def get_action(args):
    adc = ADCCommandSet(5)
    adc.from_read(args.channels)

    results = adc.execute()

    print(tabulate(
        [(ch, '{:1.3f}'.format(r)) for ch, r in results],
        headers=['Channel', 'Voltage'],
    ))

@subcommand
def set_action(args):
    dac = DACCommandSet(5)
    dac.from_write(args.channels)

    dac.execute()

    outputs = [
        (channel, code, dac_code_to_voltage(code))
        for channel, code in args.channels
    ]

    print(tabulate(
        outputs,
        headers=['Channel', 'Value', 'Voltage'],
    ))

@subcommand
def list_action(args):
    print(args)


class ChannelValuesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        channels = []
        for pair in values:
            channel, value = pair.split('=')
            channels.append((
                int(channel), int(value, 0)
            ))

        setattr(namespace, self.dest, channels)


def build_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list', help='List channels')
    list_parser.set_defaults(func=list_action)

    get_parser = subparsers.add_parser('get', help='Get channel data')
    get_parser.set_defaults(func=get_action)
    get_parser.add_argument('channels', nargs='+', type=int)

    set_parser = subparsers.add_parser('set', help='Set channel data')
    set_parser.set_defaults(func=set_action)
    set_parser.add_argument('channels', nargs='+', action=ChannelValuesAction)

    return parser

def main():
    parser = build_parser()

    args = parser.parse_args()

    if hasattr(args, 'func'):
        if args.func(args):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
