from django.contrib import admin

# Register your models here.


from matches.models import (Job, Location, Employer, PositionMatch, Match,
                            EmployerMatch, LocationMatch)

admin.site.register(Job)
admin.site.register(Location)
admin.site.register(Employer)
admin.site.register(Match)
admin.site.register(EmployerMatch)
admin.site.register(LocationMatch)
admin.site.register(PositionMatch)
