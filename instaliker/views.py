from django.conf import settings

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from django.utils import translation
from django.utils.translation import gettext as _

from django.contrib.auth import views as auth_views
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView, RedirectView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from .forms import RegisterForm


    
#################################### Manage Account ####################################

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('instagram:login')

class PasswordChangeFormView(auth_views.PasswordChangeView):
    def get_success_url(self) :
        messages.success(self.request, _("Password's been changed successfully!"))
        return reverse_lazy('instagram:login')

class PasswordResetFormView(auth_views.PasswordResetView):
    def get_success_url(self) :
        messages.success(self.request, _("We've emailed you instructions for setting your password. You should receive the email shortly!"))
        return reverse_lazy('instagram:password_reset')

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def get_success_url(self):
        messages.success(self.request, _("Password's been changed successfully, try to login"))
        return reverse_lazy('instagram:login') 

#################################### Main Views ####################################

class HomeView(TemplateView):
    template_name = 'instagram/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        context['greeting'] = _("Welcome to App Manager")
        return context

def privacy(request):
    return render(request, 'instagram/privacy.html')
def terms(request):
    return render(request, 'instagram/privacy.html')

class FacebookCallbackView(View):
    def get(self, request, *args, **kwargs):
        # Process the callback from Facebook
        # You might use the social-auth library to handle this
        try:
            # This assumes you're using the social-auth app
            user = request.user  # Get the user
            # Handle user login or registration
            return redirect('instagram:home')  # Redirect to home after login
        except Exception:
            return redirect('instagram:login')  # Handle any error

class LoginSuccessView(View):
    def get(self, request, *args, **kwargs):
        messages.success(self.request, _("login with FB successfully"))

        return HttpResponseRedirect(reverse('instagram:home'))
    
class LoginErrorView(View):
    def get(self, request, *args, **kwargs):
        messages.error(self.request, _("Error login with FB"))
        return HttpResponseRedirect(reverse('instagram:login'))
