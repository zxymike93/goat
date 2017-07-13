from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from accounts.models import Token
# from utils import log


def send_login_email(request):
    email = request.POST['email']
    # log(type(send_mail))
    token = Token.objects.create(email=email)
    path = reverse('login')
    query = '?token={}'.format(token.uid)
    url = request.build_absolute_uri(path + query)
    body = 'Use this link to log in: {}'.format(url)
    send_mail(
        'Your login link for Superlists',
        body,
        'zxymike93@163.com',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user:
        auth.login(request, user)
    return redirect('/')
