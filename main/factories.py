import factory
import random

from .models import Discount, Tax, Item, Order


class ItemFactory(factory.django.DjangoModelFactory):
    name = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )
    description = factory.Faker(
        'sentence',
        nb_words=15,
        variable_nb_words=True
    )
    price = factory.LazyAttribute(
        lambda a: random.randint(0, 10000)
    )

    class Meta:
        model = Item
        django_get_or_create = ('name',)


class TaxFactory(factory.django.DjangoModelFactory):
    name = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )
    description = factory.Faker(
        'sentence',
        nb_words=15,
        variable_nb_words=True
    )
    count = factory.LazyAttribute(
        lambda a: random.randint(0, 100)
    )

    class Meta:
        model = Tax
        django_get_or_create = ('name',)


class DiscountFactory(TaxFactory):
    class Meta:
        model = Discount


class OrderFactory(factory.django.DjangoModelFactory):
    discount = factory.SubFactory(DiscountFactory)

    class Meta:
        model = Order

    @factory.post_generation
    def tax(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tax in extracted:
                self.tax.add(tax)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for items in extracted:
                self.tax.add(items)
