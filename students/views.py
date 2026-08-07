from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
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