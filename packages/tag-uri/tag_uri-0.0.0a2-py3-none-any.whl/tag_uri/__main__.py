"""Main module for parsing a tag_uri.

The tag_uri can be parsed from the command line or from stdin. The output is yaml with
the parsed tag_uri.
"""

import argparse
import sys

import yaml

from .tag_uri import TagURI


def main():
    parser = argparse.ArgumentParser(description="Parse tag_uri")
    parser.add_argument(
        "tag_uri",
        type=str,
        help="The tag_uri to parse. If omitted will read from stdin.",
        nargs="*",
    )
    args = parser.parse_args(sys.argv[1:])
    if args.tag_uri:
        tags = [TagURI.parse(arg) for arg in args.tag_uri]
        yaml.dump_all([tag.as_dict() for tag in tags], sys.stdout)
    else:
        for line in sys.stdin:
            tag = TagURI.parse(line.strip())
            yaml.dump_all([tag.as_dict()], sys.stdout)


if __name__ == "__main__":
    main()
