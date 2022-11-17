#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import shutil
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_front_end.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



if __name__ == "__main__":
    # create appdata directories if necessary
    main()
    # from pathlib import Path
    # from platformdirs import PlatformDirs    
    # dirs = PlatformDirs(appname="yawning_titan", appauthor="DSTL")


    # print("Setup complete")

    # if Path(dirs.user_data_path).exists():      

    #     from flaskwebgui import FlaskUI
    #     from yt_front_end.wsgi import application as app    

    #     print(f"running app with {sys.executable}")
    #     FlaskUI(app=app, server="django").run()

    # else:
    #     print("Error please use the install.exe to create the yawning titan package folders")