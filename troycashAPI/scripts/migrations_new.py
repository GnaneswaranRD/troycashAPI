import os
import subprocess

from django.core.management import call_command

from troycashAPI import settings


def run():
    """
    Stand alone script to create migration files for all apps and apply them.

    Developer: Pall Pandiyan.S
    """
    call_command("makemigrations", "--no-input")
    for app in settings.OWN_APPS:
        migration_dir_path = os.path.join(settings.BASE_DIR, app, "migrations")
        subprocess.run(["mkdir", "-p", migration_dir_path])
        subprocess.run(["touch", os.path.join(migration_dir_path, "__init__.py")])
        call_command("makemigrations", app, "--no-input")

    call_command("migrate", "--no-input")
