from django.db import models
from django.conf import settings
from students.models import Student


class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('bank_transfer', 'Bank o\'tkazmasi'),
    )

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='transactions'
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS, 
        default='cash'
    )
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_transactions'
    )

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Payment(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='payment'
    )
    month_for = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.month_for}"


class StudentPayment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'langan'),
        ('cancelled', 'Bekor qilingan'),
    )

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='student_payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.status})"


class TeacherSalary(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'langan'),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='teacher_salaries'
    )
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='teacher_salary'
    )
    for_month = models.DateField()
    calculated_salary = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher} - {self.for_month}"