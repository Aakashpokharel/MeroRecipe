# Generated by Django 4.2.3 on 2023-07-22 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_is_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_user',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
