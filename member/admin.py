from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class MemberPaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name','simu','jinsia','dhehebu','huduma_aliyonayo']
    
    list_filter = ['name','dhehebu', 'jinsia']
    search_fields = ['name', 'dhehebu', 'jinsia']

@admin.register(Offering)
class OfferingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['member', 'name','description','amount']
    
    list_filter = ['member','name', 'paid_all']
    search_fields = ['member__name', 'name']
    inlines = (MemberPaymentInline,)

@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['offering','payment','created_at']
    
    
    search_fields = ['offering__name']


@admin.register(Zaka)
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['member','payment','created_at']
    
    list_filter = ['member',]
    search_fields = ['member__name',]


admin.site.register(Day)
admin.site.register(Timetable)
admin.site.register(Department)
admin.site.register(Sub_Department)
admin.site.register(DepartmentMeeting)