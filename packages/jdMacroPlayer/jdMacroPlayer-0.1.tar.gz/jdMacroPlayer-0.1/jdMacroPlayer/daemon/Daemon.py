from ..Constants import DBUS_DAEMON_SERVICE_NAME
from ..Functions import is_flatpak
from typing import TYPE_CHECKING
import jeepney.io.blocking
import configparser
import subprocess
import tempfile
import jeepney
import secrets
import sys
import os


if TYPE_CHECKING:
    from ..Environment import Environment
    from ..core.Macro import Macro


class Deamon:
    def __init__(self, env: "Environment") -> None:
        self._env = env

        self._portal = jeepney.DBusAddress(
            object_path="/org/freedesktop/portal/desktop",
            bus_name="org.freedesktop.portal.Desktop",
        )
        self._global_shortcuts = self._portal.with_interface("org.freedesktop.portal.GlobalShortcuts")
        self._conn = jeepney.io.blocking.open_dbus_connection()

        with open(os.path.join(env.program_dir, "daemon", "interface.xml"), "r", encoding="utf-8") as f:
            self._introspect_data = f.read()

        self._activated_macros: dict[str, bool] = {}

    def is_running(self) -> bool:
        address = jeepney.DBusAddress(
            bus_name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface="org.freedesktop.DBus",
        )

        req = jeepney.new_method_call(address, "ListNames", "", ())
        rep = self._conn.send_and_get_reply(req)

        return DBUS_DAEMON_SERVICE_NAME in rep.body[0]

    def prepare(self) -> None:
        rep = self._conn.send_and_get_reply(jeepney.bus_messages.message_bus.RequestName(DBUS_DAEMON_SERVICE_NAME))
        if rep.body[0] != 1:
           sys.exit(1)

        if is_flatpak():
            background = self._portal.with_interface("org.freedesktop.portal.Background")
            jeepney.new_method_call(background, "RequestBackground", "sa{sv}", ("", {"reason": ("s", "Run Daemon in Background")}))

    def open(self) -> None:
        token = secrets.token_hex()
        sender_name = self._conn.unique_name[1:].replace('.', '_')
        handle = f"/org/freedesktop/portal/desktop/request/{sender_name}/{token}"

        response_rule = jeepney.bus_messages.MatchRule(
            type='signal', interface='org.freedesktop.portal.Request', path=handle
        )
        jeepney.io.blocking.Proxy(jeepney.bus_messages.message_bus, self._conn).AddMatch(response_rule)

        with self._conn.filter(response_rule) as responses:
            req = jeepney.new_method_call(self._global_shortcuts, "CreateSession", "a{sv}", ({"handle_token": ("s", token), "session_handle_token": ("s", "Macros")},))

            self._conn.send_and_get_reply(req)
            resp = self._conn.recv_until_filtered(responses)
            self._session_handle = resp.body[1]["session_handle"][1]

    def _generate_ydotool_socket(self) -> None:
        if is_flatpak():
            socket_dir = os.getenv("XDG_CACHE_HOME")
        else:
            socket_dir = tempfile.gettempdir()

        for i in os.listdir(socket_dir):
            if i.startswith("jdmacroplayer_ydotool_socket_"):
                os.remove(os.path.join(socket_dir, i))

        self._ydotool_socket = tempfile.mktemp(prefix="jdmacroplayer_ydotool_socket_", dir=socket_dir)
        os.environ["YDOTOOL_SOCKET"] = self._ydotool_socket

    def _flatpak_to_host_path(self, path: str, app_path: str, runtime_path: str) -> str:
        if path.startswith("/app"):
            return os.path.join(app_path, path.removeprefix("/app/"))
        elif path.startswith("/usr"):
            return os.path.join(runtime_path, path.removeprefix("/usr/"))
        else:
            return path

    def _get_ld_path(self, app_path: str, runtime_path: str) -> str:
        result = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.strip().startswith("ld-linux"):
                return self._flatpak_to_host_path(line.split(" => ")[1].strip(), app_path, runtime_path)

    def _get_all_lib_paths(self, app_path: str, runtime_path: str) -> list[str]:
        path_list: list[str] = []
        result = subprocess.run(["ldconfig", "-v"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if not line.startswith("\t"):
                path_list.append(self._flatpak_to_host_path(line.split(":")[0], app_path, runtime_path))
        return path_list

    def start_ydotoold(self) -> None:
        self._generate_ydotool_socket()

        if is_flatpak():
            config = configparser.ConfigParser()
            config.read("/.flatpak-info")
            app_path = config["Instance"]["app-path"]
            runtime_path = config["Instance"]["runtime-path"]
            lib_paths = self._get_all_lib_paths(app_path, runtime_path)
            ld_path = self._get_ld_path(app_path, runtime_path)
            ydotoold_path = os.path.join(app_path, "bin", "ydotoold")

            subprocess.Popen(["flatpak-spawn", "--host", "pkexec", "--disable-internal-agent", ld_path, "--library-path", ":".join(lib_paths), ydotoold_path, "-p", self._ydotool_socket, "-o", f"{os.getuid()}:{os.getuid()}"], cwd=os.path.expanduser("~"))
        else:
            subprocess.Popen(["pkexec", "--disable-internal-agent", "ydotoold", "-p", self._ydotool_socket, "-o", f"{os.getuid()}:{os.getuid()}"])

    def get_existing_shortcuts(self) -> list[str]:
        token = secrets.token_hex()
        sender_name = self._conn.unique_name[1:].replace('.', '_')
        handle = f"/org/freedesktop/portal/desktop/request/{sender_name}/{token}"

        response_rule = jeepney.bus_messages.MatchRule(
            type='signal', interface='org.freedesktop.portal.Request', path=handle
        )
        jeepney.io.blocking.Proxy(jeepney.bus_messages.message_bus, self._conn).AddMatch(response_rule)

        with self._conn.filter(response_rule) as responses:
            req = jeepney.new_method_call(self._global_shortcuts, "ListShortcuts", "oa{sv}", (self._session_handle, {"handle_token": ("s", token)}))
            self._conn.send_and_get_reply(req)
            resp = self._conn.recv_until_filtered(responses)

            shortcut_list: list[str] = []
            for i in resp.body[1]["shortcuts"][1]:
                shortcut_list.append(i[0])
            return shortcut_list

    def prepare_shortcuts(self) -> None:
        shortcut_list = self.get_existing_shortcuts()

        arg_list = []
        for macro in self._env.macro_manager.get_all_macros():
            if macro.id not in shortcut_list:
                arg_list.append((macro.id, {"description": ("s", macro.name)},))

        if len(arg_list) == 0:
            return

        args = (self._session_handle, arg_list, "", {})

        req = jeepney.new_method_call(self._global_shortcuts, "BindShortcuts", "oa(sa{sv})sa{sv}", args)
        self._conn.send_and_get_reply(req)

    def _execute_macro(self, macro: "Macro") -> None:
        for action in macro.actions:
            action_type = action.get_type_object()

            if action_type is None:
                continue

            action_type.execute_action(self._env, action.config)

    def _stop(self) -> None:
        os.remove(self._ydotool_socket)
        sys.exit(0)

    def _handle_interface(self, msg: jeepney.Message) -> None:
        match msg.header.fields[jeepney.HeaderFields.member]:
            case "ExecuteMacro":
                if len(msg.body) != 1:
                    self._conn.send_message(jeepney.new_error(msg, DBUS_DAEMON_SERVICE_NAME + ".Error.WrongArguments"))
                    return

                macro = self._env.macro_manager.get_macro_by_id(msg.body[0])
                if macro is None:
                    self._conn.send_message(jeepney.new_error(msg, DBUS_DAEMON_SERVICE_NAME + ".Error.MacroNotFound"))
                    return
                else:
                    self._conn.send_message(jeepney.new_method_return(msg, "", ()),)
                    self._execute_macro(macro)

            case "Reload":
                self._env.macro_manager.load_file()
                self.prepare_shortcuts()
                self._conn.send_message(jeepney.new_method_return(msg, "", ()),)

            case "Stop":
                self._conn.send_message(jeepney.new_method_return(msg, "", ()),)
                self._stop()

            case "Introspect":
                self._conn.send_message(jeepney.new_method_return(msg, "s", (self._introspect_data,)))

            case "Ping":
                self._conn.send_message(jeepney.new_method_return(msg, "", ()),)

            case "GetMachineId":
                machine_id = ""
                for current_file in ("/var/lib/dbus/machine-id", "/etc/machine-id"):
                    if os.path.isfile(current_file):
                        with open(current_file, "r", encoding="utf-8") as f:
                            machine_id = f.read().strip()
                            break
                self._conn.send_message(jeepney.new_method_return(msg, "s", (machine_id,)))

            case _:
                self._conn.send_message(jeepney.new_error(msg, DBUS_DAEMON_SERVICE_NAME + ".Error.InvalidMethod"))

    def _handle_signal(self, msg) -> None:
        signal_type = msg.header.fields[jeepney.HeaderFields.member]

        if signal_type not in ("Activated", "Deactivated"):
            return

        macro_id = msg.body[1]

        if signal_type == "Deactivated":
            try:
                del self._activated_macros[macro_id]
            except KeyError:
                pass
            return

        if macro_id in self._activated_macros:
            return

        macro = self._env.macro_manager.get_macro_by_id(macro_id)

        if macro is None:
            return

        self._activated_macros[macro_id] = True

        self._execute_macro(macro)

    def listen(self) -> None:
        while True:
            msg = self._conn.receive()
            match msg.header.message_type:
                case jeepney.MessageType.method_call:
                    if msg.header.fields[jeepney.HeaderFields.destination] == DBUS_DAEMON_SERVICE_NAME:
                        self._handle_interface(msg)
                case jeepney.MessageType.signal:
                    if msg.header.fields[jeepney.HeaderFields.interface] == "org.freedesktop.portal.GlobalShortcuts":
                        self._handle_signal(msg)
