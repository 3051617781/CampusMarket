# Generated by Django 4.2.14 on 2024-08-06 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_report_userlikeuser_userlikepost_userlikecomment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="id",
            field=models.BigAutoField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
