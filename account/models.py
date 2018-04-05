from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User,unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    classID = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    institute = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.CharField(max_length=255, blank=True, null=True, default='')
    status = models.CharField(max_length=255, blank=True, null=True, default='') #记录该用户是否过期，1为有效，2为无效

    def __str__(self):
        return "user:{}".format(self.user.username)

    class Meta:
        permissions = (
            ('add_userproinfo', u"添加用户"),  # 权限字段名称及其解释
            ('delete_userproinfo', u"删除用户"),
            ('change_userproinfo', u"修改用户信息"),
        )

#项目信息
class UserProInfo(models.Model):
    # user = models.OneToOneField(User, unique=True)
    user = models.ForeignKey(User)
    pro_name = models.CharField(max_length=255, blank=True, null=True, default='')
    tutor = models.CharField(max_length=255, blank=True, null=True, default='')
    result_type = models.CharField(max_length=255, blank=True, null=True, default='')
    lab = models.CharField(max_length=255, blank=True, null=True, default='')
    mem_num = models.CharField(max_length=255, blank=True, null=True, default='')

    apply_year = models.CharField(max_length=255, blank=True, null=True, default='') #该项目申请年份
    apply_status = models.CharField(max_length=255, blank=True, null=True, default='') #申请报告提交情况
    middle_status = models.CharField(max_length=255, blank=True, null=True, default='') #中期报告提交情况
    conclude_status = models.CharField(max_length=255, blank=True, null=True, default='') #结题报告提交情况
    file_status = models.CharField(max_length=255, blank=True, null=True, default='') #其他文件提交情况
    comment = models.CharField(max_length=255, blank=True, null=True, default='')  # 项目评价


    def __str__(self):
        return "user:{}".format(self.user.username)