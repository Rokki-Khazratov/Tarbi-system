from django.db import models
import json

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

    def __str__(self):
        return self.full_name


class MonthArchive(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES.choices)
    kid = models.ForeignKey(Kid, related_name='month_archives', on_delete=models.CASCADE)

    missed_days = models.TextField()
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    left_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    missday_count = models.IntegerField(editable=False, default=0)
    missday_cost = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['kid', 'year', 'month'], name='unique_kid_month_year')
        ]

    def __str__(self):
        return f"{self.year}-{self.get_month_display()} for {self.kid.full_name}"

    def save(self, *args, **kwargs):
        self.missday_count = len(json.loads(self.missed_days))
        if not self.is_paid:
            self.left_sum = self.tarif - (self.missday_count * self.missday_cost)
        if self.left_sum <= 0.0:
            self.is_paid = True
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
