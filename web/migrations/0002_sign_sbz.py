# Generated by Django 3.2.9 on 2021-12-15 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sign',
            name='sbz',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
