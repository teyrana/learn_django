from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register, name='index'),
    url(r'^register', views.result ),
    url(r'^list', views.list ),
    url(r'^send', views.send ),
]
