from django.contrib import admin
from .models import Category, Transaction, Payment, StudentPayment, TeacherSalary


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'category', 'payment_method', 'date', 'created_by')
    list_filter = ('payment_method', 'category__type', 'date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'month_for', 'transaction')


@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'calculated_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'for_month', 'calculated_salary', 'status', 'created_at')
    list_filter = ('status', 'for_month', 'created_at')