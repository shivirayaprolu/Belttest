from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.log_register, name="register"),
    url(r'^login$', views.log_register, name="login"),
    url(r'^travels$', views.travels, name="travels"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^travels/add/$', views.addtrip, name="addtrip"),
    url(r'^createtrip$', views.createtrip, name="createtrip"),
    #url(r'^travels/add/$', views.addtrip, name="addtrip"),
#    url(r'^otherusertrip$', views.otherusertrip, name="otherusertrip"),
#    url(r'^yourtrips$', views.yourtrips, name="yourtrips"),
#    url(r'^join/(?P<id>\d+)$', views.join, name="join"),
    url(r'^destination/(?P<id>\d+)$', views.destination, name="destination"),
#    url(r'^home$', views.home, name="home"),
  ]
