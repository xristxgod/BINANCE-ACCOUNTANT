from rest_framework.generics import GenericAPIView

from ..models import Account


class Accounts(GenericAPIView):
    authentication_classes = ()
