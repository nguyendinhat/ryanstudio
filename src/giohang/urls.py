from django.conf.urls import url

from .views import giohang_view, giohang_capnhat, thanhtoan_view, thanhtoan_auth_view, thanhtoan_thangcong_view

urlpatterns = [
    url(r'^$', giohang_view, name='home'),
    url(r'^update/$', giohang_capnhat, name='update'),
    url(r'^thanhtoan/$', thanhtoan_view, name='thanhtoan'),
    url(r'^thanhtoan/authentication/$', thanhtoan_auth_view, name='authentication'),
    url(r'^thanhtoan/success$', thanhtoan_thangcong_view, name='success'),
]
