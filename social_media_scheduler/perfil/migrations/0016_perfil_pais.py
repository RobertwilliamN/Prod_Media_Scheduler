# Generated by Django 5.0.7 on 2024-09-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0015_alter_perfil_rede_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='pais',
            field=models.CharField(choices=[('Portugal', 'Portugal'), ('EUA', 'EUA'), ('Brazil', 'Brazil')], default='Brazil', max_length=50),
        ),
    ]
