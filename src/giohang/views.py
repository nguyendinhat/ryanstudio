from django.conf import settings
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .models import GioHang, GioHangSanPham
from .forms import DiaChiForm
from .shippingfee import get_shipping_fee

from taikhoan.models import ThanhVien, Khach
from taikhoan.forms import LoginForm, KhachForm
from sanpham.models import SanPham

def giohang_sanpham_view(request):
    giohang_obj = GioHang.objects.new_or_get(request)
    sanpham = [
        {
            "id_sanpham": item.id_sanpham,
            "url": item.get_absolute_url(),
            "ten": item.ten,
            "dongia": item.dongia,
            "soluong": GioHangSanPham.objects().filter(giohang=giohang_obj, sanpham=item).soluong,
            "thanhtien": GioHangSanPham.objects().filter(giohang=giohang_obj, sanpham=item).thanhtien,
        } for item in giohang_obj.sanpham.all()
    ]    
    giohang_data = {
        "sanpham": sanpham, 
        "phigiaohang": giohang_obj.phigiaohang,
        "giamgia": giohang_obj.giamgia,
        "tong_thanhtien": giohang_obj.tong_thanhtien
    }
    return JsonResponse(giohang_data)

def new(self, taikhoan=None):
    taikhoan_obj = None
    if taikhoan is not None:
        if taikhoan.is_authenticated():
            taikhoan_obj = taikhoan

    return GioHang.objects.create(taikhoan=taikhoan_obj, status='created')

def giohang_view(request):
    giohang_obj = GioHang.objects.new_or_get(request)
    request.session['giohang_items_count'] = giohang_obj.sanpham.count() or 0
    ghsp = GioHangSanPham.objects.get_spgh(giohang=giohang_obj)    
    for spgh in ghsp:
        sp = SanPham.objects.get_by_id(spgh.sanpham.id_sanpham)
        spgh.capnhat_trangthai(sp.soluong)
    context = {
        "giohang": giohang_obj,
        "ghsp": ghsp
    }
    return render(request, "giohang/home.html", context)
   

def giohang_capnhat(request):
    id_sanpham      = request.POST.get('id_sanpham', None) 
    soluong         = request.POST.get('soluong', None)
    if id_sanpham is not None and soluong is None:
        try:
            sanpham_obj = SanPham.objects.get(id_sanpham=id_sanpham)
        except ObjectDoesNotExist:
            print("Không tìm thấy sp")
        giohang_obj = GioHang.objects.new_or_get(request)
        if sanpham_obj in giohang_obj.sanpham.all():
            ghsp = GioHangSanPham.objects.filter(giohang=giohang_obj,sanpham=sanpham_obj)
            ghsp.delete()
            added = False
        else:
            ghsp = GioHangSanPham(giohang=giohang_obj,sanpham=sanpham_obj)
            ghsp.save()
            added = True 
        if request.is_ajax():
            json_data = {
                "added": added,
                "remove": not added,
                "hethang": giohang_obj.check_hethang(),
                "giohangItemsCount": giohang_obj.sanpham.count() or 0
            }
        request.session['giohang_items_count'] = giohang_obj.sanpham.count() or 0
        return JsonResponse(json_data, status=200)
    if id_sanpham is not None and soluong is not None:       
        try:
            sanpham_obj = SanPham.objects.get(id_sanpham=id_sanpham)
        except ObjectDoesNotExist:
            print("Không tìm thấy sp")
        giohang_obj = GioHang.objects.new_or_get(request)
        if sanpham_obj in giohang_obj.sanpham.all() and int(soluong) <= sanpham_obj.soluong:
            ghsp = GioHangSanPham.objects.get(giohang=giohang_obj,sanpham=sanpham_obj)
            ghsp.capnhat_soluong(int(soluong))
            return HttpResponse({"message": "success"},status=201)
        else:
            return HttpResponse({"message": "error"}, status_code=401)        
    return redirect("giohang:home")

def thanhtoan_view(request):
    hoten           = request.POST.get('hoten', None)
    sdt             = request.POST.get('sdt', None)
    diachi          = request.POST.get('diachi', None)
    tinh_thanh      = request.POST.get('tinhthanh', None)
    quan_huyen      = request.POST.get('quanhuyen', None)
    xa_phuong       = request.POST.get('xaphuong', None)
    loai_thanhtoan  = request.POST.get('loai_thanhtoan', None)
    so_the          = request.POST.get('so_the', None)
    hoten_the       = request.POST.get('hoten_the', None)
    ngayhethan      = request.POST.get('ngayhethan', None)
    ccv             = request.POST.get('ccv', None)
    ma_tinhthanh    = request.POST.get('ma_tinhthanh', None)
    # ma_khuyenmai    = request.POST.get('ma_khuyenmai', None)
    
    giohang_obj = GioHang.objects.new_or_get(request)
    ghsp = GioHangSanPham.objects.get_spgh(giohang=giohang_obj)
    tong_trongluong = 0
    for spgh in ghsp:
        sp = SanPham.objects.get_by_id(spgh.sanpham.id_sanpham)
        tong_trongluong = tong_trongluong + (sp.trongluong*spgh.soluong)
    # print(tong_trongluong)
    request.session['giohang_items_count'] = giohang_obj.sanpham.count() or 0
    if giohang_obj.sanpham.count() == 0 or giohang_obj.check_hethang():
        return redirect("giohang:home")
    elif giohang_obj.email is None:
        return redirect("giohang:authentication")
    if request.method == "POST":
        for spgh in ghsp:
            sp = SanPham.objects.get_by_id(spgh.sanpham.id_sanpham)
            if spgh.soluong > sp.soluong:
                error: "limitover"
                return JsonResponse(error, status=204)
        if all(i is not None for i in [hoten,sdt,diachi, tinh_thanh, quan_huyen, xa_phuong, loai_thanhtoan, ma_tinhthanh]):
            giohang_obj.full_name       = hoten
            giohang_obj.sdt             = sdt
            giohang_obj.diachi          = diachi
            giohang_obj.tinh_thanh      = tinh_thanh
            giohang_obj.quan_huyen      = quan_huyen
            giohang_obj.xa_phuong        = xa_phuong
            giohang_obj.loai_thanhtoan  = loai_thanhtoan
            giohang_obj.phigiaohang     = get_shipping_fee(ma_tinhthanh,tong_trongluong)
            
            if loai_thanhtoan == "credit":
                giohang_obj.so_the      = so_the
                giohang_obj.hoten_the   = hoten_the
                giohang_obj.ngayhethan  = ngayhethan
                giohang_obj.ccv         = ccv
            
            if giohang_obj.check_done():  
                giohang_obj.save()          
                for spgh in ghsp:
                    sp = SanPham.objects.get_by_id(spgh.sanpham.id_sanpham)
                    sp.soluong = sp.soluong - spgh.soluong
                    sp.save()
                giohang_obj.refresh_status()
                del request.session['id_giohang']
                request.session['giohang_items_count'] = 0
                return HttpResponse({"message": "success"},status=202)

    context = {
        "giohang": giohang_obj,
        "ghsp": ghsp,
        "tong_trongluong": tong_trongluong
    }
    return render(request, "giohang/thanhtoan.html", context)

def thanhtoan_auth_view(request):
    giohang_obj = GioHang.objects.new_or_get(request)
    if giohang_obj.email is not None:
        return redirect("giohang:thanhtoan")
    request.session['giohang_items_count'] = giohang_obj.sanpham.count() or 0
    login_form              = LoginForm(request=request)
    khach_form              = KhachForm(request=request)
    context = {
        "giohang": giohang_obj,
        "login_form": login_form,
        "khach_form": khach_form,
    }
    return render(request, "giohang/thanhtoan_auth.html", context)

def thanhtoan_thangcong_view(request):
    return render(request, "giohang/thanhtoan_xong.html", {})
