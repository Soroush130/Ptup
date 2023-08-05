from django.contrib.auth.admin import UserAdmin
from .models import User, SiteRules, OtpCode
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['__str__', 'phone', 'role', 'is_otp_code_verify', 'is_active', 'is_staff']
    list_filter = ['phone', 'role', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Inoframtion', {'fields': ('role', 'is_otp_code_verify', 'is_accept_rules')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('phone', 'role', 'password1', 'password2', 'is_staff')
            }
        ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)

admin.site.register(SiteRules)


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['otp_code', 'phone', 'is_valid', 'created']


admin.site.register(OtpCode, OtpCodeAdmin)
