# Generated by Django 4.2.7 on 2025-02-26 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
