from rest_framework import serializers
from .models import StudentPayment, TeacherSalary


class StudentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPayment
        fields = '__all__'
        read_only_fields = ('calculated_amount', 'status', 'created_at', 'updated_at')


class TeacherSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalary
        fields = '__all__'
        read_only_fields = ('calculated_salary', 'status', 'created_at', 'updated_at')