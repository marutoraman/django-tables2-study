from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    '''
    パスワード変更完了画面
    '''
    template_name = 'registration/password_change_done.html'
