from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from giohang.models import GioHang, GioHangSanPham

def home_view(request):
    giohang_obj = GioHang.objects.new_or_get(request)
    request.session['giohang_items_count'] =  giohang_obj.sanpham.count() or 0
    request.session['email_check_order']  = None
    return render(request, "home.html", {})
