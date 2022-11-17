from django.contrib import admin

from .models import Account
from .models import Google2FA
from .models import Telegram


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'active', 'user')
    list_filter = ('network', 'active', 'user')


admin.site.register(Account, AccountAdmin)
