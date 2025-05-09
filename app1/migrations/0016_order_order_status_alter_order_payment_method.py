# Generated by Django 5.1.4 on 2025-04-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_order_mobile_order_ordered_by_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Khalti', 'Khalti')], default='Cash On Delivery', max_length=20),
        ),
    ]
