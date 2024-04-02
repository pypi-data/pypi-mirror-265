# coding: utf-8
import base64
import fileinput
import subprocess
from pathlib import Path

import httpx
import stem
from stem import Signal, process, CircStatus
from stem.control import Controller
from stem.version import get_system_tor_version, Requirement

import medor.utils.globals_ as globals_
from medor.utils import net
from medor.utils.util import success, failure, warning, spinner


class Tor:
    def __init__(self):
        self.tor_binary_path = str(globals_.tor["tor_binary_path"])
        self.tor_pwd = self.pw_decode(globals_.tor["tor_plain"])
        self.net = net.Net(onion=True)
        self.launch()

    def launch(self):
        self.ini_connection()
        self.new_id()
        self.verify_tor()

    def ini_connection(self):
        spinner.start("Initializing tor")
        try:
            with Controller.from_port(port=globals_.tor["controller_port"]) as co:
                spinner.start("Refreshing tor route")
                co.authenticate(self.tor_pwd)
                if co.get_info("status/circuit-established") == "1":
                    co.close()
                    spinner.stop_and_persist(symbol=success, text="Tor initialized")
                    return
        except stem.SocketError as e:
            try:
                self.start()
            except OSError as e:
                self.shutdown()
                self.ini_connection()
                print(
                    "Your tor configuration (tor path and password,...) is not set or is not right."
                )

    def start(self):
        if (
            get_system_tor_version(self.tor_binary_path)
            >= Requirement.TORRC_CONTROL_SOCKET
        ):
            try:
                tor_process = process.launch_tor_with_config(
                    config={
                        "ControlPort": str(globals_.tor["controller_port"]),
                        "HashedControlPassword": globals_.tor["tor_hashed"],
                        "CookieAuthentication": "1",
                    },
                    tor_cmd=self.tor_binary_path,
                    completion_percent=100,
                )
            except OSError as e:
                spinner.stop()
                exit(
                    f"{failure}  Tor might be already running. Shut down tor process"
                    f"{e}\n"
                )
        else:
            spinner.stop()
            exit(f"{failure}  Please, update tor.\n")

    def new_id(self):
        spinner.start("Setting new tor identity")
        with Controller.from_port(port=globals_.tor["controller_port"]) as co:
            co.authenticate(self.tor_pwd)
            recommended = co.get_info("status/version/recommended").split(",")
            self.tor_recommended(recommended)
            if co.is_newnym_available():
                co.signal(Signal.NEWNYM)
                co.close()
                spinner.stop_and_persist(symbol=success, text="Tor new identity set")

    def shutdown(self):
        spinner.start("Shutting down tor")
        with Controller.from_port(port=globals_.tor["controller_port"]) as co:
            spinner.start("Refreshing tor route")
            co.authenticate(self.tor_pwd)
            co.signal(Signal.HALT)
            spinner.stop_and_persist(symbol=success, text="Tor shut down")

    def verify_tor(self):
        spinner.start("Checking Tor Exit IP")
        try:
            res = self.net.connect("https://check.torproject.org/api/ip")
            if res.status_code == 200:
                is_tor = res.json()["IsTor"]
                ip = res.json()["IP"]
                if is_tor:
                    spinner.stop_and_persist(
                        symbol=success, text=f"Tor is ok. Exit IP: {ip}"
                    )
                    return
            else:
                raise httpx.HTTPError
        except httpx.HTTPError:
            real_ip = self.net.get_real_ip()
            exit_node = self.get_exit()
            if real_ip != exit_node:
                spinner.stop_and_persist(
                    symbol=success, text=f"Tor exit check. Exit IP: {exit_node}"
                )
                return
            else:
                spinner.stop_and_persist(
                    symbol=failure, text=f"Can't verify tor exit IP. Exiting."
                )
                exit(1)
        spinner.stop_and_persist(symbol=failure, text=f"Tor is not active. Exiting")
        exit(1)

    def get_exit(self):
        with Controller.from_port(port=9051) as co:
            co.authenticate(self.tor_pwd)

            for circ in co.get_circuits():
                if circ.status != CircStatus.BUILT:
                    continue

            exit_fp, exit_nickname = circ.path[-1]

            exit_desc = co.get_network_status(exit_fp, None)
            exit_address = exit_desc.address if exit_desc else "unknown"
            co.close()
            return exit_address

    def tor_recommended(self, recommended):
        present = str(get_system_tor_version(self.tor_binary_path)).split(" ")[0]
        if present not in recommended:
            spinner.stop_and_persist(
                symbol=warning, text=f"Update tor, highly recommended for security."
            )
        return

    def pw_decode(self, b_pass: bytes) -> str:
        return base64.b64decode(b_pass).decode("utf-8")


def write_tor_controller(plain: bytes, hashed: str, path: str) -> None:
    with fileinput.input(
        Path(Path(__file__).parent, "globals_.py"), inplace=True, encoding="utf-8"
    ) as f:
        for line in f:
            if '    "tor_plain":' in line:
                line = f'    "tor_plain": {plain},\n'
            if """    "tor_hashed":""" in line:
                line = f'    "tor_hashed": "{hashed}",\n'
            if '    "tor_binary_path":' in line:
                line = f'    "tor_binary_path": Path(r"{path}"),\n'
            print(line, end="")


def create_tor_hash(tor_pw, tor_path):
    tor_pass = subprocess.run(
        [Path(tor_path), "--hash-password", tor_pw],
        capture_output=True,
        text=True,
    )
    if stem.util.system.is_windows():
        hashed = tor_pass.stdout.splitlines()[2]
    else:
        hashed = tor_pass.stdout.replace("\n", "")
    return hashed


def setup() -> None:
    import pwinput

    tor_pass = pwinput.pwinput(prompt="A new password to connect to tor: ", mask="*")
    if len(tor_pass) == 0:
        exit(f"{failure}   You should enter a password.")
    tor_path = input(r'Tor binary path (e.g. "C:\Tor\tor.exe" for windows,'
                     """\n"/usr/bin/tor" or "tor" for linux) : """)
    if len(tor_path) == 0:
        exit(f"{failure}   You should enter a path.")
    tor_pass_e = base64.b64encode(tor_pass.encode("utf-8"))
    tor_pass_hash = create_tor_hash(tor_pass, tor_path)
    write_tor_controller(tor_pass_e, tor_pass_hash, tor_path)
