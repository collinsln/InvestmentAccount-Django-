# Generated by Django 5.1.1 on 2024-09-09 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0003_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='No description', max_length=255),
            preserve_default=False,
        ),
    ]
