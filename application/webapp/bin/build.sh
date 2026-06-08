#!/bin/bash
#
# Build the development stack, or the production stack
#

# Clean up local development files
rm yip/settings/local.py
rm db.sqlite3
sleep 2s

if [ "$ENV" == 'prod' ]
then
    echo "Building production"

    echo "Cleaning up non prod settings"
    rm webapp/yip/yip/settings/local.py
    rm webapp/yip/yip/settings/development.py
    sleep 5s

    # Make migrations
    python3 manage.py makemigrations
    python3 manage.py migrate

    # Static files are served locally by uWSGI from /opt/yip/static (see the static-map
    # in uwsgi.ini and the local STATICFILES_STORAGE override in settings), so no
    # collectstatic-to-S3 step is required. If you switch back to S3 static hosting,
    # re-add: python3 manage.py collectstatic --noinput

    # kick off UWSGI
    /usr/local/bin/uwsgi --ini /opt/yip/uwsgi.ini

elif [ "$ENV" == 'dev' ]
then
    echo "Building staging"

    # Make migrations
    python3 manage.py makemigrations
    python3 manage.py migrate
    sleep 2s

    # Kick off UWSGI
    /usr/local/bin/uwsgi --ini /opt/yip/uwsgi.ini

else
    echo "Invalid environment passed into build"
    exit 1
fi

