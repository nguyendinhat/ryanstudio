from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LogoutView

from django.conf.urls import url
from django.contrib import admin

from .views import home_view
from taikhoan.views import LoginView, RegisterView, GuestRegisterView
from sanpham.views import SanPhamDanhMucView
from giohang.views import giohang_sanpham_view, donhang_view, chitiet_donhang_view

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/guest$', GuestRegisterView.as_view(), name='guest_register'),
    url(r'^danhmuc/(?P<slug>[\w-]+)/$', SanPhamDanhMucView.as_view(), name='sanpham-danhmuc'),
    url(r'^sanpham/', include("sanpham.urls", namespace='sanpham')),
    url(r'^timkiem/', include("timkiem.urls", namespace='search')),
    url(r'^giohang/', include("giohang.urls", namespace='giohang')),
    url(r'^api/giohang/$', giohang_sanpham_view, name='api-giohang'),
    url(r'^taikhoan/', include("taikhoan.urls", namespace='taikhoan')),
    url(r'^donhang/$', donhang_view, name='donhang-list'),
    url(r'^donhang/(?P<id_giohang>[0-9A-Za-z]+)/$', chitiet_donhang_view, name='donhang-chitiet'),
    
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
