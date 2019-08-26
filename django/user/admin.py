from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count

USER_MODEL = get_user_model()

class UserAdmin(admin.ModelAdmin):
    # list settings
    list_display = ('id', 'username', 'email', 'is_active', 'date_joined')
    list_display_links = ('username',)
    search_fields = ('id', 'email', 'username')
    list_filter = ('is_active', 'date_joined',)
    date_hierarchy = 'date_joined'
    list_per_page = 20
    actions = ('resend_confirmation_emails',)

    # single form_page settings
    readonly_fields = ('is_active', 'password', 'date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fields(self, request, obj=None):
        fields = [
            ('username', 'email', 'is_active',),
            'password', 'first_name', 'last_name',
            ('is_staff', 'is_superuser',),
            ('date_joined', 'last_login'),
        ]
        if Group.objects.exists():
            fields.append('groups')
        return fields

    # actions
    def resend_confirmation_emails(self, request, queryset):
        email_count = 0
        for user in queryset:
            if not user.is_active:
                user.send_confirmation_email()
                email_count = email_count + 1
        message_text = 'В адрес неактивированных пользователей направлено {} писем о подтверждении регистрации'
        self.message_user(request, message_text.format(email_count))
    resend_confirmation_emails.short_description = 'Направить повторное письмо о подвтерждении регистрации'

admin.site.register(USER_MODEL, UserAdmin)
