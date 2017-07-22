from django.conf.urls import url

from api import api_lists


urlpatterns = [
    url(r'^lists/(\d+)/', api_lists, name='api_lists'),
]
