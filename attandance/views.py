# attendance/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendance, AttendanceRecord
from .serializers import (
    AttendanceSerializer,
    AttendanceCreateSerializer,
    AttendanceRecordSerializer,
)


class AttendancesView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all().order_by("-date")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AttendanceCreateSerializer
        return AttendanceSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        group_id = self.request.query_params.get("group")
        if group_id:
            qs = qs.filter(group_id=group_id)
        return qs


class AttendanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceRecordsView(APIView):
    def get(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceRecordSerializer(attendance.records.all(), many=True)
        return Response(serializer.data)


class AttendanceMarkView(APIView):
    def post(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        student_id = request.data.get("student")
        status_value = request.data.get("status")

        if student_id is None or status_value is None:
            return Response(
                {"error": "student va status majburiy"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record, _ = AttendanceRecord.objects.update_or_create(
            attendance=attendance,
            student_id=student_id,
            defaults={"status": status_value},
        )
        serializer = AttendanceRecordSerializer(record)
        return Response(serializer.data)


class AttendanceRecordsListView(generics.ListCreateAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        attendance_id = self.request.query_params.get("attendance")
        if attendance_id:
            qs = qs.filter(attendance_id=attendance_id)
        return qs


class AttendanceRecordView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer