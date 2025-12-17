from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('TENANT', 'Tenant'),
        ('MANAGER', 'Property Manager'),
        ('ADMIN', 'Administrator'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TENANT')
    phone = models.CharField(max_length=20, blank=True, default='')
    unit = models.CharField(max_length=100, blank=True, default='')  # e.g., Apartment/House label

    def is_tenant(self): return self.role == 'TENANT'
    def is_manager(self): return self.role == 'MANAGER'
    def is_admin(self): return self.role == 'ADMIN'