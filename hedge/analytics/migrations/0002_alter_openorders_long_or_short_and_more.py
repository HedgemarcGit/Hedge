# Generated by Django 4.2.16 on 2024-10-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openorders',
            name='long_or_short',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='openorders',
            name='risk_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='openorders',
            name='stop_loss',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='openorders',
            name='time_frame',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
