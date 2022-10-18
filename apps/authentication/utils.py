
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import user_logged_out

def logout_user(request):

    Token.objects.filter(user=request.user).delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    if request.user.is_authenticated:
        logout(request)