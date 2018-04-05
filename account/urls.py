from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.account_home, name="account_home"),
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^logout/$', auth_views.logout, {"template_name": "account/logout.html"}, name="user_logout"),
    url(r'^password-change/$', auth_views.password_change,
        {"post_change_redirect": "/account/password-change-done", "template_name": "account/password_change.html"},
        name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done,
        {"template_name": "account/password_change_done.html"}, name='password_change_done'),
    url(r'^my-information/$', views.user_info, name="my_information"),
    url(r'^edit-my-information/$', views.user_info_edit, name="edit_my_information"),
    url(r'^my-pro-information/$', views.user_pro_info, name="my_pro_information"),
    url(r'^edit-my-pro-information/$', views.user_pro_info_edit, name="edit_my_pro_information"),
    url(r'^upload-apply/$', views.upload_apply, name="upload_apply"),
    url(r'^upload-middle/$', views.upload_middle, name="upload_middle"),
    url(r'^upload-conclude/$', views.upload_conclude_file, name="upload_conclude"),
    # url(r'^upload-conclude-file/$', views.upload_conclude_file, name="upload_conclude_file"),
    url(r'^index/$', views.account_index, name="account_index"),
    url(r'^index/password-change/$', auth_views.password_change,
        {"post_change_redirect": "/account/index/password-change-done",
         "template_name": "account/index_password_change.html"},
        name='index_password_change'),
    url(r'^index/password-change-done/$', auth_views.password_change_done,
        {"template_name": "account/index_password_change_done.html"}, name='index_password_change_done'),
    url(r'^index/edit-my-pro-information/$', views.index_user_pro_info_edit, name="index_edit_my_pro_information"),
    url(r'^index/my-information/$', views.index_user_info, name="index_my_information"),
    url(r'^index/edit-my-information/$', views.index_user_info_edit, name="index_edit_my_information"),
    url(r'^get_status/$', views.get_status, name="get_status")
]
