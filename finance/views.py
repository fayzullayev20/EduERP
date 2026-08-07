from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Category, Transaction, Payment, StudentPayment, TeacherSalary
from .serializers import (
    CategorySerializer,
    TransactionSerializer,
    PaymentSerializer,
    StudentPaymentSerializer,
    TeacherSalarySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().select_related('category', 'created_by')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class StudentPaymentViewSet(viewsets.ModelViewSet):
    queryset = StudentPayment.objects.all().select_related('student')
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAuthenticated]


class TeacherSalaryViewSet(viewsets.ModelViewSet):
    queryset = TeacherSalary.objects.all().select_related('teacher', 'transaction')
    serializer_class = TeacherSalarySerializer
    permission_classes = [IsAuthenticated]