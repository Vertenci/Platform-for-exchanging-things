# Generated by Django 5.2 on 2025-04-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ad_condition_alter_exchangeproposal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='is_draft',
            field=models.BooleanField(default=True, verbose_name='Черновик'),
        ),
    ]
