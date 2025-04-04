from django.contrib import admin
from .models import EmailVerificationEvent, Email


admin.site.register(Email)
@admin.register(EmailVerificationEvent)
class EmailVerificationEventAdmin(admin.ModelAdmin):
    list_display = ['email', 'token', 'attempts', 'expired', 'timestamp']
    fields = ['email', 'token', 'attempts', 'last_attempt_at', 'expired', 'expired_at', 'timestamp']
    readonly_fields = ['token', 'timestamp']
