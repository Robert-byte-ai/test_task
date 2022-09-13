from django.http.response import JsonResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView
from django.conf import settings
import stripe

from .models import Item, Order


class ItemDetailView(DetailView):
    model = Item
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'object': self.object, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
        return context


class OrderDetailView(ItemDetailView):
    model = Order


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ItemBuyView(DetailView):
    model = Item
    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.object = self.get_object()
        domain_url = request.build_absolute_uri('/')
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': self.object.currency,
                    'product_data': {
                        'name': self.object.name,
                    },
                    'unit_amount': int(self.object.price * 100),
                },
                'quantity': 1,

            }],
            mode='payment',
            success_url='{}success/'.format(domain_url),
            cancel_url='{}cancel/'.format(domain_url),
        )
        return JsonResponse({'sessionId': session.id}, status=200)


class OrderBuyView(DetailView):
    model = Order
    template_name = 'checkout.html'

    def get(self, request, taxes=None, discount=None, *args, **kwargs):
        order = Order.objects.prefetch_related('items', 'tax').select_related('discount').get(id=self.kwargs['pk'])
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if order_tax := order.tax:
            taxes = [stripe.TaxRate.create(
                display_name=tax.name,
                description=tax.description,
                percentage=tax.count,
                inclusive=False,
            )['id'] for tax in order_tax.all()]
        if order_discount := order.discount:
            discount = stripe.Coupon.create(
                percent_off=order_discount.count,
            )['id']
        domain_url = request.build_absolute_uri('/')
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'tax_rates': taxes,
            'quantity': 1,
        } for item in order.items.all()]
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='{}success/'.format(domain_url),
            cancel_url='{}cancel/'.format(domain_url),
            discounts=[{'coupon': discount}],
        )
        return JsonResponse({'sessionId': session.id}, status=200)
