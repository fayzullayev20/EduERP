from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teachers"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class SalaryType(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        BIWEEKLY = "biweekly", "Biweekly (2 marta oyiga)"
        HOURLY = "hourly", "Hourly"
        PER_LESSON = "per_lesson", "Per Lesson"

    salary_type = models.CharField(
        max_length=20,
        choices=SalaryType.choices,
        default=SalaryType.MONTHLY
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"