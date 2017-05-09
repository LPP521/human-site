from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete = models.CASCADE)
    birth = models.DateField('出生日期', blank=True, null=True)
    # TODO Add read_name
    dep = models.ForeignKey('Department', on_delete = models.CASCADE, blank=True, null=True)
    arms = models.CharField('序列', max_length = 50, blank=True, null=True)
    level = models.IntegerField('等级', default = 1)
    vacation = models.IntegerField('年假', default = 10) 
    def __str__(self):
        return self.user.username
    def name(self):
        return self.user.first_name + self.user.last_name

    name.short_description = '姓名'

    class Meta:
        verbose_name = '员工信息'
        verbose_name_plural = '员工信息'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userinfo.save()

class Department(models.Model):
    name = models.CharField('名称', max_length = 50)
    master = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE, 
        limit_choices_to={'arms': 'M'}, 
        null = True
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门' 
 
class Salary(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField('发放日期', blank=True, null=True)
    salary = models.FloatField('总薪资', default = 0)
    def pension(self):
        return round(self.salary * 0.08, 2) 
    def medical(self):
        return round(self.salary * 0.02, 2)
    def unemployment(self):
        return round(self.salary * 0.005, 2)
    def housing(self):
        return round(self.salary * 0.07, 2)
    def tax(self):
        if self.salary >= 5000:
            return (self.salary - 5000) * 0.08
        else:
            return 0

    pension.short_description = '养老保险'
    medical.short_description = '医疗保险'
    unemployment.short_description = '失业保险'
    housing.short_description = '公积金'
    tax.short_description = '税'

    class Meta:
        verbose_name = '员工薪资'
        verbose_name_plural = '员工薪资' 

INDIVIDUAL = 1 # 个人财产
ORGANIZED = 2  # 组织财产
class Asset(models.Model):
    name = models.CharField('名称', max_length = 50)
    mark = models.CharField('产品标识', max_length = 40)
    sort = models.IntegerField('类型', default = INDIVIDUAL)
    purchase = models.DateField('购入日期', auto_now_add = True)
    def __str__(self):
        return self.mark

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = '资产'
    

class UserAsset(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    asset = models.ForeignKey(
        Asset,
        limit_choices_to={'sort': INDIVIDUAL},
        on_delete = models.CASCADE
    )
    borrow = models.DateField('发放日期', default = datetime.date.today, blank=True, null=True)
    back = models.DateField('归还日期', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '员工资产'
        verbose_name_plural = '员工资产'

class DepAsset(models.Model):
    dep = models.ForeignKey(Department, on_delete = models.CASCADE)
    asset = models.ForeignKey(
        Asset,
        limit_choices_to={'sort': ORGANIZED},
        on_delete = models.CASCADE
    )

    class Meta:
        verbose_name = '部门资产'
        verbose_name_plural = '部门资产'

ATTEND = 1   # 出席
ABSENCE = 2  # 缺席
LEAVE = 3    # 请假
VACATION = 4 # 年假
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField('日期', default=datetime.datetime.now())
    status = models.IntegerField('状态', default = ATTEND)

    class Meta:
        verbose_name = '员工考勤'
        verbose_name_plural = '员工考勤'
