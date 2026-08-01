from rest_framework import serializers
from .models import Teacher, Subject, TeacherWorkload, Transaction, Contract


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subjects",
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "owner",
            "subjects",
            "subject_ids",
            "amount",
            "salary_type",
        ]
        read_only_fields = ["owner"]


class TeacherWorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherWorkload
        fields = ["id", "teacher", "group", "hours_per_week", "created_at"]
        read_only_fields = ["created_at"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "teacher", "transaction_type", "comment", "amount", "date_added"]
        read_only_fields = ["date_added"]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["id", "teacher", "number", "start_date", "end_date", "file", "is_active", "created_at"]
        read_only_fields = ["created_at"]