from django.core.management.base import BaseCommand

from main.factories import (
    ItemFactory,
    TaxFactory,
    DiscountFactory,
    OrderFactory
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(5):
            ItemFactory()
            TaxFactory()
            DiscountFactory()
            OrderFactory()
