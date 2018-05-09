from django.contrib import admin
from .models import GioHang, GioHangSanPham

class GioHangAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'email', 'taikhoan', 'tong_thanhtien', 'phigiaohang', 'giamgia','tong_cong', 'loai_thanhtoan', 'status', 'active', 'ngaydat','timestamp', 'capnhat')
    search_fields = ['__str__', 'taikhoan', 'email', 'soluong']
    class Meta:
        model = GioHang
admin.site.register(GioHang, GioHangAdmin)

class GioHangSanPhamAdmin(admin.ModelAdmin):
    list_display    = ('giohang', 'sanpham', 'soluong', 'thanhtien', 'timestamp')
    search_fields = ['giohang', 'sanpham']
    class Meta:
        model = GioHangSanPham

admin.site.register(GioHangSanPham, GioHangSanPhamAdmin)