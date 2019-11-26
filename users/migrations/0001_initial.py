# Generated by Django 2.2.6 on 2019-11-25 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('users_image', models.CharField(max_length=50)),
                ('users_name', models.CharField(max_length=180)),
                ('users_no', models.CharField(max_length=180, primary_key=True, serialize=False)),
                ('users_password', models.CharField(max_length=180)),
                ('users_major', models.CharField(max_length=180)),
                ('users_isactive', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Users_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('disciplinary_offence', models.CharField(max_length=180)),
                ('book_leading', models.CharField(max_length=180)),
            ],
        ),
    ]
