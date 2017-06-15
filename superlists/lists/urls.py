from django.conf.urls import url

from lists.views import home_page


urlpatterns = [
    url(r'^$', home_page),
]
