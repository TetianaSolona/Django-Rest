# Generated by Django 4.1 on 2023-02-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_customuser_password1_customuser_password2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='password2',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
    ]