from django.conf.urls import url


urlpatterns = [
    url(r'^send_login_email/$', 'accounts.views.send_login_email',
        name='send_login_email'),
]
