# Generated by Django 3.2.5 on 2022-12-05 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20221205_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='anatoa_zaka',
            field=models.CharField(choices=[('Anatoa Zaka', 'Anatoa Zaka'), ('Hatoi Zaka', 'Hatoi Zaka')], max_length=200),
        ),
    ]
