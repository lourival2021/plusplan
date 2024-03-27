from django.contrib.auth.models import AbstractUser, Group,Permission
from django.db import models
from cadastros.models import Empresa

class CustomUser(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios_da_empresa',blank=True, null=True)

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        help_text='Specific permissions for this user.',
    )