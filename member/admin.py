from django.contrib import admin
from .models import *

admin.site.register(Member)
admin.site.register(FeeType)
admin.site.register(Payment)
admin.site.register(Day)
admin.site.register(Timetable)
admin.site.register(Department)
admin.site.register(Sub_Department)
admin.site.register(DepartmentMeeting)