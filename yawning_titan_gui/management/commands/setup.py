import shutil
from django.core.management.base import BaseCommand

import sys
#from setup import _create_app_dirs
class Command(BaseCommand):
    help = 'sets up yawning titan dependencies'

    def handle(self, *args, **kwargs):
        print("Running setup...")
        from yawning_titan import DATA_DIR
        from yawning_titan_gui import _YT_GUI_ROOT_DIR        

        #import setup
        # print(sys.path, setup._create_app_dirs)
        #_create_app_dirs()
        #_copy_package_data_notebooks_to_notebooks_dir()
        print(_YT_GUI_ROOT_DIR / "static",DATA_DIR)
        # Creates the static ui files copy in the data directory
        shutil.copytree(
            (_YT_GUI_ROOT_DIR / "static").as_posix(), 
            DATA_DIR.as_posix(), 
            dirs_exist_ok=True
        )

        print(list(DATA_DIR.iterdir()))
