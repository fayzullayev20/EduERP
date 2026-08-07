from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentPaymentViewSet, TeacherSalaryViewSet

router = DefaultRouter()
router.register(r'student-payments', StudentPaymentViewSet)
router.register(r'teacher-salaries', TeacherSalaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]