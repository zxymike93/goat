from django.conf.urls import url

from lists.views import home_page


urlpatterns = [
    url(r'^$', home_page),
    url(r'lists/new/$', 'lists.views.new_list', name='new_list'),
    url(r'lists/(.+)/$', 'lists.views.view_list', name='view_list'),
]
