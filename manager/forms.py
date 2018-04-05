from django import forms

from account.models import UserInfo, UserProInfo


class UserInfoForm(forms.ModelForm):
    user = forms.CharField(max_length=10)
    class Meta:
        model = UserInfo
        exclude = ("phone","email")

class UserProInfoForm(forms.ModelForm):
    Comment = (
        ('不合格','不合格'),
        ('合格', '合格'),
        ('优秀', '优秀'),
        ('一等奖', '一等奖'),
        ('二等奖', '二等奖'),
        ('三等奖', '三等奖'),
    )
    comment = forms.CharField(widget=forms.Select(choices=Comment))
    class Meta:
        model = UserProInfo
        fields = ("comment",)
