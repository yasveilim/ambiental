# Generated by Django 5.0.1 on 2024-02-14 03:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecosystem', '0003_remove_restorepasswordrequest_password'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbientalBookMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='ambientalbookprops',
            name='user',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ambientalbookprops',
            name='comment',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='ambientalbook',
            name='material',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='ecosystem.ambientalbookmaterial'),
        ),
    ]
