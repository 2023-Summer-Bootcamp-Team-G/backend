# Generated by Django 4.2.3 on 2023-07-07 07:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("login_id", models.CharField(max_length=200, unique=True)),
                ("nick_name", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
