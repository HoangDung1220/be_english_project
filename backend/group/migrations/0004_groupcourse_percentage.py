# Generated by Django 4.2.1 on 2023-06-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0003_alter_group_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupcourse",
            name="percentage",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
