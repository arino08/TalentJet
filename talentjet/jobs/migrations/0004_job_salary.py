# Generated by Django 4.2.7 on 2025-03-01 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.CharField(blank=True, help_text='E.g., $50K-$70K or Competitive', max_length=100),
        ),
    ]
