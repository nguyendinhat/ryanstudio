from django.dispatch import Signal

get_luotxem = Signal(providing_args=['instance', 'request'])

def get_ip_khachhang(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip