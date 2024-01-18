# Generated by Django 4.2.6 on 2024-01-17 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmbientalBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=50)),
                ('document_name', models.CharField(max_length=50)),
                ('is_critical', models.BooleanField(default=False)),
                ('category', models.CharField(max_length=50)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AmbientalBookProps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive', models.FileField(upload_to='uploads/')),
                ('comment', models.TextField()),
                ('advance', models.CharField(choices=[('delivered', 'DELIVERED'), ('pending', 'PENDING'), ('na', 'NA')], default='pending', max_length=9)),
                ('essential_in_cloud', models.BooleanField(default=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosystem.ambientalbook')),
            ],
        ),
    ]
