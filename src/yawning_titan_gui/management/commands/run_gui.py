import multiprocessing
import os
import subprocess
import logging
import sys
from multiprocessing import Process
from threading import Thread, Event
from typing import Union

from django.core.management.base import BaseCommand
from flaskwebgui import OPERATING_SYSTEM


class Command(BaseCommand):
    """
    Command to run the yawning titan gui in a window.

    :Examples:

    >>> yawning-titan gui
    """

    help = "Run yawning titan gui in window."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.app = None

    def __startup(self):
        """The function called when starting up the GUI"""
        # print the command used to run the gui
        logging.log(logging.INFO, "Command: ".join(self.app.browser_command))

    def __shutdown(self):
        """The function called when the GUI is closed"""
        logging.warning(f'Application has been shut down. {self.app.url} should no longer be up')

    def __get_server_process(self):
        """Creates the thread used for the server process"""
        # check if os is macOS
        if OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")
            server_process = Process(
                target=self.app.server, kwargs=self.app.server_kwargs or {}
            )
        else:
            server_process = Thread(target=self.app.server, kwargs=self.app.server_kwargs or {})

        # return the server process
        return server_process

    def __get_browser_process(self, server_process: Union[Thread, Process]):
        """Creates the thread used for the browser process"""
        process = None
        # check if windows
        if sys.platform == 'win32':
            process = subprocess.Popen(['start', self.app.url], shell=True)
        # check if macOS
        elif sys.platform == 'darwin':
            process = subprocess.Popen(['open', self.app.url])
        # catch all for other Operating Systems
        else:
            try:
                process = subprocess.Popen(['xdg-open', self.app.url])
            except OSError:
                logging.warning('Unable to determine Operating System')
                logging.warning('Please open a browser on: ' + self.app.url)

        return process

    def run(self):
        """
        Run the GUI backend server and then runs the GUI in the user's default browser
        """
        from flaskwebgui import FlaskUI

        from yawning_titan_server.wsgi import application

        self.app = FlaskUI(
            server="django",
            server_kwargs={
                "app": application,
                "port": 8000,
                "host": "localhost"
            },
            fullscreen=True
        )

        logging.log(logging.DEBUG, self.app)

        # run startup
        self.__startup()

        # setup server process
        server_process = self.__get_server_process()

        # setup browser thread
        browser_thread = Thread(target=self.__get_browser_process, args=(server_process,))

        # start threads
        server_process.start()

        # wait for server process to be online
        while not server_process.is_alive():
            os.wait()

        try:
            browser_thread.start()
            server_process.join()
            browser_thread.join()
        except KeyboardInterrupt:
            self.__keyboard_interrupt = True
            print("Stopped")

        # browser_thread.start()
        #
        # # join threads
        # server_process.join()
        # browser_thread.join()

        # browser_active = True
        #
        # logging.log(logging.DEBUG, "server process: " + server_process.name)
        # logging.log(logging.DEBUG, "browser process: " + browser_thread.name)
        #
        # while browser_active:
        #     # check if the browser thread is still alive
        #     browser_active = browser_thread.is_alive()
        #     logging.log(logging.DEBUG, f"browser_active: {browser_active}")
        #
        #     if not browser_thread.is_alive():
        #         # shutdown function
        #         self.__shutdown()
        #
        #         # kill the server thread
        #         server_process.kill()

    def handle(self, *args, **kwargs):
        """Method that is fired on execution of the command in the terminal."""
        self.run()
