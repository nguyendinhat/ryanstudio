import random
import os
# Django library
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
# App
from ryanstudio.utils import unique_slug_generator, get_filename_ext

def upload_hinhanh_sanpham(instance, filename):
    ext = get_filename_ext(filename)
    new_filename = random.randint(1000000000,9999999999)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    location = "images/sanpham/"
    return location + final_filename

def upload_hinhanh_danhmuc(instance, filename):
    ext = get_filename_ext(filename)
    new_filename = random.randint(1000000000,9999999999)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    location = "images/danhmuc/"
    return location + final_filename

class DanhMucQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class DanhMucManager(models.Manager):
    def get_queryset(self):
        return DanhMucQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id_danhmuc):
        qs = self.get_queryset().filter(id_danhmuc=id_danhmuc)
        if qs.count() == 1:
            return qs.first()
        return None

class DanhMuc(models.Model):
    id_danhmuc  = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    danhmuc_cha = models.ForeignKey('self', null=True, blank=True, db_index=True, db_column='id_danhmuc_cha',)
    ten         = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    hinhanh     = models.ImageField(upload_to=upload_hinhanh_danhmuc, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)

    objects     = DanhMucManager()
    
    class Meta:
        db_table = 'danhmuc'

    def __str__(self):
        return self.ten

    def get_absolute_url(self, ancestors=None):    
        return reverse('sanpham:danhmuc', kwargs={'id_danhmuc': self.id_danhmuc, 'slug': self.slug})

def pre_save_danhmuc_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_danhmuc_receiver, sender=DanhMuc)

class SanPhamQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def sanpham_noibat(self):
        return self.filter(noibat=True, active=True)
    def search(self, query):
        lookups =  (
            Q(ten__icontains=query) |
            Q(mota__icontains=query) |
            Q(dongia__icontains=query) |
            Q(danhmuc__ten__icontains=query)
        )
        return self.filter(lookups).distinct()

class SanPhamManager(models.Manager):
    def get_queryset(self):
        return SanPhamQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def sanpham_noibat(self):
        return self.get_queryset().sanpham_noibat()

    def get_by_id(self, id_sanpham):
        qs = self.get_queryset().filter(id_sanpham=id_sanpham)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):        
        return self.get_queryset().active().search(query)

class SanPham(models.Model):
    id_sanpham      = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    danhmuc         = models.ForeignKey(DanhMuc, blank=True, null=True, db_column='id_danhmuc')
    ten             = models.CharField(max_length=255)
    hinhanh         = models.ImageField(upload_to=upload_hinhanh_sanpham, null=True, blank=True)
    slug            = models.SlugField(max_length=255, blank=True, unique=True)
    mota            = models.TextField(blank=True, null=True)
    dongia          = models.PositiveIntegerField(default=0)
    donvi           = models.CharField(max_length=120)
    chatlieu        = models.CharField(max_length=120)
    trongluong      = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    chieudai        = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    chieurong       = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    chieucao        = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    soluong         = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    vitri           = models.CharField(max_length=120, blank=True, null=True)
    active          = models.BooleanField(default=True)
    noibat          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)
    
    objects = SanPhamManager()

    class Meta:
        db_table = 'sanpham'

    def get_absolute_url(self):    
        return reverse('sanpham:chitiet-sanpham', kwargs={'slug': self.slug})

    def __str__(self):
        return self.ten
    
def pre_save_sanpham_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_sanpham_receiver, sender=SanPham)


