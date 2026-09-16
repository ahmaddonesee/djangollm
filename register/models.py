from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )

        user.is_superuser = False
        # user.is_staff = True
        user.is_admin = True

        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


























# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user = self.create_user(
#             email,
#             password=password,
#             username=username,
#         )
#         user.is_superuser = False
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class MyUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name="email address",
#         max_length=255,
#         unique=True,
#     )
#     # date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
    

#     objects = CustomUserManager()

#     USERNAME_FIELD = "email"
#     # # REQUIRED_FIELDS = ["date_of_birth"]
    
#     REQUIRED_FIELDS = ["username"]

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin