# Generated by Django 5.0.7 on 2024-08-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0010_alter_perfil_app_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='app_secret',
            field=models.CharField(default='fd5e6fdd6ceb1ec9aa891db08fadb2ac', max_length=255),
        ),
    ]
