from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    groups_details = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'frozen_at', 'archived_at', 'created_at', 'updated_at')

    def get_groups_details(self, obj):
        return [{'id': str(g.id), 'name': getattr(g, 'name', str(g))} for g in obj.groups.all()]


class BalanceTopUpSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1, help_text="To'ldiriladigan summa")


class GroupActionSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(help_text="Guruh ID si")


class GroupTransferSerializer(serializers.Serializer):
    from_group_id = serializers.UUIDField(required=True)
    to_group_id = serializers.UUIDField(required=True)