# Generated by Django 4.1.7 on 2023-02-23 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("subjects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Til",
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
                ("title", models.CharField(max_length=10)),
                ("content", models.TextField()),
                ("is_opened", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "subject_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tils",
                        to="subjects.subject",
                    ),
                ),
            ],
        ),
    ]