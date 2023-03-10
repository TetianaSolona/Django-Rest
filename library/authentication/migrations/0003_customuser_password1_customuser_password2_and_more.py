# Generated by Django 4.1 on 2023-02-13 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='password1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='password2',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
