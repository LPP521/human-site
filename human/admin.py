from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ['dep']
    list_display = ('user', 'name', 'birth', 'dep', 'arms', 'level', 'vacation')

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'salary', 'pension', 'medical', 'unemployment', 'housing', 'tax', 'date')
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'master')
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'mark','sort', 'purchase')
class UserAssetAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'borrow', 'back')
    
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(UserAsset, UserAssetAdmin)
admin.site.register(DepAsset)
admin.site.register(Attendance)

