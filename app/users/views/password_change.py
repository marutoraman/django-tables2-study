from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    '''
    パスワード変更ビュー
    '''
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'registration/password_change.html'

