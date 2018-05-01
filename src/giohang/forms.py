from django import forms
from .models import GioHang

class DiaChiForm(forms.ModelForm):
    full_name = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    sdt = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    diachi = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    tinh_thanh = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    quan_huyen = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    xa_phuong = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = GioHang
        fields = ('full_name', 'sdt', 'tinh_thanh', 'quan_huyen', 'xa_phuong')

class ThanhToanForm(forms.ModelForm):
    so_the = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    hoten_the = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    exp_month = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    exp_year = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    cvv = forms.CharField(
        label   ='',
        widget  = forms.TextInput(
            attrs = {
                "class": "form-control",
            }
        )
    )
    class Meta:
        model = GioHang
        fields = ('so_the', 'hoten_the', 'exp_month', 'exp_year', 'cvv')