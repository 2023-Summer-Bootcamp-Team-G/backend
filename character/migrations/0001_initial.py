# Generated by Django 4.2.3 on 2023-07-09 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0001_initial"),
        ("question", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submit",
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
                ("result_url", models.CharField(max_length=200, null=True)),
                ("nick_name", models.CharField(max_length=200, null=True)),
                (
                    "poll_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="question.poll"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Answer",
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
                ("num", models.IntegerField()),
                ("content", models.CharField(max_length=200, null=True)),
                (
                    "question_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="question.question",
                    ),
                ),
                (
                    "submit_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="character.submit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
