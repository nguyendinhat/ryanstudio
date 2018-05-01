from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed

from taikhoan.models import Khach, ThanhVien
from sanpham.models import SanPham

Taikhoan = settings.AUTH_USER_MODEL

GH_PPTT_CHOICES = (
    ('cod', 'COD'),
    ('credit', 'Thẻ tín Dụng'),
)

GH_TRANGTHAI_CHOICES = (
    ('created', 'Đã tạo giỏ hàng'),
    ('paid', 'Đã thanh toán'),
    ('shipping', 'Đang giao hàng'),
    ('shipped', 'Đã giao hàng'),
)


class GioHangManager(models.Manager):
    # def get_queryset(self):
    #     return self.get_queryset().active()

    def new_or_get(self, request):
        id_giohang = request.session.get("id_giohang", None)
        id_khach = request.session.get("id_khach", None)
        # có user, có giỏ hàng db
        if request.user.is_authenticated() and GioHang.objects.filter(taikhoan=request.user,status="created").count()>=1:
            qs = GioHang.objects.filter(taikhoan=request.user,status="created")
            qs1 = GioHang.objects.filter(id_giohang=id_giohang,status="created")
            giohang_obj = qs.first()
            # có user, đã có giỏ hàng db, lại tạo giỏ hàng mới(request), 
            # sp trong ghm >>> ghc nếu có thì thêm số lượng
            # clean db dư thừa
            if qs1.count()==1 and qs1.first() != qs.first():
                giohang_moi = GioHang.objects.filter(id_giohang=id_giohang,status="created")
                giohang_sanpham_moi= GioHangSanPham.objects.filter(giohang=giohang_moi)
                for spgh_m in giohang_sanpham_moi:
                    spgh_c = GioHangSanPham.objects.filter(giohang=giohang_obj, sanpham=spgh_m.sanpham).first() or None
                    if spgh_c is not None:
                        spgh_cu = GioHangSanPham.objects.get(giohang=giohang_obj, sanpham=spgh_m.sanpham)
                        spgh_cu.soluong = spgh_cu.soluong + spgh_m.soluong
                        spgh_cu.save()                       
                    else:
                        sp_m = GioHangSanPham.objects.create(giohang=giohang_obj,sanpham=spgh_m.sanpham, soluong=spgh_m.soluong)    
                        sp_m.save()
                for item in GioHangSanPham.objects.filter(giohang=giohang_moi):
                    item.delete()
                giohang_moi.delete()            
            request.session['id_giohang'] = giohang_obj.id_giohang
            return giohang_obj
         # có giỏ hàng request
        if GioHang.objects.filter(id_giohang=id_giohang,status="created").count()==1:
            qs = GioHang.objects.filter(id_giohang=id_giohang,status="created")
            giohang_obj = qs.first()
            # có giỏ hàng request, có user, không có giỏ hàng db
            if request.user.is_authenticated() and giohang_obj.taikhoan is None and giohang_obj.email is None :
                giohang_obj.taikhoan = ThanhVien.objects.get(email=request.user.email)
                giohang_obj.email = request.user.email
                giohang_obj.save()
            # có giỏ hàng request, có khách
            elif id_khach is not None:
                giohang_obj.email = Khach.objects.get(id=id_khach).email
                giohang_obj.save()                
            return giohang_obj
        # không giỏ hàng request           
        giohang_obj = GioHang.objects.new(taikhoan=request.user)
        request.session['id_giohang'] = giohang_obj.id_giohang
        return giohang_obj

    def new(self, taikhoan=None):
        taikhoan_obj = None
        email_obj = None
        if taikhoan is not None:
            if taikhoan.is_authenticated():
                taikhoan_obj = taikhoan
                email_obj = taikhoan.email
        return self.model.objects.create(taikhoan=taikhoan_obj, email=email_obj)
                

class GioHang(models.Model):
    id_giohang              = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    taikhoan                = models.ForeignKey(Taikhoan, db_column='id_taikhoan', blank=True, null=True)
    email                   = models.EmailField(blank=True, null=True)
    sanpham                 = models.ManyToManyField(SanPham, through='GioHangSanPham')
    full_name               = models.CharField(max_length=50)    
    sdt_regex               = RegexValidator(regex=r'^\d{10,11}$', message="Số điện thoại không hợp lệ")
    sdt                     = models.CharField(validators=[sdt_regex], max_length=11, blank=True)
    diachi                  = models.CharField(max_length=255)
    tinh_thanh              = models.CharField(max_length=50)
    quan_huyen              = models.CharField(max_length=50)
    xa_phuong               = models.CharField(max_length=50)
    phigiaohang             = models.PositiveIntegerField(default=0)
    giamgia                 = models.PositiveIntegerField(default=0)
    tong_thanhtien          = models.PositiveIntegerField(default=0)
    tong_cong               = models.PositiveIntegerField(default=0)
    loai_thanhtoan          = models.CharField(max_length=6, choices=GH_PPTT_CHOICES, blank=True, null=True)
    so_the                  = models.CharField(max_length=16, null=True, blank=True)
    hoten_the               = models.CharField(max_length=50, blank=True, null=True)
    ngayhethan              = models.CharField(max_length=9, blank=True, null=True)
    cvv                     = models.CharField(max_length=3, blank=True, null=True)    
    status                  = models.CharField(max_length=8, choices=GH_TRANGTHAI_CHOICES, default='created')
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)
    capnhat                 = models.DateTimeField(auto_now=True)
    
    objects = GioHangManager()

    class Meta:
        db_table = 'giohang'

    def __str__(self):
        return str(self.id_giohang)

    def get_diachi(self):
        return "{diachi}, {xa_phuong}, {quan_huyen}, {tinh_thanh}".format(
                diachi          = self.diachi,
                xa_phuong       = self.xa_phuong,
                quan_huyen      = self.quan_huyen,
                tinh_thanh      = self.tinh_thanh,
        )

    def update_tong_thanhtien(self):
        total = 0
        items = GioHangSanPham.objects.get_spgh(giohang=self)
        for item in items:
            total += item.thanhtien
        self.tong_thanhtien = total + self.phigiaohang - self.giamgia
        self.save()

    def check_done(self):       
        diachi     = False      
        thanhtoan  = False
        if all(i is not None for i in [self.diachi, self.tinh_thanh, self.quan_huyen, self.xa_phuong]):
            diachi = True
        if self.loai_thanhtoan == "cod":
            thanhtoan = True
        elif self.loai_thanhtoan == "credit":
            if all(i is not None for i in [self.so_the, self.hoten_the, self.ngayhethan, self.cvv]):
                thanhtoan = True        
        if diachi and thanhtoan and self.tong_thanhtien > 0:
            return True
        return False

    def refresh_status(self):
        if self.status!='paid':
            if self.check_done():
                self.status = "paid"
                self.save()
            else:
                self.status = "created"
                self.save()
        return self.status

    def check_hethang(self):
        for item in GioHangSanPham.objects.get_spgh(self):
            if item.active == False:
                return True
        return False

def giohang_receiver(sender, instance, *args, **kwargs):
    instance.tong_cong = instance.tong_thanhtien + instance.phigiaohang - instance.giamgia
    
pre_save.connect(giohang_receiver, sender=GioHang)



class GioHangSanPhamQuerySet(models.query.QuerySet):
    def get_item(self, giohang, sanpham):
        return self.filter(giohang=giohang, sanpham=sanpham)
    
    def get_spgh(self, giohang):
        return self.filter(giohang=giohang)

class GioHangSanPhamManager(models.Manager):
    def get_queryset(self):
        return GioHangSanPhamQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def get_item(self, giohang, sanpham):
        return self.get_queryset().filter(giohang=giohang, sanpham=sanpham)

    def get_spgh(self, giohang):
       return self.get_queryset().filter(giohang=giohang)

class GioHangSanPham(models.Model):
    giohang     = models.ForeignKey(GioHang, db_column='id_giohang')
    sanpham     = models.ForeignKey(SanPham, db_column='id_sanpham')
    soluong     = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    thanhtien   = models.PositiveIntegerField(default=0)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=False)

    objects     = GioHangSanPhamManager()

    class Meta:
        db_table = 'giohang_sanpham'
        unique_together = (("giohang", "sanpham"))
        ordering = ['timestamp']

    def capnhat_soluong(self, soluong):
        self.soluong = soluong
        self.save()
    
    def capnhat_trangthai(self, slc):
        self.active = False
        if slc > 0: 
            self.active = True
        self.save()

def pre_save_giohangsanpham_receiver(sender, instance, *args, **kwargs):
    instance.thanhtien = instance.sanpham.dongia*instance.soluong
    
pre_save.connect(pre_save_giohangsanpham_receiver, sender=GioHangSanPham)

def post_save_ghsp_receiver(sender, instance, *args, **kwargs):
    instance.giohang.update_tong_thanhtien()

post_save.connect(post_save_ghsp_receiver, sender=GioHangSanPham)

post_delete.connect(post_save_ghsp_receiver, sender=GioHangSanPham)