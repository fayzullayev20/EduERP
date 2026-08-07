from django.contrib import admin
<<<<<<< HEAD
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
=======

# Register your models here.
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
