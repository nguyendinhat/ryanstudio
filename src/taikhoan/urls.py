from django.conf.urls import url

from .views import taikhoan_view

urlpatterns = [
    url(r'^$', taikhoan_view, name='home'),
    # url(r'^update/$', giohang_capnhat, name='update'),
    # url(r'^thanhtoan/$', thanhtoan_view, name='thanhtoan'),
    # url(r'^thanhtoan/authentication/$', thanhtoan_auth_view, name='authentication'),
    # url(r'^thanhtoan/success$', thanhtoan_thangcong_view, name='success'),
]
