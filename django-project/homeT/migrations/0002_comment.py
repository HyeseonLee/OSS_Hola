# Generated by Django 2.2.3 on 2020-06-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeT', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
            ],
        ),
    ]
