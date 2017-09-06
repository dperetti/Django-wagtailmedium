#!/bin/bash

#Exit immediately if a command exits with a non-zero status.
set -e

# no database yet ? let's run the migrations and fixtures #vkJmM#
if [ ! -f /db/db.sqlite3 ]; then
  python manage.py migrate
  python manage.py shell -c "exec(open('fixture.py').read())"
fi
exec "$@"
