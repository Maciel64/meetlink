# Generated by Django 5.1.3 on 2024-12-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetlink", "0003_alter_call_description_alter_call_responsible_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="call",
            name="finished_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Hora Finalização"
            ),
        ),
    ]
