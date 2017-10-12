"""backup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from viewReport import sqlReport,sqlReportActive
from viewAuditList import sqlAuditList,sqlAuditPost,auditDetail,auditExecute,auditPreExecute
from viewAuditHistoryList import auditHistoryList,auditHistoryListDate
from viewAuditModify import sqlUpdate,sqlUpdateActive
from view.viewReviewHome import reviewUserLoginVerification,loginHome,reviewUserLogin,reviewUserLogout,index_char_pie,index_char_pie_ddl,index_char_line
from view.viewReviewReport import reportUpdate,reportUpdatePost
from view.viewReview import reviewReportListAll,reviewListAllHistory,reviewExecute,reviewPreExecute,reviewPost,reviewDetail,reviewPostHistory,reviewBak
from view.test import test
from view.viewTempReview import reviewTempActive,reviewTemp
from view.viewRollBack import reviewRollBack
from django.views import static
from view.reviewExmp import reviewUseExamp
from view.viewUserProfileUpdate import userPofileUpdate,userPofile
import settings

urlpatterns = [
url(r'^admin/', admin.site.urls),
url(r'^review/v1.0/review/useExamp/',reviewUseExamp,name='reviewUseExamp'),
# url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
url(r'^user/profile/update/', userPofileUpdate,name='userPofileUpdate'),
url(r'^user/profile/', userPofile,name='userPofile'),
url(r'^test/', test,name='test'),
url(r'^review/v1.0/rollback/', reviewRollBack,name='reviewRollBack'),
url(r'^review/v1.0/review/temp/', reviewTempActive,name='reviewTempActive'),
url(r'^review/v1.0/review/home/', reviewTemp,name='reviewTemp'),
url(r'^review/v1.0/review/char1/', index_char_line,name='index_char_line'),
url(r'^review/v1.0/review/char2/', index_char_pie,name='index_char_pie'),
url(r'^review/v1.0/review/char3/', index_char_pie_ddl,name='index_char_pie_ddl'),
url(r'^review/v1.0/review/detail/', reviewDetail,name='reviewDetail'),
url(r'^review/v1.0/review/execute/', reviewExecute,name='reviewExecute'),
url(r'^review/v1.0/review/preexecute/', reviewPreExecute,name='reviewPreExecute'),
url(r'^review/v1.0/review/all/', reviewReportListAll,name='reviewReportListAll'),

url(r'^review/v1.0/review/bak/', reviewBak,name='reviewBak'),
url(r'^review/v1.0/review/post/', reviewPost,name='reviewPost'),
url(r'^review/v1.0/review/history/post/', reviewPostHistory,name='reviewPostHistory'),
url(r'^review/v1.0/review/history/', reviewListAllHistory,name='reviewListAllHistory'),

url(r'^review/v1.0/report/update/',sqlUpdate,name='sqlUpdate'),
url(r'^review/v1.0/report/post/',sqlUpdateActive,name='sqlUpdateActive'),

url(r'^review/v1.0/audit/history/data/', auditHistoryListDate,name='auditHistoryListDate'),
url(r'^review/v1.0/audit/history/', auditHistoryList,name='auditHistoryList'),

url(r'^review/v1.0/audit/execute/', auditExecute,name='auditExecute'),
url(r'^review/v1.0/audit/PreExecute/', auditPreExecute,name='auditPreExecute'),
url(r'^review/v1.0/audit/detail/', auditDetail,name='auditDetail'),
url(r'^review/v1.0/report/list/', sqlAuditList,name='sqlAuditList'),
url(r'^review/v1.0/report/post', sqlAuditPost,name='sqlAuditPost'),

url(r'^review/v1.0/report/active/', sqlReportActive,name='sqlReportActive'),
url(r'^review/v1.0/report/', sqlReport,name='sqlReport'),
url(r'^user/v1.0/account/verification/', reviewUserLoginVerification,name='loginVerification'),
url(r'^user/v1.0/account/login/', reviewUserLogin,name='userLogin'),
url(r'^user/v1.0/account/logout/', reviewUserLogout,name='userLogout'),
url(r'^$', loginHome,name='home'),
]
