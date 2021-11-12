from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser

def get_tipo_usuario_request(request):
    try:
        customuser = CustomUser.objects.get(user_ptr=request.user)
        return customuser.tipo_usuario
    except CustomUser.DoesNotExist:
        return 'A' #then user is admin

def get_tipo_usuario(user):
    try:
        customuser = CustomUser.objects.get(user_ptr=user)
        return customuser.tipo_usuario
    except CustomUser.DoesNotExist:
        return 'A' # then user is admin

def comprador_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    decorator = user_passes_test(
        lambda u: get_tipo_usuario(u) == 'C' or get_tipo_usuario(u) == 'A',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator

def leiloeiro_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    decorator = user_passes_test(
        lambda u: get_tipo_usuario(u) == 'L' or get_tipo_usuario(u) == 'A',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return decorator(function)
    return decorator

def vendedor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    decorator = user_passes_test(
        lambda u: get_tipo_usuario(u) == 'V' or get_tipo_usuario(u) == 'A',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return decorator(function)
    return decorator