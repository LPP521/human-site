from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
# Create your models here.

class UserInfo(models.Model):
    ARMS_TYPE = (
        ('M', '管理人员'),
        ('T', '技术人员')
    )

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    birth = models.DateField('出生日期', blank=True, null=True)
    # TODO Add read_name
    dep = models.ForeignKey('Department', on_delete=models.CASCADE, blank=True, null=True, verbose_name="所属部门")
    arms = models.CharField('序列', max_length=50, blank=True, null=True, choices=ARMS_TYPE)
    level = models.IntegerField('等级', default=1)
    vacation = models.IntegerField('年假', default=10) 
    def __str__(self):
        return self.user.username
    def name(self):
        return self.user.first_name + self.user.last_name
    def id(self):
        return self.user.id

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
    name = models.CharField('名称', max_length=50)
    master = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE, 
        limit_choices_to={'arms': 'M'}, 
        blank=True, 
        null=True,
        verbose_name="部门主管"
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门' 
 
class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('发放日期', blank=True, null=True)
    salary = models.FloatField('总薪资', default=0)
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
    SORT_TYPE = (
        (1, '个人财产'),
        (2, '组织财产')
    )

    name = models.CharField('名称', max_length=50)
    mark = models.CharField('产品标识', max_length=40)
    sort = models.IntegerField('类型', default=1, choices=SORT_TYPE)
    purchase = models.DateField('购入日期', auto_now_add=True)
    def __str__(self):
        return self.mark

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = '资产'
    

class UserAsset(models.Model):
    APPLY_TYPE = (
        (1, '已借'),
        (2, '已还'),
        (3, '处理中')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(
        Asset,
        limit_choices_to={'sort': INDIVIDUAL},
        on_delete = models.CASCADE
    )
    borrow = models.DateField('发放日期', default=datetime.date.today, blank=True, null=True)
    back = models.DateField('归还日期', blank=True, null=True)
    status = models.IntegerField('申请状态', default=1, choices=APPLY_TYPE)

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
    STATUS_TYPE = (
        (1, '出席'),
        (2, '缺席'),
        (3, '请假'),
        (4, '年假')
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField('日期', default = datetime.datetime.now())
    status = models.IntegerField('状态', default = ATTEND, choices=STATUS_TYPE)

    class Meta:
        verbose_name = '员工考勤'
        verbose_name_plural = '员工考勤'

class Message(models.Model):
    MESSAGE_TYPE = (
        ('leave', '请假'),
        ('return', '物品归还'),
        ('read', '只读消息')
    )

    sender = models.ForeignKey(User, related_name = "sender",on_delete = models.CASCADE, verbose_name = "发件人")
    to = models.ForeignKey(User, related_name = "to",on_delete = models.CASCADE, verbose_name = "收件人")
    message_type = models.CharField('消息类型', choices = MESSAGE_TYPE, max_length = 15)
    content = models.TextField('消息内容')
    key = models.IntegerField('关键信息', blank=True, null=True)
    time = models.DateTimeField('发送时间', default = datetime.datetime.now(), blank=True, null=True)
    status = models.BooleanField('已读？',default = False)
    result = models.BooleanField('已处理？', default = False)

    class Meta:
        verbose_name = '消息管理'
        verbose_name_plural = '消息管理'
