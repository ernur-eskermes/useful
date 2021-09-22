from tortoise import models, fields

from src.app.user.models import User


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    parent: fields.ForeignKeyNullableRelation["Category"] = \
        fields.ForeignKeyField(
        "models.Category",
        related_name="children",
        null=True
    )
    children: fields.ReverseRelation["Category"]


class Toolkit(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    parent = fields.ForeignKeyField(
        "models.Toolkit",
        related_name="children",
        null=True
    )


class Project(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    create_date = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField("models.User", related_name="user_projects")
    toolkit: fields.ForeignKeyRelation[Toolkit] = fields.ForeignKeyField(
        "models.Toolkit",
        related_name="projects"
    )
    team: fields.ManyToManyRelation[User] = fields.ManyToManyField(
        "models.User",
        related_name="projects",
        through="team_project"
    )
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category",
        related_name="projects"
    )


class Task(models.Model):
    id = fields.IntField(pk=True)
    description = fields.TextField()
    create_date = fields.DatetimeField(auto_now_add=True)
    start_date = fields.DatetimeField(null=True)
    end_date = fields.DatetimeField(null=True)
    project = fields.ForeignKeyField("models.Project", related_name="tasks")
    worker = fields.ForeignKeyField(
        "models.User",
        related_name="tasks",
        null=True
    )


class CommentTask(models.Model):
    id = fields.IntField(pk=True)
    message = fields.CharField(max_length=100)
    create_date = fields.DatetimeField(auto_now_add=True)
    task = fields.ForeignKeyField("models.Task", related_name="tasks_comments")
    user = fields.ForeignKeyField("models.User", related_name="tasks_comments")
