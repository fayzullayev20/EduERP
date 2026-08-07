from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import StudentPaymentViewSet, TeacherSalaryViewSet

router = DefaultRouter()
router.register(r'student-payments', StudentPaymentViewSet)
router.register(r'teacher-salaries', TeacherSalaryViewSet)
=======

from .views import TransactionViewSet, PaymentViewSet, TeacherSalaryViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'teacher-salaries', TeacherSalaryViewSet, basename='teachersalary')
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1

urlpatterns = [
    path('', include(router.urls)),
]