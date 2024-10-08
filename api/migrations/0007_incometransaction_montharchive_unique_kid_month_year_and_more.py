# Generated by Django 5.0.2 on 2024-08-17 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_montharchive_left_sum_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('card', 'Card'), ('cash', 'Cash'), ('account', 'Account')], max_length=10)),
            ],
        ),
        migrations.AddConstraint(
            model_name='montharchive',
            constraint=models.UniqueConstraint(fields=('kid', 'year', 'month'), name='unique_kid_month_year'),
        ),
        migrations.AddField(
            model_name='incometransaction',
            name='kid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.kid'),
        ),
    ]
