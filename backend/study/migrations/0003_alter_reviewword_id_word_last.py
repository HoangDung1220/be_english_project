# Generated by Django 4.2.1 on 2023-07-04 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0004_course_number_user_learned"),
        ("study", "0002_reviewword"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewword",
            name="id_word_last",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="course.vocabulary",
            ),
        ),
    ]