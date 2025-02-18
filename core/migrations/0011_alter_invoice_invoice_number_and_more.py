# Generated by Django 5.0.2 on 2025-01-30 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_total_amount_purchase_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='metal_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sell',
            name='metal_type',
            field=models.CharField(max_length=20),
        ),
    ]
