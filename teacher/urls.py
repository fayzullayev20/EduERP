from django.urls import path

from .views import TeachersView, TeacherView, MyTeacherProfileView

urlpatterns = [
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('teachers/<int:pk>/', TeacherView.as_view(), name='teacher'),
    path('teachers/me/', MyTeacherProfileView.as_view(), name='my-teacher-profile'),
]