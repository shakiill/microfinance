from django.contrib import admin

from apps.user.models import Staff, Customer, CustomUser, OtpToken


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(OtpToken)
