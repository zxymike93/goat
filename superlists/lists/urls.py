from django.conf.urls import url

from lists.views import home_page, view_list


urlpatterns = [
    url(r'^$', home_page),
    url(r'^lists/the-only-list-in-the-world/$', view_list, name='view_list'),
]
