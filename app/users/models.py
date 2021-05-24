from config.const import SELECTION
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
import uuid as uuid_lib


class YahooAccount(models.Model):
    yahoo_account_id = models.CharField(_('ヤフオクアカウント'), max_length=50, blank=True)
    yahoo_pass = models.CharField(_('ヤフオクパスワード'), max_length=20, blank=True)
    def __str__(self):
        return self.yahoo_account_id

    class Meta:
        verbose_name = _('ヤフオクアカウント')
        verbose_name_plural = _('ヤフオクアカウント')

class UserManager(UserManager):
    '''
    カスタムUserモデルを作成したため、UserManagerもオーバーライドする
    '''    
    def _create_user(self, account_id, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not account_id:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        account_id = self.model.normalize_username(account_id)
        user = self.model(account_id=account_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, account_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(account_id, email, password, **extra_fields)
    
    def create_superuser(self, account_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(account_id, email, password, **extra_fields)
    
    # 各種初期設定を作成
    def init_settings(self, account_id):
        pass
    
class User(AbstractBaseUser, PermissionsMixin):
    """　
    カスタムUserモデル
    """
    uuid = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    account_id = models.CharField(
        _('アカウントID'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that account_id already exists."),
        },
    )
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    account_count=models.IntegerField(_('最大アカウント数'),blank=True,null=True)
    yahoo_account_id = models.ManyToManyField(
        YahooAccount,
        verbose_name=_('ヤフオクアカウント'),
        blank=True,
        help_text=_('ヤフオクアカウントを登録'),
        related_name="user_set",
        related_query_name="user",
    )
    plan = models.CharField(_('プラン'), max_length=20, choices=SELECTION.PLAN,default=SELECTION.PLAN[0][0])
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    begin_crawle_at = models.DateTimeField(_('クロール開始日時'), null=True)
    crawled_at = models.DateTimeField(_('最終クロール日時'), null=True)
    is_crawle = models.BooleanField(_('is_crawle'), null=True)
    syuppin_mode_at = models.DateTimeField(_('最終出品モード起動日時'), null=True)
    torihiki_mode_at = models.DateTimeField(_('最終取引モード起動日時'), null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'account_id'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 既存メソッドの変更
    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
    

