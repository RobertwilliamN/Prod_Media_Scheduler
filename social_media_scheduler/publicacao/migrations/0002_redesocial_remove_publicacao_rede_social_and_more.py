# Generated by Django 5.0.7 on 2024-08-07 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedeSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='publicacao',
            name='rede_social',
        ),
        migrations.AddField(
            model_name='publicacao',
            name='rede_social',
            field=models.ManyToManyField(to='publicacao.redesocial'),
        ),
    ]
