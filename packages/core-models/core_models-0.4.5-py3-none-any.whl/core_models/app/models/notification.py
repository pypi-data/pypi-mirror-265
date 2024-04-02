from django.db import models

from .company import Company
from .base import BaseModelAbstract
from ... import constants


class Notification(BaseModelAbstract, models.Model):
    company = models.ForeignKey(Company, models.CASCADE, null=True, blank=True)
    notice_type = models.CharField(max_length=50, null=False, blank=False)
    object_id = models.UUIDField(null=True, blank=True)
    seen = models.BooleanField(default=False)

    def __unicode__(self):
        email = self.created_by.email if self.created_by else '-'
        return f"Notification type: {self.notice_type} for: {email}"

    @property
    def object(self):
        from .profile_application import ProfileApplication
        from .contract import Contract
        from .invoice import Invoice
        maps = {
            constants.ADMIN_NEW_PROFILE_NOTIF_TYPE: ProfileApplication,
            constants.ADMIN_CONTRACT_DD_NOTIF_TYPE: Contract,
            constants.ADMIN_VAL_INVOICE_NOTIF_TYPE: Invoice,
        }
        if m := maps.get(self.notice_type):
            return m.objects.get(id=self.object_id)
        return None

    @property
    def text(self):
        for item in constants.NOTIFICATION_TYPES:
            if item[0] == self.notice_type:
                return item[1]
        return '-'

    @property
    def description(self):
        for item in constants.NOTIFICATION_TYPES:
            if item[0] == self.notice_type:
                return item[1]
        return '-'
