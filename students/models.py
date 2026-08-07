import uuid
from django.db import models
<<<<<<< HEAD
=======
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


User = get_user_model()
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1


class StudentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    FROZEN = 'FROZEN', 'Frozen'
    ARCHIVED = 'ARCHIVED', 'Archived'


<<<<<<< HEAD
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    
    groups = models.ManyToManyField('groups.Group', related_name='enrolled_students', blank=True)
    status = models.CharField(
        max_length=50,
        choices=StudentStatus.choices,
        default=StudentStatus.ACTIVE
    )
    balance = models.BigIntegerField(default=0)
    
    frozen_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_students'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
=======
phone_validator = RegexValidator(regex=r'^\+998\d{9}$', message="Format: +998901234567")


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_regax = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True)
    passport_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, unique=True)
    # groups = models.ManyToManyField('Group', related_name='students', blank=True)
    status = models.CharField(
        max_length=20, 
        choices=StudentStatus.choices, 
        default=StudentStatus.ACTIVE
    )
    balance = models.BigIntegerField(default=0)
    frozen_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_profile')
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"