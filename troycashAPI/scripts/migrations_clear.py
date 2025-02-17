import os
import shutil

from troycashAPI import settings

def run():
    """
    Stand alone script clear old migration files.
    """
    # remove all the application's migration directories.
    for app in settings.OWN_APPS:
        app_migration_dir = os.path.join(settings.BASE_DIR, app, "migrations")
        print("removing migration dir:", app_migration_dir)
        shutil.rmtree(app_migration_dir, ignore_errors=True)
