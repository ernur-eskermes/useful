from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    date_join = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    avatar = fields.BinaryField(null=True)

    def __str__(self):
        return self.username


class SocialAccount(models.Model):
    id = fields.IntField(pk=True)
    account_id = fields.IntField()
    account_url = fields.CharField(max_length=255)
    account_login = fields.CharField(max_length=255)
    account_name = fields.CharField(max_length=255)
    provider = fields.CharField(max_length=255)
    user = fields.ForeignKeyField(
        "models.User",
        related_name='social_accounts'
    )

    def __str__(self):
        return self.account_login
