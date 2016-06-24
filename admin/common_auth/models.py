from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def prereg_users(self):
        return self.filter(groups__name='prereg_group')


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    osf_id = models.CharField(max_length=5, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return ('{0} {1}'.format(self.first_name, self.last_name)).strip() or self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    class Meta:
        ordering = ['email']

    @property
    def osf_user(self):
        # import on call to avoid interference w/ django's manage.py commands like collectstatic
        from website.models import User as OsfUserModel

        if not self.osf_id:
            raise RuntimeError('This user does not have an associated Osf User')
        return OsfUserModel.load(self.osf_id)

    def is_in_group(self, group):
        return self.groups.filter(name=group).exists()

    def group_names(self):
        return self.groups.all().values_list('name', flat=True)
