# Generated by Django 3.0.6 on 2020-05-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank='null', upload_to='')),
            ],
        ),
    ]
