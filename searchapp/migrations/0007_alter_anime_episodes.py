# Generated by Django 5.0.2 on 2024-02-21 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchapp', '0006_alter_anime_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='episodes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
