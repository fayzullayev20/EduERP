from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "owner",
            "amount",
            "salary_type",
        ]
        read_only_fields = ["owner"]