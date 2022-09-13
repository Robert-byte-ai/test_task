from django.core.validators import MinValueValidator
from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=200, null=True,
                                   blank=True, verbose_name='Описание')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ('name',)
        abstract = True


class Discount(BaseModel):
    count = models.PositiveIntegerField(verbose_name='Сумма скидки')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(BaseModel):
    count = models.PositiveIntegerField(verbose_name='Сумма налога')

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Item(BaseModel):
    currency_choice = (
        ('usd', 'usd'),
        ('rub', 'rub'),

    )
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(0)],
                                verbose_name='Цена')

    currency = models.CharField(choices=currency_choice, default='usd',
                                verbose_name='Валюта', max_length=5)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders',
                                   verbose_name='Товары', )

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='discounts', verbose_name='Скидка')

    tax = models.ManyToManyField(Tax, blank=True, related_name='taxes', verbose_name='Налог')

    payed = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-pk',)
