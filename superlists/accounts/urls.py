from django.conf.urls import url


urlpatterns = [
    url(r'^send_login_email/$', 'accounts.views.send_login_email',
        name='send_login_email'),
    url(r'^login$', 'accounts.views.login', name='login'),
    url(r'^logout$', 'accounts.views.logout', name='logout'),
]
