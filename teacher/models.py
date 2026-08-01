from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name="teachers",
        blank=True
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
        PER_LESSON = "per_lesson", "Per Lesson"

    salary_type = models.CharField(
        max_length=20,
        choices=SalaryType.choices,
        default=SalaryType.MONTHLY
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeacherWorkload(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="workloads"
    )
    group = models.ForeignKey(
        "group.Group",
        on_delete=models.CASCADE,
        related_name="workloads"
    )
    hours_per_week = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("teacher", "group")

    def __str__(self):
        return f"{self.teacher} - {self.group} ({self.hours_per_week} soat/hafta)"


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        SALARY = "salary", "Salary"
        BONUS = "bonus", "Bonus"
        PENALTY = "penalty", "Penalty"
        OTHER = "other", "Other"

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )
    comment = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.transaction_type} - {self.amount}"


class Contract(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to="contracts/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shartnoma #{self.number} - {self.teacher}"
    