# Generated by Django 3.2.9 on 2021-12-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_remove_bookrecord_bno'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrecord',
            name='broomtype',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]