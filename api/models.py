from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def __str__(self):
        return self.full_name

class MonthArchive(models.Model):
    year = models.IntegerField()
    month_name = models.IntegerField(choices=MONTH_CHOICES.choices)
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)

    missed_days = ArrayField(models.IntegerField())
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    left_sum = models.DecimalField(max_digits=10, decimal_places=2)

    missday_count = models.IntegerField(editable=False)
    missday_cost = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField()

    def __str__(self):
        return f"{self.year}-{self.get_month_name_display()} for {self.kid.full_name}"

    def save(self, *args, **kwargs):
        self.missday_count = len(self.missed_days)
        super().save(*args, **kwargs)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
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
