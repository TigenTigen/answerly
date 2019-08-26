from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from user.forms import CustomUserCreationForm
from user.models import AdvUser, signer

class RegictrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user:registration_done')

class RegictrationDoneView(TemplateView):
    template_name = 'registration/registration_done.html'

def registration_confirmation(request, sign):
    try:
        username = signer.unsign(sign)
        user = get_object_or_404(AdvUser, username=username)
        user.confirm()
        success = True
    except:
        success = False
    return render(request, 'registration/registration_confirmed.html', context={'success': success})

class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'registration/profile.html'

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('user:password_change_done')

class CustomPasswordResetView(PasswordResetView):
    #template_name = 'registration/password_reset_form.html'
    subject_template_name = 'emails/password_reset_subject.txt'
    email_template_name = 'emails/password_reset_email.txt'
    html_email_template_name = 'emails/password_reset_email.html'
    success_url = '/accounts/password_reset/done/' # path_name
    #form_class = django.contrib.auth.forms.PasswordResetForm
    #extra_context = {}
    #extra_email_context = {}
    #default context includes parameters form, title + extra_context
    #default email context includes: protocol, domain, uid, token, email, user
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    #template_name = 'registration/password_reset_confirm.html'
    #post_reset_login = False #  если True - пользовтель будет автоматически залогинен, False - произойдет перенаправление на форму входа
    success_url = '/accounts/password_reset/complete/' # path_name
    #extra_context = {}
    #form_class = django.contrib.auth.forms.SetResetForm
    #default_context includes parameters title, form, validlink + extra_context
    pass
