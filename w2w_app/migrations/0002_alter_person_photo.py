# Generated by Django 4.2.4 on 2023-08-10 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w2w_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(default='default_person.jpeg', upload_to='person'),
        ),
    ]