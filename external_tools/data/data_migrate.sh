#!/bin/bash
./manage.py makemigrations
./manage.py migrate

#admin_user=$1
#admin_password=$2
#sudo ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$admin_user', 'hpcdraja@hlrs.de', '$admin_password')"
