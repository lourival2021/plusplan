# Generated by Django 5.0.1 on 2024-03-16 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_rename_usuario_empresa_empresa_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa'),
        ),
    ]
