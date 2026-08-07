from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
<<<<<<< HEAD
from django.utils import timezone
from django.db import transaction

from common.permissions import IsAdmin, IsSuperUser, IsTeacher
from .models import Student, StudentStatus
from .serializers import (
    StudentSerializer, 
    BalanceTopUpSerializer, 
    GroupActionSerializer,
    GroupTransferSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'passport_number']
    ordering_fields = ['created_at', 'balance', 'first_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'dashboard']:
            permission_classes = [IsAdmin | IsSuperUser | IsTeacher]
        else:
            permission_classes = [IsAdmin | IsSuperUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        student = self.get_object()
        
        attendance_records = getattr(student, 'attendancerecord_set', None)
        if attendance_records:
            total_lessons = attendance_records.count()
            attended_lessons = attendance_records.filter(is_present=True).count()
        else:
            total_lessons = 0
            attended_lessons = 0

        attendance_rate = (attended_lessons / total_lessons * 100) if total_lessons > 0 else 0

        return Response({
            'id': student.id,
            'full_name': f"{student.first_name} {student.last_name}",
            'phone_number': student.phone_number,
            'balance': student.balance,
            'status': student.status,
            'groups': [{'id': str(g.id), 'name': getattr(g, 'name', str(g))} for g in student.groups.all()],
            'attendance': {
                'total_lessons': total_lessons,
                'attended_lessons': attended_lessons,
                'missed_lessons': total_lessons - attended_lessons,
                'rate_percentage': f"{round(attendance_rate, 1)}%"
            },
            'owner': student.owner.username if student.owner else None,
            'created_at': student.created_at
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        student = self.get_object()
        student.status = StudentStatus.FROZEN
        student.frozen_at = timezone.now()
        student.save()
        return Response({'detail': f"{student.first_name} {student.last_name} muzlatildi."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfreeze(self, request, pk=None):
        student = self.get_object()
        student.status = StudentStatus.ACTIVE
        student.frozen_at = None
        student.save()
        return Response({'detail': f"{student.first_name} {student.last_name} faollashtirildi."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        student = self.get_object()
        student.status = StudentStatus.ARCHIVED
        student.archived_at = timezone.now()
        student.save()
        return Response({'detail': f"{student.first_name} {student.last_name} arxivlandi."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=BalanceTopUpSerializer)
    def top_up_balance(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        
        student = self.get_object()
        with transaction.atomic():
            student.balance += amount
            student.save()
        
        return Response({
            'detail': f"Balans {amount} so'mga to'ldirildi.",
            'new_balance': student.balance
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=GroupActionSerializer)
    def add_group(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = self.get_object()
        student.groups.add(serializer.validated_data['group_id'])
        return Response({'detail': "Talaba guruhga qo'shildi."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=GroupActionSerializer)
    def remove_group(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = self.get_object()
        student.groups.remove(serializer.validated_data['group_id'])
        return Response({'detail': "Talaba guruhdan chiqarildi."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=GroupTransferSerializer)
    def transfer_group(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from_group_id = serializer.validated_data['from_group_id']
        to_group_id = serializer.validated_data['to_group_id']
        
        student = self.get_object()
        with transaction.atomic():
            student.groups.remove(from_group_id)
            student.groups.add(to_group_id)
            
        return Response({'detail': "Talaba yangi guruhga ko'chirildi."}, status=status.HTTP_200_OK)
=======
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin, IsTeacher, IsStudent
from .models import Student
from .serializers import StudentSerializer, StudentCreateUpdateSerializer, TransferStudentSerializer
from .services import StudentService



def custom_response(data=None, message="", success=True, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data if data is not None else {}
    }, status=status_code)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['first_name', 'last_name', 'phone_number', 'passport_number']

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'role', None) == 'student':
            return Student.objects.filter(owner=self.request.user)

        return Student.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, (IsAdmin | IsTeacher | IsStudent)]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        return StudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True) # <-- Bu yerda 'page' bo'lishi kerak
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return custom_response(data=serializer.data, message="Talabalar ro'yxati")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return custom_response(
            data=StudentSerializer(student).data,
            message="Talaba muvaffaqiyatli yaratildi",
            status_code=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], url_path='freeze')
    def freeze(self, request, pk=None):
        student = self.get_object()
        update_student = StudentService.freeze_student(student)
        return custom_response(
            data=StudentSerializer(update_student).data,
            message="Talaba muzlatildi."
        )

    @action(detail=True, methods=['post'], url_path='unfreeze')
    def unfreeze(self, request, pk=None):
        student = self.get_object()
        updated_student = StudentService.unfreeze_student(student)
        return custom_response(
            data=StudentSerializer(updated_student).data,
            message="Talaba aktivlashtirildi."
        )

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        student = self.get_object()
        updated_student = StudentService.archive_student(student)
        return custom_response(
            data=StudentSerializer(updated_student).data,
            message="Talaba arxivga o'tkazildi."
        )
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
