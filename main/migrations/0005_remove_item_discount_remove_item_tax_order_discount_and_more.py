# Generated by Django 4.1.1 on 2022-09-11 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_tax_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='item',
            name='tax',
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discounts', to='main.discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ManyToManyField(blank=True, related_name='taxes', to='main.tax', verbose_name='Налог'),
        ),
    ]