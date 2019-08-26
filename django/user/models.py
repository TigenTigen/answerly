from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.signing import Signer
from django.template import engines, Context
from django.urls import reverse
from django.db.models import Count

signer = Signer()
dt_engine = engines['django'].engine

# Данная sмодель заменит модель пользователя User, используемую по умолчанию.
# Данная замена должна быть отражена в настройках проекта: AUTH_USER_MODEL = 'user.models.AdvUser'.
# Замен производится с целью расширения стандартной модели с помощью дополнительных методов и атрибутов.

class AdvUser(AbstractUser):
    #objects = AdvUserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи (расширенная модель)'
        ordering = ['-date_joined']
        unique_together = ['email']

    def __str__(self):
        return self.username

    def confirm(self):
        self.is_active = True
        self.save()

    def get_email_context(self):
        host = settings.HOST_NAME
        sign = signer.sign(self.username)
        link = host + reverse('user:registration_confirmed', kwargs={'sign': sign})
        return Context({'confirmation_link': link})

    def send_confirmation_email(self):
        context = self.get_email_context()
        text_body = dt_engine.get_template('emails/registration_confirmation.txt').render(context=context)
        html_body = dt_engine.get_template('emails/registration_confirmation.html').render(context=context)
        self.email_user(subject='Answerly: Подтверждение регистрации', message=text_body, html_message=html_body)
