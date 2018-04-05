from django import forms

from account.models import UserProInfo, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("phone","email")

class UserProInfoForm(forms.ModelForm):
    Lab = (
        ('创新实验室', '创新实验室'),
    )
    lab = forms.CharField(widget=forms.Select(choices=Lab))
    Result_Type = (
        ('研究报告','研究报告'),
        ('实验报告', '实验报告'),
        ('论文', '论文'),
        ('成果实物', '成果实物'),
        ('信息系统', '信息系统'),
    )
    result_type = forms.CharField(widget=forms.Select(choices=Result_Type))
    class Meta:
        model = UserProInfo
        fields = ("tutor", "pro_name","lab","result_type","mem_num")
