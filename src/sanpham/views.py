from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from thongke.mixins import ObjectViewedMixin
from giohang.models import GioHang
# from orders.models import ProductPurchase
from .models import SanPham, DanhMuc

class SanPhamView(ListView):
    template_name = "sanpham/danh_sach.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SanPhamView,self).get_context_data(*args, **kwargs)
        giohang_obj = GioHang.objects.new_or_get(self.request)
        self.request.session['giohang_items_count'] =  giohang_obj.sanpham.count() or 0
        context['giohang'] = giohang_obj        
        
        return context
    
    def get_queryset(self):
        request = self.request
        return SanPham.objects.all().order_by("-timestamp")

class ChiTietSanPhamView(ObjectViewedMixin,DetailView): 
    queryset = SanPham.objects.all()
    template_name = "sanpham/chi_tiet.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ChiTietSanPhamView, self).get_context_data(*args, **kwargs)
        giohang_obj = GioHang.objects.new_or_get(self.request)
        context['giohang'] = giohang_obj
        return context
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = get_object_or_404(SanPham, slug=slug, active=True)
        except ObjectDoesNotExist:
            raise Http404("Không tìm thấy sản phẩm")
        except MultipleObjectsReturned:
            qs = SanPham.objects.filter(slug=slug, active=True)
            return qs.first()
        except:
            raise Http404("oops!")
        return instance

class SanPhamDanhMucView(ListView):
    template_name = "sanpham/danh_sach.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SanPhamDanhMucView,self).get_context_data(*args, **kwargs)
        return context
    
    def get_queryset(self):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = get_object_or_404(DanhMuc, slug=slug, active=True)                
            danhmuc_con = []
            danhmuc_con.append(instance.id_danhmuc)
            for dm in DanhMuc.objects.filter(danhmuc_cha=instance):
                danhmuc_con.append(dm)
            for dm in danhmuc_con:
                for edm in DanhMuc.objects.filter(danhmuc_cha=dm):
                    danhmuc_con.append(edm)
            return SanPham.objects.filter(danhmuc__in=danhmuc_con).order_by("-timestamp")
            
        except ObjectDoesNotExist:
            raise Http404("Không tìm thấy danh mục")
        except:
            raise Http404("oops!")