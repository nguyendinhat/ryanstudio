from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import ThanhVien, Khach, BoPhan, NhanVienBoPhan
from .forms import UserAdminCreationForm, UserAdminChangeForm

class ThanhVienAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'full_name', 'ngaysinh', 'gioitinh', 'sdt', 'is_active', 'is_staff', 'is_admin', 'last_login')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login')}),
        ('Personal info', {'fields': ('full_name','ngaysinh','gioitinh', 'sdt')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active',)}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'ngaysinh', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email',)
    
    filter_horizontal = ()

admin.site.register(ThanhVien, ThanhVienAdmin)
admin.site.unregister(Group)

class KhachAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = Khach

admin.site.register(Khach, KhachAdmin)

class BoPhanAdmin(admin.ModelAdmin):
    search_fields = ['ten_bophan']
    class Meta:
        model = BoPhan

admin.site.register(BoPhan, BoPhanAdmin)

class NhanVienBoPhanAdmin(admin.ModelAdmin):
    list_display = ('bophan', 'thanhvien', 'is_active')
    search_fields = ['bophan', 'bophan']
    class Meta:
        model = NhanVienBoPhan

admin.site.register(NhanVienBoPhan, NhanVienBoPhanAdmin)