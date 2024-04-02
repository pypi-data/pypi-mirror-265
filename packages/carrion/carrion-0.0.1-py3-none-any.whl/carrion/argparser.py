import argparse


def create_parser(name):
    """Create, name, and return a parser object.

    Parameters:
        name (str): the name of the parser

    Returns:
        parser (argparse.ArgumentParser): a parser object
    """

    parser = argparse.ArgumentParser(
        prog=name,
        description="Welcome to %(prog)s! We're here to help you scavenge your specimens.",
        epilog="Thanks for using %(prog)s! Have a great day!",
        usage="%(prog)s [options]",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="The query string with which to search Google Scholar.",
    )
    parser.add_argument(
        "-o",
        "--offset",
        type=int,
        required=False,
        default=0,
        help="The start page.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=1,
        help="The number of pages of results to return.",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        required=False,
        default=1900,
        help="The start publication date.",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        required=False,
        default=2023,
        help="The end publication date.",
    )
    return parser
