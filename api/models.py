from django.db import models

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

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    kids = models.ManyToManyField(Kid)

class Journal(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    month = models.DateField()
    schedule = models.JSONField()
    missday_cost = models.IntegerField()
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    total_sum = models.IntegerField()

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"
