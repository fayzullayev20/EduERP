from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'date_start',
            'date_end',
            'price',
            'days',
            'time_start',
            'time_end',
            'status',
            'room',
            'max_student',
            'teacher',
            'students',
            'students_count',
        ]

    def validate(self, data):
  
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        if date_start and date_end and date_start >= date_end:
            raise serializers.ValidationError({"date_end": "Tugash sanasi boshlanish sanasidan keyin bo'lishi shart."})

        time_start = data.get('time_start')
        time_end = data.get('time_end')
        if time_start and time_end and time_start >= time_end:
            raise serializers.ValidationError({"time_end": "Tugash vaqti boshlanish vaqtidan keyin bo'lishi shart."})

        return data

class AssignTeacherSerializer(serializers.Serializer):
    teacher_id = serializers.UUIDField()

class AddStudentSerializer(serializers.Serializer):
    student_id = serializers.UUIDField()