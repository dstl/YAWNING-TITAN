import multiprocessing
import subprocess
import logging
import sys
import threading

from django.core.management.base import BaseCommand
from yawning_titan_server.wsgi import application

import os
import time
import signal
import psutil
import tempfile
import platform
import subprocess
import socketserver
import multiprocessing
from multiprocessing import Process
from threading import Thread
from dataclasses import dataclass
from typing import Callable, Any, Union

OPERATING_SYSTEM = platform.system().lower()
PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"


def get_free_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    return free_port

class DefaultServerDjango:
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {"app": kwargs["app"], "port": kwargs["port"]}

    @staticmethod
    def server(**server_kwargs):
        import waitress

        waitress.serve(**server_kwargs)


@dataclass
class YawningTitanServer:
    server: Union[str, Callable[[Any], None]]
    server_kwargs: dict = None
    app: Any = None
    port: int = None
    width: int = None
    height: int = None
    fullscreen: bool = True
    on_startup: Callable = None
    on_shutdown: Callable = None
    socketio: Any = None

    def __post_init__(self):
        self.__keyboard_interrupt = False

        if self.port is None:
            self.port = (
                self.server_kwargs.get("port")
                if self.server_kwargs
                else get_free_port()
            )

        if isinstance(self.server, str):
            default_server = DefaultServerDjango
            self.server = default_server.server
            self.server_kwargs = self.server_kwargs or default_server.get_server_kwargs(
                app=self.app, port=self.port, flask_socketio=self.socketio
            )

        self.profile_dir = os.path.join(tempfile.gettempdir(), "flaskwebgui")
        self.url = f"http://127.0.0.1:{self.port}"

    def _get_browser_process(self):
        """Creates the thread used for the browser process"""
        process = None
        # check if windows
        if sys.platform == 'win32':
            process = subprocess.Popen(['start', self.url], shell=True)
        # check if macOS
        elif sys.platform == 'darwin':
            process = subprocess.Popen(['open', self.url])
        # catch all for other Operating Systems
        else:
            try:
                process = subprocess.Popen(['xdg-open', self.url])
            except OSError:
                logging.warning('Unable to determine Operating System')
                logging.warning('Please open a browser on: ' + self.url)

        return process


    def run(self):
        end_server_event = threading.Event()

        if self.on_startup is not None:
            self.on_startup()

        if OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")
            server_process = Process(
                target=self.server, kwargs=self.server_kwargs or {}
            )
        else:
            server_process = Thread(target=self.server, kwargs=self.server_kwargs or {})

        browser_thread = Thread(target=self._get_browser_process)

        try:
            # start server
            server_process.start()
            # start browser
            browser_thread.start()

            server_process.join()
            browser_thread.join()

        except KeyboardInterrupt:
            self.__keyboard_interrupt = True
            print("Stopped")

        return server_process, browser_thread


class Command(BaseCommand):
    """
    Command to run the yawning titan gui in a window.

    :Examples:

    >>> yawning-titan gui
    """

    help = "Run yawning titan gui in window."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def run(self):
        """
        Run the GUI backend server and then runs the GUI in the user's default browser
        """
        YawningTitanServer(  # noqa
            server="django",
            server_kwargs={
                "app": application,
                "port": 8000,
                "host": "localhost"
            },
            fullscreen=True
        ).run()

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        self.run()
