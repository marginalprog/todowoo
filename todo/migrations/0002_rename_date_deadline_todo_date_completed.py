# Generated by Django 5.0 on 2024-03-02 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='date_deadline',
            new_name='date_completed',
        ),
    ]
