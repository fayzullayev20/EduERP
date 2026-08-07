from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StudentPayment, TeacherSalary
from .serializers import StudentPaymentSerializer, TeacherSalarySerializer


class StudentPaymentViewSet(viewsets.ModelViewSet):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    permission_classes = [IsAuthenticated]


class TeacherSalaryViewSet(viewsets.ModelViewSet):
    queryset = TeacherSalary.objects.all()
    serializer_class = TeacherSalarySerializer
    permission_classes = [IsAuthenticated]