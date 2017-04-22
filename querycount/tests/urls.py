from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^empty/$', views.empty, name='empty'),
    url(r'^count/$', views.count_migrations, name='count'),
]
