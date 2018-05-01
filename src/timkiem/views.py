from django.shortcuts import render
from django.views.generic import ListView

from sanpham.models import SanPham

class TimKiemSanPhamView(ListView):
    template_name = "timkiem/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TimKiemSanPhamView, self).get_context_data(*args,**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:            
            return SanPham.objects.search(query)
        return SanPham.objects.sanpham_noibat()