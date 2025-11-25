from django.contrib import admin
from .models import User, Account, Budget, Notification, Transaction

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Budget)
admin.site.register(Notification)
admin.site.register(Transaction)
