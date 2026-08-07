from django.db import models
from decimal import Decimal


class StudentPayment(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'To\'lanmagan'),
        ('partial', 'Qisman to\'langan'),
        ('paid', 'To\'liq to\'langan'),
    )

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='student_payments')
    month = models.DateField(help_text="To'lov oyi (masalan, 2026-08-01)")
    
    course_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="12 darslik to'liq kurs narxi")
    total_lessons = models.PositiveIntegerField(default=12, help_text="Bir oydagi rejalashtirilgan standart darslar soni")
    attended_lessons = models.PositiveIntegerField(default=0, help_text="Talaba amalda qatnashgan darslar soni")
    
    calculated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Davomatga ko'ra hisoblangan summa")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Talaba amalda to'lagan summa")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'group', 'month')

    def calculate_amount(self):
        if self.total_lessons > 0:
            one_lesson_price = Decimal(self.course_price) / Decimal(self.total_lessons)
            return round(one_lesson_price * Decimal(self.attended_lessons), 2)
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        self.calculated_amount = self.calculate_amount()
        
        if self.paid_amount >= self.calculated_amount and self.calculated_amount > 0:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.group.name} ({self.month.strftime('%Y-%m')})"


class TeacherSalary(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'langan'),
    )

    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE, related_name='salaries')
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='teacher_salaries')
    month = models.DateField(help_text="Maosh oyi (masalan, 2026-08-01)")
    
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, help_text="12 dars o'tilganda beriladigan to'liq oylik")
    total_lessons = models.PositiveIntegerField(default=12, help_text="Bir oydagi rejalashtirilgan darslar soni")
    conducted_lessons = models.PositiveIntegerField(default=0, help_text="O'qituvchi amalda o'tgan darslar soni")
    
    calculated_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="O'tilgan darslarga ko'ra hisoblangan maosh")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('teacher', 'group', 'month')

    def calculate_salary(self):
        if self.total_lessons > 0:
            one_lesson_rate = Decimal(self.base_salary) / Decimal(self.total_lessons)
            return round(one_lesson_rate * Decimal(self.conducted_lessons), 2)
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        self.calculated_salary = self.calculate_salary()
        
        if self.paid_amount >= self.calculated_salary and self.calculated_salary > 0:
            self.status = 'paid'
        else:
            self.status = 'pending'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher} - {self.group.name} ({self.month.strftime('%Y-%m')})"