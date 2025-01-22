from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.


class Role(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", "Super Administrador"
    MANAGER = "MANAGER", "Gestor"
    TOTEM = "TOTEM", "Totem"
    INTERPRETER = "INTERPRETER", "Intérprete"

    class Meta:
        verbose_name = "Permissão"
        verbose_name_plural = "Permissões"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
        verbose_name="Permissão",
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"


class Call(models.Model):
    responsible = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="responsible_calls",
        blank=True,
        null=True,
        verbose_name="Responsável",
    )
    interpreter = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="interpreter_calls",
        blank=True,
        null=True,
        verbose_name="Interprete",
    )
    subject = models.ForeignKey(
        "Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Assunto",
    )
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Hora Solicitação"
    )
    manager_entered_at = models.DateTimeField(
        verbose_name="Hora de Entrada do Gestor", blank=True, null=True
    )
    interpreter_entered_at = models.DateTimeField(
        verbose_name="Hora de Entrada do Intérprete", blank=True, null=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Hora Atualização", blank=True, null=True
    )
    finished_at = models.DateTimeField(
        verbose_name="Hora Finalização", blank=True, null=True
    )

    def __str__(self):
        return (
            f"Call by {self.responsible.username if self.responsible else None}"
            f" at {self.created_at}"
        )

    class Meta:
        verbose_name = "Chamada"
        verbose_name_plural = "Chamadas"
