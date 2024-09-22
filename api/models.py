from django.db import models
import json
from django.db import transaction

class MONTH_CHOICES(models.IntegerChoices):
    JANUARY = 1, 'January'
    FEBRUARY = 2, 'February'
    MARCH = 3, 'March'
    APRIL = 4, 'April'
    MAY = 5, 'May'
    JUNE = 6, 'June'
    JULY = 7, 'July'
    AUGUST = 8, 'August'
    SEPTEMBER = 9, 'September'
    OCTOBER = 10, 'October'
    NOVEMBER = 11, 'November'
    DECEMBER = 12, 'December'

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('boss', 'Boss'),
        ('teacher', 'Teacher'),
    ]
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



class Kid(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
    ]
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=2, choices=GENDER_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.full_name
    
    

    def apply_payment_to_debt(self, amount):
        with transaction.atomic():  # Включаем атомарную транзакцию
            print(f"Начальный баланс: {self.balance}")
            remaining_amount = amount + self.balance

            if remaining_amount > 0:
                unpaid_archives = self.month_archives.filter(is_paid=False).order_by('year', 'month')

                if unpaid_archives.exists():
                    print(f"Найдены неоплаченные архивы: {len(unpaid_archives)}")
                else:
                    print("Не найдены неоплаченные архивы")
                    self.balance = remaining_amount
                    self.save()
                    return

                for archive in unpaid_archives:
                    print(f"Remaining_amount перед итерацией: {remaining_amount}")
                    print(f"Обрабатываем архив: {archive.year}-{archive.get_month_display()}, текущий долг: {archive.left_sum}")

                    if remaining_amount >= archive.left_sum:
                        remaining_amount -= archive.left_sum
                        archive.left_sum = 0
                        archive.is_paid = True
                        archive.save(update_fields=['left_sum', 'is_paid'])
                        print(f"Архив {archive.year}-{archive.get_month_display()} полностью оплачен, остаток денег: {remaining_amount}")
                    else:
                        new = archive.left_sum - remaining_amount
                        remaining_amount = 0
                        if new > 0:  # Сравниваем с 'new', а не с 'archive.left_sum'
                            print("in if",f"new_sum = {new}")
                            archive.is_paid = False
                            archive.left_sum = new
                        else:
                            archive.is_paid = True  # Если остаток стал 0 или меньше, то помечаем как оплаченный

                        archive.save()  # Сохраняем изменения в архиве

                    print(f"Частично погашаем: {archive.year}-{archive.get_month_display()}, остаток: {archive.left_sum}, is_paid после сохранения: {archive.is_paid}")
                    return

                self.balance = remaining_amount
                self.save(update_fields=['balance'])
            else:
                self.balance = 0
                self.save(update_fields=['balance'])

            print(f"Финальный баланс: {self.balance}, осталось денег после оплаты: {remaining_amount}")




    










class MonthArchive(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES.choices)
    kid = models.ForeignKey(Kid, related_name='month_archives', on_delete=models.CASCADE)

    missed_days = models.TextField()
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    left_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    missday_count = models.IntegerField(editable=False, default=0)
    missday_cost = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['kid', 'year', 'month'], name='unique_kid_month_year')
        ]

    def __str__(self):
        return f"{self.year}-{self.get_month_display()} for {self.kid.full_name}"

    def save(self, *args, **kwargs):
        # Пересчитываем количество пропущенных дней
        self.missday_count = len(json.loads(self.missed_days))

        # Если не оплачено, пересчитываем left_sum
        if not self.is_paid:
            self.left_sum = self.tarif - (self.missday_count * self.missday_cost)

            # Если left_sum меньше или равно 0, считаем долг полностью погашенным
            if self.left_sum <= 0:
                self.is_paid = True
                self.left_sum = 0

        # Вызываем стандартный метод save() для сохранения в базе данных
        super().save(*args, **kwargs)

    def apply_payment(self, amount):
        if amount <= 0:
            raise ValueError("Сумма платежа должна быть положительной")

        # Уменьшаем долг
        self.left_sum -= amount
        
        # Проверка на отрицательный остаток и установка в 0, если долг полностью погашен
        if self.left_sum <= 0:
            self.is_paid = True
            self.left_sum = 0

        # Применяем оплату и сохраняем изменения без пересчета left_sum
        self.save(skip_calculation=True)





class IncomeTransaction(models.Model):
    kid = models.ForeignKey(Kid, related_name='income_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    TYPE_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('account', 'Account'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)









        
    
class Stuff(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    POSITION_CHOICES = [
        ('boss', 'Boss'),
        ('administrator', 'Administrator'),
        ('teacher', 'Teacher'),
        ('assistant', 'Assistant'),
        ('coder', 'Coder'),
        ('cleaner', 'Cleaner'),
        ('cook', 'Cook'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    birthday = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    password = models.CharField(max_length=128)  # Storing hashed password
    start_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name



class Group(models.Model):
    teacher = models.ForeignKey(Stuff, limit_choices_to={'position': 'teacher'}, on_delete=models.CASCADE)
    kids = models.ManyToManyField(Kid)

    def __str__(self):
        return f"{self.teacher.name}'s Group"

class Journal(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    month = models.DateField()
    missday_cost = models.IntegerField()
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    total_sum = models.IntegerField()

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"
