#!/bin/bash
# Create Superuser
ls -al ../../manage.py
../../manage.py makemigrations
../../manage.py migrate
../../manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'hpcdraja@hlrs.de', 'adminpass')"
