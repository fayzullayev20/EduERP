from rest_framework import serializers
<<<<<<< HEAD
=======

>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
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
=======
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'owner', 'first_name', 'last_name',
            'phone_number', 'passport_number', 'status', 'balance',
            'frozen_at', 'archived_at',
        ]
        read_only_fields = ['status', 'balance', 'frozen_at', 'archived_at']


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['owner', 'first_name', 'last_name', 'phone_number', 'passport_number', 'groups']


class TransferStudentSerializer(serializers.Serializer):
    current_group_id = serializers.IntegerField()
    target_group_id = serializers.IntegerField()
>>>>>>> fe439967a4c9f5b0fe6a6889a838d7af247ac1c1
