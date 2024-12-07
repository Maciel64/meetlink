# Generated by Django 5.1.3 on 2024-12-07 01:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetlink', '0002_alter_call_options_alter_subject_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='call',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calls', to=settings.AUTH_USER_MODEL, verbose_name='Responsável'),
        ),
        migrations.AlterField(
            model_name='call',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Hora Atualização'),
        ),
    ]
