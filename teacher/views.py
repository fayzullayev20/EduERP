from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from .models import Teacher, Subject, TeacherWorkload, Transaction, Contract, HomeWork, StudentGamification
from .serializers import (
    TeacherSerializer,
    SubjectSerializer,
    TeacherWorkloadSerializer,
    TransactionSerializer,
    ContractSerializer,
    HomeWorkSerializer,
    StudentGamificationSerializer,
)
from .permissions import (
    IsOwnerOrReadOnlyForStaff,
    IsRelatedTeacherOwner,
    TeacherScopedQuerysetMixin,
)


class TeachersView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Teacher.objects.filter(owner=self.request.user).exists():
            raise ValidationError(
                {"detail": "Sizda allaqachon teacher profili mavjud."}
            )
        serializer.save(owner=self.request.user)


class TeacherView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyForStaff]


class MyTeacherProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Teacher.objects.get(owner=self.request.user)
        except Teacher.DoesNotExist:
            raise NotFound("Sizga tegishli teacher profili topilmadi")


class SubjectsView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class SubjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class TeacherWorkloadsView(TeacherScopedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = TeacherWorkloadSerializer
    permission_classes = [IsAuthenticated]
    teacher_lookup = "teacher_id"

    def get_queryset(self):
        qs = self.scope_to_teacher(TeacherWorkload.objects.all())
        teacher_id = self.request.query_params.get("teacher")
        if teacher_id:
            qs = qs.filter(teacher_id=teacher_id)
        return qs


class TeacherWorkloadView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherWorkload.objects.all()
    serializer_class = TeacherWorkloadSerializer
    teacher_lookup = "teacher_id"
    permission_classes = [IsAuthenticated, IsRelatedTeacherOwner]


class TransactionsView(TeacherScopedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    teacher_lookup = "teacher_id"

    def get_queryset(self):
        qs = self.scope_to_teacher(Transaction.objects.all().order_by("-date_added"))
        teacher_id = self.request.query_params.get("teacher")
        if teacher_id:
            qs = qs.filter(teacher_id=teacher_id)
        return qs


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    teacher_lookup = "teacher_id"
    permission_classes = [IsAuthenticated, IsRelatedTeacherOwner]


class ContractsView(TeacherScopedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    teacher_lookup = "teacher_id"

    def get_queryset(self):
        qs = self.scope_to_teacher(Contract.objects.all())
        teacher_id = self.request.query_params.get("teacher")
        if teacher_id:
            qs = qs.filter(teacher_id=teacher_id)
        return qs


class ContractView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    teacher_lookup = "teacher_id"
    permission_classes = [IsAuthenticated, IsRelatedTeacherOwner]


class HomeWorksView(TeacherScopedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = HomeWorkSerializer
    permission_classes = [IsAuthenticated]
    teacher_lookup = "lesson__group__workloads__teacher_id"

    def get_queryset(self):
        qs = self.scope_to_teacher(HomeWork.objects.all().order_by("-created_at"))
        qs = qs.distinct()  # workloads orqali join bo'lgani uchun takrorlanishning oldini olamiz
        lesson_id = self.request.query_params.get("lesson")
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)
        return qs

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get("lesson")
        if not self.request.user.is_staff:
            own_teacher = Teacher.objects.filter(owner=self.request.user).first()
            group = getattr(lesson, "group", None)
            has_workload = (
                own_teacher is not None
                and group is not None
                and TeacherWorkload.objects.filter(teacher=own_teacher, group=group).exists()
            )
            if not has_workload:
                raise PermissionDenied("Faqat o'z darsingiz uchun uy vazifa qo'sha olasiz")
        serializer.save()


class HomeWorkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer
    permission_classes = [IsAuthenticated, IsRelatedTeacherOwner]
    teacher_lookup = "lesson__group__workloads__teacher_id"

    def perform_update(self, serializer):
        new_lesson = serializer.validated_data.get("lesson")
        if new_lesson is not None and not self.request.user.is_staff:
            own_teacher = Teacher.objects.filter(owner=self.request.user).first()
            group = getattr(new_lesson, "group", None)
            has_workload = (
                own_teacher is not None
                and group is not None
                and TeacherWorkload.objects.filter(teacher=own_teacher, group=group).exists()
            )
            if not has_workload:
                raise PermissionDenied("Faqat o'z darsingizga tegishli qilib o'zgartira olasiz")
        serializer.save()


class StudentGamificationsView(generics.ListCreateAPIView):
    serializer_class = StudentGamificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = StudentGamification.objects.all()
        student_id = self.request.query_params.get("student")
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs


class StudentGamificationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentGamification.objects.all()
    serializer_class = StudentGamificationSerializer
    permission_classes = [IsAuthenticated]