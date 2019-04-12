from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, **extra_fields):
        """Create and save a user with the given email."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, **extra_fields)


class AbstractEmailUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(_('email address'), unique=True, db_index=True)
    username = None
    password = None

    def has_usable_password(self):
        return False

    objects = EmailUserManager()

    class Meta(AbstractUser.Meta):
        abstract = True


class EmailUser(AbstractEmailUser):
    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
