# Generated by Django 4.1.7 on 2023-02-27 09:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tils", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="til",
            old_name="subject_id",
            new_name="subject",
        ),
    ]
