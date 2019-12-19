from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from ClientDashboard.views import PortfolioView, Dashboard, AppointmentScheduler, Overview, welcome
from ClientDashboard import views

urlpatterns = [

    url(r'^portfolio/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^portfolio/(?P<user_id>\d+)/$', PortfolioView.as_view(), name=u'profile'),
    url(r'^$', Dashboard.as_view(), name=u'dashboard'),
    url(r'^appointment_scheduler/$', AppointmentScheduler.as_view(), name=u'appointment_scheduler'),
    url(r'^client_register$', views.client_register, name=u'client_register'),
    url(r'^logout', views.logout, name=u'logout'),
    url(r'^welcome', views.welcome, name=u'welcome'),
    url(r'^confirmation/(?P<confirmation_code>\w+)/(?P<username>\w+)$', views.confirmation),
    url(r'^client_login$', views.client_login, name=u'client_login'),
    url(r'^auth$', views.auth_view, name=u'authenticate'),
    url(r'^overview/$', views.Overview, name=u'overview'),
    url(r'^design_upload/$', views.design_upload, name=u'design_upload'),
    url(r'^project_upload/$', views.project_upload, name=u'project_upload'),
    url('load_sub_category$', views.load_sub_category, name='load_sub_category'),
    url('upload_details$', views.upload_details, name='upload_details'),
    url(r'^delete_design$', views.delete_design, name='delete_design'),
    url('load_upload_form', views.load_upload_form, name='load_upload_form'),
    url('send_sms', views.send_sms_user, name='send_sms'),
]
