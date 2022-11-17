from django.conf import settings

import factory.fuzzy
from factory.django import DjangoModelFactory

from ..models import Account
from core.base.enums import AccountNetwork


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Sequence(lambda n: "title#%d" % n)
    network = factory.Iterator(AccountNetwork)
    active = True
    user = factory.SubFactory(settings.AUTH_USER_MODEL)

    class Params:
        inactive = factory.Trait(
            active=False
        )
