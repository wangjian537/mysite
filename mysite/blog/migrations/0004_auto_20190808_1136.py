# Generated by Django 2.2.4 on 2019-08-08 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190804_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-create_time']},
        ),
    ]