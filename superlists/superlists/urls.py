from django.conf.urls import include, url
from django.contrib import admin

from lists import urls as lists_url


urlpatterns = [
    # Examples:
    # url(r'^$', 'superlists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(lists_url)),
    # url(r'^admin/', include(admin.site.urls)),
]
