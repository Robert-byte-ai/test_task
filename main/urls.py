from django.urls import path

from . import views

urlpatterns = [
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('item/buy/<int:pk>/', views.ItemBuyView.as_view(), name='buy'),
    path('order/buy/<int:pk>/', views.OrderBuyView.as_view(), name='order'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
