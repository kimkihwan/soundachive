# Generated by Django 2.1.7 on 2019-03-18 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20190317_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='post_id_list',
            field=models.TextField(blank=True),
        ),
    ]
