from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QLabel, QMessageBox
from ..Constants import DBUS_DAEMON_SERVICE_NAME, DBUS_DAEMON_INTERFACE_NAME
from PyQt6.QtDBus import QDBusConnection, QDBusMessage, QDBusArgument
from PyQt6.QtCore import QCoreApplication, QMetaType, pyqtSlot
from .AddEditMacroDialog import AddEditMacroDialog
from ..ui_compiled.MainWindow import Ui_MainWindow
from .SettingsDialog import SettingsDialog
from .WelcomeDialog import WelcomeDialog
from .AboutDialog import AboutDialog
from typing import TYPE_CHECKING
import subprocess
import webbrowser
import shutil
import sys
import os


if TYPE_CHECKING:
    from ..Environment import Environment


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self.setupUi(self)

        self._env = env

        self._dbus_connection = QDBusConnection.sessionBus()

        self._daemon_running_label = QLabel()
        self.statusBar().addPermanentWidget(self._daemon_running_label)

        if shutil.which("jdmacroplayer-daemon") is None:
            self.autostart_daemon_action.setVisible(False)

        self._update_macro_list()
        self._update_daemon_running()

        self._dbus_connection.connect("org.freedesktop.DBus", "/org/freedesktop/DBus", "org.freedesktop.DBus", "NameOwnerChanged", self._dbus_name_owner_changed)

        self.exit_action.triggered.connect(lambda: sys.exit(0))

        self.start_daemon_action.triggered.connect(self._start_daemon)
        self.stop_daemon_action.triggered.connect(self._stop_daemon)
        self.autostart_daemon_action.triggered.connect(self._autostart_daemon_action_clicked)

        self.settings_action.triggered.connect(self._settings_action_clicked)

        self.welcome_dialog_action.triggered.connect(self.open_welcome_dialog)
        self.view_source_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdMacroPlayer"))
        self.report_bug_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdMacroPlayer/issues"))
        self.translate_action.triggered.connect(lambda: webbrowser.open("https://translate.codeberg.org/projects/jdMacroPlayer"))
        self.donate_action.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/jakobdev"))
        self.about_action.triggered.connect(lambda: AboutDialog(self, self._env).exec())
        self.about_qt_action.triggered.connect(env.app.aboutQt)

        self.macro_list.currentItemChanged.connect(self._update_macro_buttons_enabled)

        self.add_macro_button.clicked.connect(self._add_macro_button_clicked)
        self.edit_macro_button.clicked.connect(self._edit_macro_button_clicked)
        self.delete_macro_button.clicked.connect(self._delete_macro_button_clicked)
        self.execute_macro_button.clicked.connect(self._execute_macro_button_clicked)

    def _update_daemon_running(self) -> None:
        msg = QDBusMessage.createMethodCall("org.freedesktop.DBus", "/org/freedesktop/DBus", "org.freedesktop.DBus", "ListNames")
        response = self._dbus_connection.call(msg)

        if response.errorMessage() != "":
            print(response.errorMessage(), file=sys.stderr)
            return

        self._is_daemon_running = DBUS_DAEMON_SERVICE_NAME in response.arguments()[0]

        if self._is_daemon_running:
            self.start_daemon_action.setEnabled(False)
            self.stop_daemon_action.setEnabled(True)
            self._daemon_running_label.setText(QCoreApplication.translate("MainWindow", "The daemon is running"))
        else:
            self.start_daemon_action.setEnabled(True)
            self.stop_daemon_action.setEnabled(False)
            self._daemon_running_label.setText(QCoreApplication.translate("MainWindow", "The daemon is not running"))

    @pyqtSlot(QDBusMessage)
    def _dbus_name_owner_changed(self, msg: QDBusMessage) -> None:
        if msg.arguments()[0] == DBUS_DAEMON_SERVICE_NAME:
            self._update_daemon_running()

    def _start_daemon(self) -> None:
        subprocess.Popen([sys.executable, "-m", "jdMacroPlayer.daemon"], cwd=os.path.dirname(self._env.program_dir))

    def _stop_daemon(self) -> None:
        msg = QDBusMessage.createMethodCall(DBUS_DAEMON_SERVICE_NAME, "/", DBUS_DAEMON_INTERFACE_NAME, "Stop")
        self._dbus_connection.call(msg)

    def _reload_daemon(self) -> None:
        msg = QDBusMessage.createMethodCall(DBUS_DAEMON_SERVICE_NAME, "/", DBUS_DAEMON_INTERFACE_NAME, "Reload")
        self._dbus_connection.call(msg)

    def _autostart_daemon_action_clicked(self) -> None:
        arr = QDBusArgument()
        arr.beginArray(QMetaType.Type.QString.value)
        arr.add("jdmacroplayer-daemon", QMetaType.Type.QString.value)
        arr.endArray()

        msg = QDBusMessage.createMethodCall("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Background", "RequestBackground")
        msg.setArguments([
            "",
            {
                "reason": QCoreApplication.translate("MainWindow", "Add Daemon to Autostart"),
                "autostart": True,
                "commandline": arr,
            }
        ])
        self._dbus_connection.call(msg)

        QMessageBox.information(
            self,
            QCoreApplication.translate("MainWindow", "Added to Autostart"),
            QCoreApplication.translate("MainWindow", "The daemon was added to the Autostart"),
         )

    def _update_macro_buttons_enabled(self) -> None:
        enabled = self.macro_list.currentItem() is not None
        self.edit_macro_button.setEnabled(enabled)
        self.delete_macro_button.setEnabled(enabled)
        self.execute_macro_button.setEnabled(enabled)

    def _add_macro_button_clicked(self) -> None:
        dialog = AddEditMacroDialog(self, self._env, self._env.macro_manager.create_new_macro())
        dialog.open_dialog()
        self._update_macro_list()

        if self._is_daemon_running:
            self._reload_daemon()

    def _edit_macro_button_clicked(self) -> None:
        macro = self._env.macro_manager.get_macro_by_id(self.macro_list.currentItem().data(42))
        dialog = AddEditMacroDialog(self, self._env, macro)
        dialog.open_dialog()
        self._update_macro_list()

        if self._is_daemon_running:
            self._reload_daemon()

    def _delete_macro_button_clicked(self) -> None:
        self._env.macro_manager.delete_macro_by_id(self.macro_list.currentItem().data(42))
        self._update_macro_list()

        if self._is_daemon_running:
            self._reload_daemon()

    def _execute_macro_button_clicked(self) -> None:
        if not self._is_daemon_running:
            QMessageBox.critical(
                self,
                QCoreApplication.translate("MainWindow", "Daemon not running"),
                QCoreApplication.translate("MainWindow", "The daemon needs to be running to execute a Macro"),
            )
            return

        msg = QDBusMessage.createMethodCall(DBUS_DAEMON_SERVICE_NAME, "/", DBUS_DAEMON_INTERFACE_NAME, "ExecuteMacro")
        msg.setArguments([self.macro_list.currentItem().data(42)])
        self._dbus_connection.call(msg)

    def _update_macro_list(self) -> None:
        self.macro_list.clear()
        for macro in self._env.macro_manager.get_all_macros():
            item = QListWidgetItem(macro.name)
            item.setData(42, macro.id)
            self.macro_list.addItem(item)
        self._update_macro_buttons_enabled()

    def _settings_action_clicked(self) -> None:
        dialog = SettingsDialog(self, self._env)
        dialog.exec()

    def open_welcome_dialog(self) -> None:
        dialog = WelcomeDialog(self, self._env)
        dialog.exec()
