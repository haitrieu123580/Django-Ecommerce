from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView, View

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'home.html', context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)


def checkout(request):
    return render(request, 'checkout.html')


# adding/removing orderItem
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # find or create new order item belong to user's order
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # find the order exist
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was increase :>')
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart :>')
            return redirect("core:order-summary")
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart :>')
    return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # find the order exist
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This item was remove from your cart:>')
            return redirect("core:order-summary")
        else:
            messages.info(request, 'This item was not in your cart :>')
    else:
        messages.info(request, 'You do not have an active order :>')
    return redirect("core:product", slug=slug)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)

        except:
            messages.error(self.request, 'You do not have an active order')
            return redirect("/")

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # find the order exist
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity -= 1
            order_item.save()
            # order_item.delete()
            messages.info(request, 'This item quantity was updated:>')
            return redirect("core:order-summary")
        else:
            messages.info(request, 'This item was not in your cart :>')
    else:
        messages.info(request, 'You do not have an active order :>')
    return redirect("core:product", slug=slug)