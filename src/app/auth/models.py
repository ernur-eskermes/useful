from uuid import uuid4

from tortoise import models, fields


class Verification(models.Model):
    """Модель для подтверждения регистраций пользователя"""
    id = fields.IntField(pk=True)
    link = fields.UUIDField(default=uuid4)
    user = fields.ForeignKeyField("models.User", related_name="verifications")
