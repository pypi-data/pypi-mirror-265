from ..Environment import Environment
from .Daemon import Deamon
import sys


def main() -> None:
    env = Environment()

    daemon = Deamon(env)

    if daemon.is_running():
        print("The daemon is already running", file=sys.stderr)
        sys.exit(1)

    daemon.prepare()
    daemon.open()
    daemon.start_ydotoold()
    daemon.prepare_shortcuts()
    daemon.listen()
