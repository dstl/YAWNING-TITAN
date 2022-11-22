import shutil
from django.core.management.base import BaseCommand

from setup import _create_app_dirs
class Command(BaseCommand):
    help = 'sets up yawning titan dependencies'

    def handle(self, *args, **kwargs):
        print("Running setup...")
        from yawning_titan import DATA_DIR
        from yawning_titan_gui import _YT_GUI_ROOT_DIR        
    

        _create_app_dirs()
        #_copy_package_data_notebooks_to_notebooks_dir()
        
        # Creates the static ui files copy in the data directory
        # shutil.copytree(
        #     (_YT_GUI_ROOT_DIR / "static").as_posix(), 
        #     DATA_DIR.as_posix(), 
        #     dirs_exist_ok=True
        # )