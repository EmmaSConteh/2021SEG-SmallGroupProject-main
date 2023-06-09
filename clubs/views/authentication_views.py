import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from clubs.forms import LogInForm, SignUpForm, EditProfileForm, PasswordForm, CreateClubForm, CreateTournamentForm
from clubs.models import User, ClubMembership, Club, Application, Tournament
from clubs.helpers import login_prohibited
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from clubs.views.mixins import LoginProhibitedMixin


# class LoginProhibitedMixin:
#     """Mixin that redirects when a user is logged in """
#
#     redirect_when_logged_in_url = None
#
#     def dispatch(self, *args, **kwargs):
#         """Redirect when logged in, or dispatch as normal otherwise"""
#         if self.request.user.is_authenticated:
#             return self.handle_already_logged_in(*args, **kwargs)
#         return super().dispatch(*args, **kwargs)
#
#     def handle_already_logged_in(self, *args, **kwargs):
#         url = self.get_redirect_when_logged_in_url()
#         return redirect(url)
#
#     def get_redirect_when_logged_in_url(self):
#         """Returns the url to redirect to when not logged in"""
#         if self.redirect_when_logged_in_url is None:
#             raise ImproperlyConfigured(
#                 "LoginProhibitedMixin requires either a value for "
#                 "'redirect_when_logged_in_url', or an implementation for"
#                 "'get_redirect_when_logged_in_url()'."
#             )
#         else:
#             return self.redirect_when_logged_in_url
#

class LogInView(LoginProhibitedMixin, View):
    """View that handles log in """

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = 'home'

    @method_decorator(login_prohibited)
    def dispatch(self, request):
        return super().dispatch(request)

    def get(self, request):
        """Display log in template"""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt"""
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in templaate with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    logout(request)
    return redirect('index')
