from django.conf.urls import url

from .views import (
    TimKiemSanPhamView

)

urlpatterns = [
    url(r'^$', TimKiemSanPhamView.as_view(), name='query'), 
]