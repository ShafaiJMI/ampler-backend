# Generated by Django 5.0.2 on 2025-01-15 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_purchase_options_alter_sell_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sell',
            options={'verbose_name_plural': 'sales'},
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='purchases',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='sales',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='core.invoice'),
        ),
        migrations.AlterField(
            model_name='sell',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='core.invoice'),
        ),
    ]
