from rest_framework import serializers
from .models import *
from decimal import Decimal





class IncomeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTransaction
        fields = '__all__'

    def create(self, validated_data):
        transaction = super().create(validated_data)
        kid = transaction.kid
        kid.apply_payment_to_debt(transaction.amount)
        print(f"Транзакция создана для ребёнка: {kid.full_name}, сумма: {transaction.amount}")

        return transaction

class KidSerializer(serializers.ModelSerializer):
    month_archives = serializers.SerializerMethodField()

    class Meta:
        model = Kid
        fields = ['id', 'full_name', 'phone_number', 'date_of_birth', 'sex', 'balance', 'month_archives']

    def get_month_archives(self, obj):
        filter_is_paid = self.context.get('filter_is_paid', None)

        archives = obj.month_archives.all()

        if filter_is_paid is not None:
            if filter_is_paid.lower() == 'true':
                filter_is_paid = True
            elif filter_is_paid.lower() == 'false':
                filter_is_paid = False
            else:
                raise serializers.ValidationError("Invalid value for 'is_paid'. Must be 'true' or 'false'.")
            
            # Применяем фильтрацию
            archives = archives.filter(is_paid=filter_is_paid)

        return MonthArchiveSerializer(archives, many=True).data




class MonthArchiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    kid = serializers.PrimaryKeyRelatedField(queryset=Kid.objects.all())  # Ожидаем ID ребенка

    class Meta:
        model = MonthArchive
        fields = [
            'id', 'year', 'month', 'kid', 'missed_days', 'tarif', 'left_sum', 
            'missday_count', 'missday_cost', 'is_paid'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['missed_days'] = json.loads(instance.missed_days)  # Преобразуем JSON-строку в список
        return representation

    def create(self, validated_data):
        # Автоматически вычисляем значения при создании архива
        missed_days_list = json.loads(validated_data['missed_days'])  # Преобразуем JSON строку в список
        validated_data['missday_count'] = len(missed_days_list)
        validated_data['left_sum'] = validated_data['tarif'] - (validated_data['missday_count'] * validated_data['missday_cost'])

        # Если left_sum становится 0 или меньше, помечаем архив как оплаченный
        if validated_data['left_sum'] <= 0:
            validated_data['is_paid'] = True

        return super().create(validated_data)





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
            'id', 'full_name', 'phone_number', 'date_of_birth', 'sex','balance'
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
