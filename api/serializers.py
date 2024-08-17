from rest_framework import serializers
from .models import *

class MonthArchiveSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source='get_month_display', read_only=True)
    kid = serializers.CharField(source='kid.full_name', read_only=True)

    class Meta:
        model = MonthArchive
        fields = [
            'year', 'month', 'kid', 'missed_days', 'tarif', 'left_sum', 
            'missday_count', 'missday_cost', 'is_paid'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['missed_days'] = json.loads(instance.missed_days)  # Convert JSON string back to a list
        return representation


    def validate(self, data):
        # At the start of the month, ensure left_sum equals tarif
        if self.instance is None or not self.instance.pk:
            data['left_sum'] = data.get('tarif')
        return data

    def save(self, **kwargs):
        # Get the instance or create a new one
        instance = super().save(**kwargs)

        # Calculate missday_count based on missed_days
        instance.missday_count = len(json.loads(instance.missed_days))

        # Calculate left_sum if is_paid is still False
        if not instance.is_paid:
            instance.left_sum = instance.tarif - (instance.missday_count * instance.missday_cost)
        
        # Automatically mark as paid if left_sum is 0.0
        if instance.left_sum <= 0.0:
            instance.is_paid = True

        # Save the instance with the updated values
        instance.save()
        return instance


class StuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff
        fields = [
            'id', 'name', 'birthday', 'sex', 'phone_number', 'position', 'start_date', 'salary'
        ]


    

class StuffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff
        fields = [
            'id', 'name', 'birthday', 'sex', 'phone_number', 'position', 'start_date', 'salary'
        ]


class KidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth', 'sex'
        ]

class KidSerializer(serializers.ModelSerializer):
    month_archives = MonthArchiveSerializer(many=True, read_only=True)

    class Meta:
        model = Kid
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth', 'sex', 'month_archives'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    teacher = StuffSerializer()

    class Meta:
        model = Group
        fields = ['id', 'teacher', 'kids']


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'
