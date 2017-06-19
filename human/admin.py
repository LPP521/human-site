from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ['dep']
    list_display = ('id', 'user', 'name', 'birth', 'dep', 'arms', 'level', 'vacation')

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'salary', 'pension', 'medical', 'unemployment', 'housing', 'tax', 'date')
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'master')
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'mark','sort', 'purchase')
class UserAssetAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'borrow', 'back', 'status')
class AttendanceAdmin(admin.ModelAdmin):
    list_filter = ['date','status']
    search_fields = ['user__username']
    list_display = ('user', 'date', 'status')
class MessageAdmin(admin.ModelAdmin):
    search_fields = ['sender__username']
    list_filter = ['time', 'message_type']
    list_display = ('sender', 'to', 'message_type', 'content', 'time', 'status', 'result')

    
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(UserAsset, UserAssetAdmin)
admin.site.register(DepAsset)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Message, MessageAdmin)

