from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import Teacher
from .serializers import TeacherSerializer


class TeachersView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeacherView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class MyTeacherProfileView(generics.RetrieveUpdateAPIView):
    """Tizimga kirgan o'qituvchi o'zining profilini ko'radi/yangilaydi"""
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Teacher.objects.get(owner=self.request.user)
        except Teacher.DoesNotExist:
            raise NotFound("Sizga tegishli teacher profili topilmadi")