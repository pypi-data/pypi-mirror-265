import uuid
from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel


class BaseModelAbstract(SafeDeleteModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    
    deleted = models.BooleanField(default=False)
    deleted_by_id = models.UUIDField(blank=True, null=True, editable=False)

    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_test = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        ordering = ('-created_at', )

    def delete(self, by=None, force_policy=None, **kwargs):
        self.deletedBy = by
        self.deleted = True
        return super(BaseModelAbstract, self).delete(force_policy, **kwargs)

    def undelete(self, force_policy=None, **kwargs):
        self.deletedBy = None
        self.deleted = False
        return super(BaseModelAbstract, self).undelete(force_policy, **kwargs)

    def __str__(self):
        return self.__unicode__()

    @property
    def is_fully_filled(self):
        ''' Checks if all the fields have been filled '''
        all_fields_names = [f.name for f in self._meta.get_fields()]
        exempt = ['deleted', 'deleted_by_id', 'deleted_at', 'created_at',
                  'updated_at', 'is_test', 'company']
        fields_names = set(all_fields_names).difference(set(exempt))
        print(['fields_names', fields_names])

        for field_name in fields_names:
            if hasattr(self, field_name):
                value = getattr(self, field_name)
                if value is None or value == '':
                    return False
        return True
