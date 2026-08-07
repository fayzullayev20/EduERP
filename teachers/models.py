from django.db import models
from django.conf import settings
import uuid

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='teacher_profile'
    )
    specialty = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    salary_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.specialty})"