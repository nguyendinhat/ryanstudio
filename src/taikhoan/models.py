from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from ryanstudio.utils import unique_id_giohang_generator

TV_GIOITINH_CHOICES = (
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('undefined', 'Chưa xác định'),
)

class ThanhVienManager(BaseUserManager):
    def create_user(self, email, full_name, ngaysinh, password=None, is_active=True, is_admin=False, is_staff=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')
        if not full_name:
            raise ValueError("User must have a full name")
        tv = self.model(email=self.normalize_email(email))
        tv.set_password(password)
        tv.ngaysinh     = ngaysinh
        tv.is_active    = is_active        
        tv.is_staff     = is_staff
        tv.is_admin     = is_admin       
        
        tv.save(using=self._db)
        return tv

    def create_staffuser(self, email, full_name, ngaysinh=None, password=None, **extra_fields):
        tv = self.model(email=self.normalize_email(email))
        tv.full_name  = full_name
        tv.ngaysinh=ngaysinh
        tv.set_password(password)
        tv.is_staff = True
        tv.save(using=self._db)        
        return tv

    def create_superuser(self, email, full_name, ngaysinh=None, password=None, **extra_fields):
        tv = self.model(email=self.normalize_email(email))
        tv.set_password(password)
        tv.full_name    = full_name
        tv.ngaysinh     =ngaysinh       
        tv.is_staff     = True
        tv.is_admin     = True
        tv.save(using=self._db)
        return tv


class ThanhVien(AbstractBaseUser):
    id_thanhvien    = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    email           = models.EmailField(max_length=255,unique=True,)
    full_name       = models.CharField(max_length=255, blank=True, null=True)
    ngaysinh        = models.DateField(blank=True, null=True)
    gioitinh        = models.CharField(max_length=9, default='undefined', choices=TV_GIOITINH_CHOICES)
    sdt_regex       = RegexValidator(regex=r'^\d{10,11}$', message="Số điện thoại không hợp lệ")
    sdt             = models.CharField(validators=[sdt_regex], max_length=11, blank=True)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = ThanhVienManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'taikhoan'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def admin(self):
        "Is the user a admin member?"
        return self.is_admin

    @property
    def active(self):
        "Is the user active?"
        return self.is_active

class Khach(models.Model):
    email       = models.EmailField()
    is_active   = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects     = models.query.QuerySet()

    class Meta:
        db_table = 'khach'

    def __str__(self):
        return self.email

class BoPhan(models.Model):
    id_bophan   = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    ten_bophan  = models.CharField(max_length=255, blank=True, null=True)
    mota        = models.TextField()

    class Meta:
        db_table = 'bophan'

    def __str__(self):
        return self.ten_bophan

class NhanVienBoPhan(models.Model):
    thanhvien = models.ForeignKey(ThanhVien, on_delete=models.CASCADE, db_column='id_thanhvien', verbose_name=('thanhvien'),  db_index=False)
    bophan = models.ForeignKey(BoPhan, on_delete=models.CASCADE, db_column='id_bophan', verbose_name=('bophan'),  db_index=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'nhanvien_bophan'
        unique_together = (("thanhvien", "bophan")) 

    def __str__(self):
        return str(self.bophan)
