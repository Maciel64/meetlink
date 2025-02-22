# Generated by Django 5.1.3 on 2024-12-07 01:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetlink", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="call",
            options={"verbose_name": "Chamada", "verbose_name_plural": "Chamadas"},
        ),
        migrations.AlterModelOptions(
            name="subject",
            options={"verbose_name": "Assunto", "verbose_name_plural": "Assuntos"},
        ),
        migrations.AddField(
            model_name="call",
            name="interpreter_entered_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Hora de Entrada do Intérprete"
            ),
        ),
        migrations.AddField(
            model_name="call",
            name="manager_entered_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Hora de Entrada do Gestor"
            ),
        ),
        migrations.AlterField(
            model_name="call",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Hora Solicitação"
            ),
        ),
        migrations.AlterField(
            model_name="call",
            name="description",
            field=models.TextField(verbose_name="Descrição"),
        ),
        migrations.AlterField(
            model_name="call",
            name="responsible",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="calls",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Responsável",
            ),
        ),
        migrations.AlterField(
            model_name="call",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="meetlink.subject",
                verbose_name="Assunto",
            ),
        ),
        migrations.AlterField(
            model_name="call",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Hora Atualização"),
        ),
        migrations.AlterField(
            model_name="subject",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Descrição"),
        ),
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Nome"),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("SUPERADMIN", "Super Administrador"),
                    ("MANAGER", "Gestor"),
                    ("TOTEM", "Totem"),
                    ("INTERPRETER", "Intérprete"),
                ],
                default="MANAGER",
                max_length=20,
                verbose_name="Permissão",
            ),
        ),
    ]
