# Generated by Django 5.0.6 on 2024-07-01 01:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecosystem', '0008_remove_ambientalbooksharepointpath_text_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambientalbooksharepointpath',
            name='category',
            field=models.CharField(choices=[('criticisms', 'CRITICAS'), ('air_noise', 'AIRE Y RUIDO'), ('water', 'AGUA'), ('waste', 'RESIDUOS'), ('recnat_and_risk', 'RECNAT Y RIESGO'), ('others', 'OTROS')], max_length=15),
        ),
        migrations.CreateModel(
            name='BookSharepointComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosystem.ambientalbooksharepointpath')),
            ],
        ),
    ]
