import sys
from django.core.management.base import BaseCommand
from yawning_titan import DATA_DIR

class Command(BaseCommand):
    help = 'sets up yawning titan dependencies'

    def handle(self, *args, **kwargs):
        if DATA_DIR.exists():
            from flaskwebgui import FlaskUI
            from yawning_titan_gui.wsgi import application as app    

            print(f"running app with {sys.executable}")
            FlaskUI(app=app, server="django").run()
        else:
            print("Error please use the 'setup command' to create the yawning titan package folders")