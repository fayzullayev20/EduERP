from django.contrib import admin
from .models import StudentPayment, TeacherSalary


@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'month', 'calculated_amount', 'paid_amount', 'status')
    list_filter = ('status', 'month', 'group')
    search_fields = ('student__first_name', 'student__last_name')


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'group', 'month', 'calculated_salary', 'paid_amount', 'status')
    list_filter = ('status', 'month', 'group')
    search_fields = ('teacher__first_name', 'teacher__last_name')