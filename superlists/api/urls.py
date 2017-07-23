from django.conf.urls import url

from api.views import lists


urlpatterns = [
    url(r'^lists/(\d+)/', lists, name='api_lists'),
]
