from django.conf.urls import include, url
# from django.contrib import admin


urlpatterns = [
    url(r'^$', 'lists.views.home_page', name='home_page'),
    url(r'^lists/', include('lists.urls')),
    url(r'^accounts/', include('accounts.urls')),
    # url(r'^admin/', include(admin.site.urls)),
]
