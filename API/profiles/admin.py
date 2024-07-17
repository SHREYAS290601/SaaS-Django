from django.contrib import admin

# Register your models here.
from subscriptions.models import SubModel, UserSubscription

admin.site.register(SubModel)
admin.site.register(UserSubscription)
