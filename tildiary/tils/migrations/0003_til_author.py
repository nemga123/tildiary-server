# Generated by Django 4.1.7 on 2023-02-27 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tils", "0002_rename_subject_id_til_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="til",
            name="author",
            field=models.SmallIntegerField(default=1),
        ),
    ]
