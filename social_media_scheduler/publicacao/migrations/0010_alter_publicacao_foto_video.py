# Generated by Django 5.0.7 on 2024-08-27 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicacao', '0009_remove_publicacao_perfil_publicacao_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacao',
            name='foto_video',
            field=models.FileField(blank=True, max_length=120, null=True, upload_to='uploads/'),
        ),
    ]
