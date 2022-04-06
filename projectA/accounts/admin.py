from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name','phone_number','is_admin')
    list_filter = ('is_admin',)

    fieldsets = ( #for UserChangeForm
        (None, {'fields':('full_name','phone_number','password')}),
        ('Permissions',{'fields':('is_active','is_admin','last_login')}),
    )

    add_fieldsets = ( # for userCreationForm
        (None,{'fields':('phone_number','full_name','password1','password2')}),
    )

    search_fields = ('full_name','phone_number')
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)