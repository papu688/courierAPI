# Generated by Django 5.1.1 on 2024-09-11 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parcel',
            old_name='reciever_name',
            new_name='receiver_name',
        ),
    ]
