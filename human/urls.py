from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views
# 处理路由分配
# This is namespace
app_name = 'human'

urlpatterns = [
   url(r'^auth$', obtain_jwt_token),
   url(r'^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view()),
   url(r'^salarys/(?P<pk>[0-9]+)$', views.SalaryList.as_view()),
   url(r'^assets/(?P<pk>[0-9]+)$', views.AssetList.as_view()),
   url(r'^assets/return/(?P<pk>[0-9]+)$', views.AssetOptions.as_view()),
   url(r'^attendances/(?P<pk>[0-9]+)$', views.AttendanceDetail.as_view()),
   url(r'^attendances$', views.AttendanceList.as_view()),
   url(r'^vacation$', views.VacationDetail.as_view()),
   url(r'message/send$', views.MessageDetail.as_view()),
   url(r'message/(?P<pk>[0-9]+)$', views.MessageList.as_view()),
   url(r'message/read/(?P<pk>[0-9]+)$', views.MessageOptions.as_view())
]