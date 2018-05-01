from django.contrib import admin

from .models import SanPham, DanhMuc


class SanPhamAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'slug', 'danhmuc', 'dongia', 'soluong', 'active', 'noibat')
    search_fields = ['ten', 'dongia', 'soluong']
    class Meta:
        model = SanPham
admin.site.register(SanPham, SanPhamAdmin)

class DanhMucAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'danhmuc_cha', 'slug', 'hinhanh', 'active', 'timestamp')
    search_fields = ['ten', 'danhmuc_cha', 'slug']
    class Meta:
        model = DanhMuc

admin.site.register(DanhMuc, DanhMucAdmin)