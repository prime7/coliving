from django.db import models

import config.easypost as ep
import easypost

easypost.api_key = ep.EASYPOST_KEY


def verify_address(street1, zip, city, street2=None):
    address = easypost.Address.create(
        verify=["delivery"],
        street1=street1,
        street2=street2,
        zip=zip,
        city=city,
        country="Canada",
    )

    return address.verifications["delivery"]


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
