from django.conf.urls import include, url
# from django.contrib import admin

from accounts import urls as accounts_urls
from lists import urls as lists_urls
from lists import views as lists_views


urlpatterns = [
    # Examples:
    # url(r'^$', 'superlists.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', lists_views.home_page, name='home_page'),
    url(r'^lists/', include(lists_urls)),
    url(r'^accounts/', include(accounts_urls)),
    # url(r'^admin/', include(admin.site.urls)),
]
