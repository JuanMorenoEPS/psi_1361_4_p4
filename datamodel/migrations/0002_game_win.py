# Generated by Django 2.2.5 on 2019-12-10 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='win',
            field=models.IntegerField(default=0),
        ),
    ]