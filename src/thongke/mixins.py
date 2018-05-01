from .signals import get_luotxem

class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        instance  = context.get('object')
        if instance:
            get_luotxem.send(instance.__class__, instance=instance, request=request)
        return context