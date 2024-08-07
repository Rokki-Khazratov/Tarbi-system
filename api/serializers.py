from rest_framework import serializers
from .models import *

class MonthArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthArchive
        fields = [
            'year', 'month_name', 'kid', 'missed_days', 'tarif', 'left_sum', 
            'missday_count', 'missday_cost', 'is_paid'
        ]

class KidSerializer(serializers.ModelSerializer):
    month_archives = MonthArchiveSerializer(many=True, read_only=True)

    class Meta:
        model = Kid
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth', 'gender', 'month_archives'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'
