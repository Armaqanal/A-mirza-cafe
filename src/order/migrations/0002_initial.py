# Generated by Django 5.0.6 on 2024-06-24 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0002_alter_menuitem_discount'),
        ('order', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='menu.menuitem'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order'),
        ),
    ]
