# Generated by Django 3.0.5 on 2021-02-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MCQ', 'MCQ'), ('True_False', 'True_False')], default=1, max_length=10),
        ),
    ]