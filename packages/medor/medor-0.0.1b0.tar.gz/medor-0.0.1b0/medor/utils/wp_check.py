# coding: utf-8
from colorama import Fore

import medor.utils.static as s
from medor.utils.globals_ import spinner
from medor.utils.waf import connect, test_site_url

_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "deflate",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Referrer": "https://google.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
}

url_signatures = {
    "urls": {
        1: "/wp-login.php",
        2: "/wp-content/",
        3: "/wp-admin/",
        4: "/wp-cron.php",
        5: "/xmlrpc.php",
        6: "/wp-json/wp/v2/",
        7: "/wp-content/themes/",
        8: "/wp-content/plugins/",
    },
}

string_signatures = {
    "license": {1: "/license.txt", 2: "WordPress"},
    "readme": {1: "/readme.html", 2: "WordPress"},
    "meta generator": {1: "", 2: """<meta name="generator" content="WordPress"""},
}


def url_sig_check(url):
    spinner.text = "Checking URL signatures"
    for signature in url_signatures:
        for sig in url_signatures[signature]:
            surl = url_signatures[signature][sig]
            res = connect(url + surl)
            if res.status_code == 200:
                spinner.stop_and_persist(
                    symbol=s.success,
                    text=f"""{Fore.GREEN}Looks like this website is built with WorPress.\n"""
                    f"""    URL signature {surl} has successfully been reached.""",
                )
                exit()


def string_sig_check(url):
    spinner.text = "Checking string signatures"
    for signature in string_signatures:
        surl = string_signatures[signature][1]
        sig = string_signatures[signature][2]
        res = connect(url + surl)
        if sig in res.text:
            spinner.stop_and_persist(
                symbol=s.success,
                text=f"""{Fore.GREEN}Looks like this website is built with WorPress.\n"""
                f""" String signature {signature} has successfully been reached.""",
            )
            exit()


def wp_check(url):
    spinner.start("Checking WordPress URL Signatures")
    if url.endswith("/"):
        url = url[:-1]
    test_site_url(url)
    url_sig_check(url)
    string_sig_check(url)
    spinner.stop()
    exit(
        f"{s.failure}  {url} website doesn't seem to be built with WordPress.\n"
        f"   No WP signature found."
    )
