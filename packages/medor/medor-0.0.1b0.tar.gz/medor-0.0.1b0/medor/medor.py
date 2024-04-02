# coding: utf-8
"""medor

Find a WordPress website IP behind a WAF or behind Onion Services.
It works if there is at least a blog post and if xmlrpc.php has not been secured.

Usage:
    medor find <item> [--item-type=<domain|site|post>] [--proxy=<proxy>|--onion]
    medor check_wp <url> [--proxy=<proxy>|--onion]
    medor tor_setup

Arguments:
    find                                Find WP IP
    <item>                              Item to investigate, matching the --item-type:
                                            domain.tld for domain (e.g. website.com)
                                            website URL for site (e.g. https://www.website.com)
                                            post URL for post (e.g. https://www.website.com/a-blog-post)
    tor_setup                           Setup tor for medor

Options:
    -h --help                           Show this help
    -v --version                        Show medor version
    -t --item-type=<domain|site|post>   Item type to investigate [default: domain]
                                            domain (domain.tld, e.g. website.com)
                                            site (website URL, e.g. https://www.website.com)
                                            post (post URL, e.g. https://www.website.com/a-blog-post)
    -p --proxy=<proxy>                  Optional. Proxy to use :
                                            with authentication : scheme://user:password@ip:port
                                            without authentication : scheme://ip:port
    -o --onion                          For onion websites. Requires tor setup

"""

from colorama import Fore
from docopt import docopt

import medor.utils.globals_ as globals_
from medor.__about__ import __version__
from medor.utils.bone import Bone
from medor.utils.tor import setup
from medor.utils.util import failure


def main():
    args = docopt(__doc__, version="medor v" + __version__)
    proxy = None
    onion = False
    if args["--proxy"]:
        proxy = args["--proxy"]
    if args["--onion"]:
        onion = True
        if not globals_.check_globals():
            exit(f"{failure}   {Fore.RED}You need to set up tor if you want to use medor with .onion websites.\n"
                 """    Check the doc.""")
    if args["tor_setup"]:
        setup()
    if args["find"]:
        if args["--item-type"] == "domain" or args["--item-type"] == "site" or args["--item-type"] == "post":
            Bone(args["--item-type"], args["<item>"], proxy=proxy, onion=onion)
        else:
            exit("{failure}   {Fore.RED}You used an invalid item-type\n"
                 """    --item-type should be either "domain", "site" or "post", matching the item investigated.""")


if __name__ == "__main__":
    main()
