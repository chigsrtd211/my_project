# Generated by Django 4.1.7 on 2023-04-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pg_main', '0004_pg_facility_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='pg_facility_new',
            name='attached_washroom',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
