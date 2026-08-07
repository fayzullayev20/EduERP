from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TransactionViewSet,
    StudentPaymentViewSet,
    TeacherSalaryViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'student-payments', StudentPaymentViewSet, basename='student-payment')
router.register(r'teacher-salaries', TeacherSalaryViewSet, basename='teacher-salary')

urlpatterns = [
    path('', include(router.urls)),
]