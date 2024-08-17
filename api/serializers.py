from rest_framework import serializers
from .models import *
from decimal import Decimal





class IncomeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTransaction
        fields = '__all__'


    

    def create(self, validated_data):
        print("Начало создания транзакции")
        transaction = super().create(validated_data)
        
        kid = transaction.kid
        print(f"Транзакция создана для ребёнка: {kid.full_name}, сумма: {transaction.amount}")

        # Получаем архив месяца, который еще не оплачен (самый старый)
        current_month_archive = kid.month_archives.filter(is_paid=False).order_by('year', 'month').first()
        print(f"Найден архив для обновления: {current_month_archive}")

        if current_month_archive:
            print(f"Текущий архив перед вычитанием: {current_month_archive.year}-{current_month_archive.get_month_display()}, left_sum: {current_month_archive.left_sum}")

            # Вычитаем сумму транзакции из left_sum
            current_month_archive.left_sum -= transaction.amount

            print(f"Обновленное значение left_sum: {current_month_archive.left_sum}")

            # Если сумма left_sum становится <= 0, помечаем как оплаченное и устанавливаем left_sum в 0
            if current_month_archive.left_sum <= 0:
                current_month_archive.is_paid = True
                current_month_archive.left_sum = 0
                print("Архив помечен как оплачен")

            # Сохраняем изменения в архиве
            current_month_archive.save()
            print(f"Архив сохранен: left_sum = {current_month_archive.left_sum}, is_paid = {current_month_archive.is_paid}")
        else:
            print("Не найден неоплаченный архив")

        return transaction



class MonthArchiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    month = serializers.CharField(source='get_month_display', read_only=True)
    kid = serializers.CharField(source='kid.full_name', read_only=True)

    class Meta:
        model = MonthArchive
        fields = [
            'id', 'year', 'month', 'kid', 'missed_days', 'tarif', 'left_sum', 
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
        instance = super().save(**kwargs)

        # Calculate missday_count based on missed_days
        instance.missday_count = len(json.loads(instance.missed_days))

        # Check if 'left_sum' is provided in the initial data
        if 'left_sum' in self.initial_data:
            # Respect the manually provided left_sum
            instance.left_sum = Decimal(self.initial_data['left_sum'])
        else:
            # Recalculate left_sum only if not manually provided
            if not instance.is_paid:
                instance.left_sum = instance.tarif - (instance.missday_count * instance.missday_cost)

        # Automatically mark as paid if left_sum is 0.0 or less
        if instance.left_sum <= 0.0:
            instance.is_paid = True

        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Calculate missday_count based on missed_days
        instance.missday_count = len(json.loads(instance.missed_days))

        # Check if 'left_sum' is provided in the initial data
        if 'left_sum' in self.initial_data:
            # Respect the manually provided left_sum
            instance.left_sum = Decimal(self.initial_data['left_sum'])
        else:
            # Recalculate left_sum only if not manually provided
            if not instance.is_paid:
                instance.left_sum = instance.tarif - (instance.missday_count * instance.missday_cost)

        # Automatically set is_paid to true if left_sum is 0 or less
        if instance.left_sum <= 0.0:
            instance.is_paid = True

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
