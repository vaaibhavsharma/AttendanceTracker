# Generated by Django 4.0.3 on 2022-09-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniWeb', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='data',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
