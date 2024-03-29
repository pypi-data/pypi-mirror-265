# Generated by Django 3.2.20 on 2023-11-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall_e_models', '0010_embedavatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpoint',
            name='avatar_url',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='userpoint',
            name='avatar_url_message_id',
            field=models.PositiveBigIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='userpoint',
            name='leveling_message_avatar_url',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='userpoint',
            name='name',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userpoint',
            name='nickname',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
