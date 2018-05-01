from django.conf.urls import url

from .views import SanPhamView, ChiTietSanPhamView

urlpatterns = [
    url(r'^$', SanPhamView.as_view(), name='danhsach-sanpham'),
    url(r'^(?P<slug>[\w-]+)/$', ChiTietSanPhamView.as_view(), name='chitiet-sanpham'),
]
