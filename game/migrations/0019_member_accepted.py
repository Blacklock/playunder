# Generated by Django 2.1 on 2018-08-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20180815_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='accepted',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
