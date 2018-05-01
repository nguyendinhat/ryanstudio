from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import pre_save, post_save

# from taikhoan.signals import get_taikhoan_dangnhap
from .signals import get_ip_khachhang
from .signals import get_luotxem

taikhoan = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION= getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)

class LuotXemQuerySet(models.query.QuerySet):
    def by_model(self, models_class, model_queryset=False):        
        content_type = ContentType.objects.get_for_model(models_class)
        qs = self.filter(content_type=content_type)
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            return models_class.objects.filter(pk__in=viewed_ids)
        return qs

class LuotXemManager(models.Manager):
    def get_queryset(self):
        return LuotXemQuerySet(self.model, using=self._db)

    def by_model(self, models_class, model_queryset=False):
        return self.get_queryset().by_model(models_class, model_queryset=model_queryset)

class LuotXem(models.Model):
    taikhoan            = models.ForeignKey(taikhoan, blank=True, null=True)
    ip_address          = models.CharField(max_length=220, blank=True, null=True)
    content_type        = models.ForeignKey(ContentType)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey('content_type', 'object_id')
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects             = LuotXemManager()

    def __str__(self):
        return "%s đã xem vào lúc %s" %(self.content_object, self.timestamp)
    
    class Meta:
        db_table = 'phantich'
        verbose_name = 'Lượt Xem'
        verbose_name_plural = 'Lượt Xem'

def receiver_luotxem(sender, instance, request, *args, **kwargs):
    content_type    = ContentType.objects.get_for_model(sender)
    taikhoan        = None
    if request.user.is_authenticated():
        taikhoan = request.user
    LuotXem.objects.create(
        taikhoan        = taikhoan, 
        content_type    = content_type,
        object_id       = instance.id,
        ip_address      = get_ip_khachhang(request)
    )

get_luotxem.connect(receiver_luotxem)