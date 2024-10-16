# Generated by Django 5.0.7 on 2024-10-15 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicacao', '0012_alter_publicacao_descricao_registropostagem'),
        ('publicacao_bau', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registropostagem',
            name='publicacao_bau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicacao_bau.publicacao_bau'),
        ),
        migrations.AlterUniqueTogether(
            name='registropostagem',
            unique_together={('publicacao_bau', 'perfil')},
        ),
    ]
