from typing import Any, Optional

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        username: str,
        password: Optional[str] = None
    ) -> Any:
        if not email:
            raise ValueError('Email is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        assert isinstance(user, User)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        password: Optional[str] = None
    ) -> Any:
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    username = models.CharField(
        max_length=10,
        blank=False,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
