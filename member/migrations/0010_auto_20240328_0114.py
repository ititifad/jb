# Generated by Django 3.2.5 on 2024-03-27 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_zaka'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ameajiriwa',
            field=models.CharField(choices=[('Ameajiriwa', 'Ameajiriwa'), ('Amejiajiri', 'Amejiajiri'), ('Hana Kazi', 'Hana Kazi')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='ameoa_ameolewa',
            field=models.CharField(choices=[('Ameoa', 'Ameoa'), ('Ameolewa', 'Ameolewa'), ('Hajaolewa', 'Hajaolewa'), ('Hajaoa', 'Hajaoa')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='anatoa_zaka',
            field=models.CharField(choices=[('Anatoa Zaka', 'Anatoa Zaka'), ('Hatoi Zaka', 'Hatoi Zaka')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='huduma_aliyonayo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='jinsia',
            field=models.CharField(choices=[('Kiume', 'Kiume'), ('Kike', 'Kike')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='mahali_anakotoka',
            field=models.CharField(help_text='mahali alikompokea yesu', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='mahali_kuzaliwa',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='mahali_ubatizo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='maji_mengi',
            field=models.CharField(choices=[('Maji Mengi', 'Maji Mengi'), ('Maji Kidogo', 'Maji Kidogo')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='namba_ya_zaka',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='simu',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
