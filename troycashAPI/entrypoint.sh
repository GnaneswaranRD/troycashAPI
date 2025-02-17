#!/bin/bash

if [[ "$ENABLE_PIP_INSTALL_ON_STARTUP" == "1" ]]; then
    # updating the python package manager first
    # echo "==> Upgrading pip and setuptools!"
    # pip install --no-cache-dir -U pip setuptools
    
    # install any missing python packages
    echo
    echo
    echo "===> Installing pip packages!"
    pip install --no-cache-dir -e .
    # pip install --no-cache-dir apache-airflow==2.10.4 psycopg2-binary -r requirements.txt
fi

# if encountered any migration issue we can manually wipe out the old migrations.
if [[ "$ENABLE_FRESH_MIGRATIONS_ON_STARTUP" == "1" ]]; then
    echo
    echo
    echo "===> Clearing old migraion files"
    # find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    # find . -name "*.pyc" -delete
    python manage.py runscript migrations_clear
fi


# just to be sure run migration for all databases configured
if [[ "$ENABLE_DB_MIGRATION_ON_STARTUP" == "1" ]]; then
    echo
    echo
    echo "===> Running database migrations"
    # python manage.py makemigrations --no-input --merge --update
    # python manage.py migrate --no-input
    python manage.py runscript migrations_new
fi


# restoring db dump if needed
if [[ "$ENABLE_DATA_LOAD_ON_STARTUP" == "1" ]]; then
    echo
    echo
    echo "===> Loading db dump"
    ./load_db_data.sh
fi


# collect the static files into BASE_DIR / static
if [[ "$ENABLE_STATIC_COLLECTION_ON_STARTUP" == "1" ]]; then
    echo
    echo
    echo "===> Collecting static files"
    python manage.py collectstatic --noinput
fi


if [[ "$ENABLE_DIRECTORY_CHECK_ON_STARTUP" == "1" ]]; then
    # Make sure eso_v3/logs dir exists!
    echo
    echo
    echo "===> Make sure eso_v3/logs dir exists!"
    mkdir media
fi

# running the development server on 0:8000
echo
echo
echo "===> Running the developement server"
python manage.py runserver 0.0.0.0:8000
