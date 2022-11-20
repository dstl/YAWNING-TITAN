import sys
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'sets up yawning titan dependencies'

    def handle(self, *args, **kwargs):
        from flaskwebgui import FlaskUI
        from yawning_titan_server.wsgi import application as app    

        print(f"running app with {sys.executable}")
        FlaskUI(app=app, server="django").run()