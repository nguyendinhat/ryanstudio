from django.db import models

class GiamGia(models.Model):
    id_giamgia      = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    ma_giamgia      = models.CharField(max_length=20)
    mota            = models.TextField(blank=True, null=True)
    batdau          = models.DateTimeField(auto_now_add=True, blank=True)
    ketthuc         = models.DateTimeField(blank=True)
    soluong         = models.IntegerField(blank=True, default=1)
    khautru         = models.DecimalField(default=0, max_digits=65, decimal_places=3)