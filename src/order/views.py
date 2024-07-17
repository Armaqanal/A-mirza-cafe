from typing import Any
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from menu.models import MenuItem
from accounts.models import Customer
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.list import ListView
from .forms import EditOrderItemForm, AddOrderItemForm, AddOrderForm, TotalSalesFilter
from .models import Order, OrderItem
from .ultis import (
    total_sales_by_year_month_day,
    total_sales_by_year,
    top_year_based_on_sales,
    total_sales_by_month_year,
    top_year_month_based_on_sales,
    top_sales_by_year_month_day,
    demography_items,
)
import csv


# def cart(request):
#     username = request.COOKIES.get("username")
#     customer = get_object_or_404(Customer, username=username)
#     unpaid_order = Order.get_unpaid_order(customer_id=customer.id)
#     unpaid_order_items = unpaid_order.order_items.all()
#     context = {"unpaid_order_items": unpaid_order_items}
#     return render(request, "order/cart.html", context)

class CartView(TemplateView):
    template_name = "order/cart.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.username = self.request.session.get("username")
        if self.username:
            self.customer = get_object_or_404(Customer, username=self.username)
            self.unpaid_order = Order.get_unpaid_order(customer_id=self.customer.id)
            self.unpaid_order_item = self.unpaid_order.order_items.all()
            return super(CartView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unpaid_order_items"] = self.unpaid_order_item
        return context


# def order(request):
#     print(request.COOKIES.get("username"))
#     return render(request, "order/order.html", {})

class OrderView(TemplateView):
    template_name = "order/order.html"


def add_menu_item_to_cart(request, selected_category=None, menu_item_id=None):
    username = request.COOKIES.get("username")
    customer = get_object_or_404(Customer, username=username)
    # page not found cases are:
    # 1. the username is for a staff instead of a customer!
    # 2. the cookie is expired

    selected_menu_item = MenuItem.objects.get(id=menu_item_id)
    print(selected_menu_item)
    unpaid_order = Order.get_unpaid_order(customer_id=customer.id)

    # check if this item has been already selected for the 'unpaid_order',
    # if it exits get it and if it doesn't create it
    order_item = OrderItem.objects.filter(order=unpaid_order).get_or_create(
        menu_item=selected_menu_item, order=unpaid_order, quantity=1
    )
    return redirect("menu", selected_category)


class ManageOrderView(PermissionRequiredMixin, ListView):
    permission_required = 'order.view_order'
    template_name = "order/manage_orders.html"
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.select_related("customer").filter(is_paid=True).order_by("-id")


class OrderCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'order.add_order'
    template_name = 'order/order_form.html'
    model = Order
    form_class = AddOrderForm
    success_url = reverse_lazy('manage-orders')


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'order.change_order'
    model = Order
    template_name = 'order/order_form.html'
    form_class = AddOrderForm

    def get_success_url(self):
        return reverse_lazy('manage-orders')

    def form_valid(self, form):
        order = self.get_object()
        cleaned_data = form.cleaned_data
        order.customer = cleaned_data['customer']
        order.save(update_fields=['customer'])
        return super().form_valid(form)


class DeleteOrderView(PermissionRequiredMixin, DeleteView):
    permission_required = 'order.delete_order'
    model = Order
    success_url = reverse_lazy('manage-orders')


class ManageOrderItemsListView(PermissionRequiredMixin, ListView):
    permission_required = 'order.view_orderitem'
    template_name = 'order/manage_order_items.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        queryset = OrderItem.objects.select_related('menu_item').filter(order=order_id).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        context['order_id'] = order_id
        return context


class OrderItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'order.add_orderitem'
    template_name = 'order/order_item_form.html'
    model = OrderItem
    form_class = AddOrderItemForm

    def get_initial(self):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        return {'order': order, 'quantity': 1}

    def get_success_url(self):
        return reverse_lazy("manage-order-items", kwargs={'order_id': self.kwargs.get('order_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs.get('order_id')
        return context


class EditOrderItemView(PermissionRequiredMixin, UpdateView):
    permission_required = 'order.change_orderitem'
    template_name = 'order/order_item_form.html'
    model = OrderItem
    form_class = EditOrderItemForm

    def get_success_url(self):
        return reverse_lazy("manage-order-items", kwargs={'order_id': self.kwargs.get('order_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs.get('order_id')
        context['order_item_id'] = self.kwargs.get('pk')
        return context


class DeleteOrderItemView(PermissionRequiredMixin, DeleteView):
    permission_required = 'order.delete_orderitem'
    model = OrderItem

    def get_success_url(self):
        return reverse_lazy("manage-order-items", kwargs={'order_id': self.kwargs.get('order_id')})


@staff_member_required
def total_sales_by_date(request):
    sales_by_year = None
    sales_by_month_year = None
    sales_by_month_year_day = None
    best_year = None
    best_year_month = None
    best_year_month_day = None
    if request.method == 'POST':
        form = TotalSalesFilter(request.POST)
        if form.is_valid():
            filter_type = form.cleaned_data["time_choice"]
            if filter_type == "year":
                sales_by_year = total_sales_by_year()
                best_year = top_year_based_on_sales()
            elif filter_type == "year|month":
                sales_by_month_year = total_sales_by_month_year()
                best_year_month = top_year_month_based_on_sales()
            elif filter_type == "year|month|day":
                sales_by_month_year_day = total_sales_by_year_month_day()
                best_year_month_day = top_sales_by_year_month_day()
    else:
        form = TotalSalesFilter()
    return render(
        request,
        "order/dashboard.html",
        {
            "form": form,
            "sales_by_year": sales_by_year,
            "sales_by_month_year": sales_by_month_year,
            "sales_by_month_year_day": sales_by_month_year_day,
            "best_year": best_year,
            "best_year_month": best_year_month,
            "best_year_month_day": best_year_month_day,
            "data_items": list(demography_items()),
        },
    )
    return render(request, 'order/dashboard.html', {
        'form': form,
        'sales_by_year': sales_by_year,
        'sales_by_month_year': sales_by_month_year,
        'sales_by_month_year_day': sales_by_month_year_day,
        'best_year': best_year,
        'best_year_month': best_year_month,
        'best_year_month_day': best_year_month_day
    })


@staff_member_required
def total_sales_by_year_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="sales_by_year.csv"'},
    )

    writer = csv.writer(response)
    sales_report_by_year = total_sales_by_year()

    writer.writerow(["year", "total_sales"])
    for row in sales_report_by_year:
        writer.writerow([row["year"], row["total_sales"]])

    return response


@staff_member_required
def total_sales_by_month_year_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="sales_by_month_year.csv"'
        },
    )

    writer = csv.writer(response)
    sales_report_by_year_month = total_sales_by_month_year()

    writer.writerow(["year", "month", "total_sales"])
    for row in sales_report_by_year_month:
        writer.writerow([row["year"], row["month"], row["total_sales"]])

    return response


@staff_member_required
def total_sales_by_year_month_day_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="sales_by_year_month_day.csv"'
        },
    )

    writer = csv.writer(response)
    sales_report_by_year_month_day = total_sales_by_year_month_day()

    writer.writerow(["year", "month", "day", "total_sales"])
    for row in sales_report_by_year_month_day:
        writer.writerow([row["year"], row["month"], row["day"], row["total_sales"]])

    return response
