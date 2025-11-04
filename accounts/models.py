from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ========== ROLES Y PERMISOS ==========
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField('Permission', blank=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ========== MANAGER ==========
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

# ========== CUSTOM USER ==========
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=150, unique=True)
    lastname = models.CharField(max_length=100, blank=True) 
    country = models.CharField(max_length=100, blank=True)    #  nuevo

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    fcm_token = models.TextField(null=True, blank=True)  #  para guardar el token
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def __str__(self):
    #     return self.username
    def is_admin(self):
        return self.role and self.role.name == "Admin"
    

