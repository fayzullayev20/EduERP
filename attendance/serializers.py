from rest_framework import serializers
from .models import Attendance, AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ["id", "attendance", "student", "student_name", "status"]

    def get_student_name(self, obj):
        student = obj.student
        return f"{student.first_name} {student.last_name}"


class AttendanceSerializer(serializers.ModelSerializer):
    records = AttendanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "date", "group", "records"]


class AttendanceCreateSerializer(serializers.ModelSerializer):
    records = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Attendance
        fields = ["id", "date", "group", "records"]

    def create(self, validated_data):
        records_data = validated_data.pop("records", [])
        attendance = Attendance.objects.create(**validated_data)
        for r in records_data:
            AttendanceRecord.objects.create(
                attendance=attendance,
                student_id=r["student"],
                status=r["status"],
            )
        return attendance