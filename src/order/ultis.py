from .models import Order, OrderItem
from menu.models import MenuItem
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
import datetime

# *************************Total sales by year ****************************
def total_sales_by_year():
    sales_by_year = (
        Order.objects.annotate(year=ExtractYear("created_at"))
        .values("year")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("year")
    )
    return sales_by_year


# *************************Total sales by month and year *******************


def total_sales_by_month_year():
    sales_by_month_year = (
        Order.objects.annotate(
            month=ExtractMonth("created_at"), year=ExtractYear("created_at")
        )
        .values("month", "year")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("year", "month")
    )
    return sales_by_month_year


# *************************Total sales by month and year and day *******************
def total_sales_by_year_month_day():
    sales_by_month_year_day = (
        Order.objects.annotate(
            month=ExtractMonth("created_at"),
            year=ExtractYear("created_at"),
            day=ExtractDay("created_at"),
        )
        .values("month", "year", "day")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("year", "month", "day")
    )
    return sales_by_month_year_day


# ****************************The Top 1 year ***************************************
def top_year_based_on_sales():
    top_year = (
        Order.objects.annotate(year=ExtractYear("created_at"))
        .values("year")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("-total_sales")
        .first()
    )
    if top_year:
        return f"year: {top_year['year']} sales: {top_year['total_sales']}"
    else:
        return None


# *****************************The Top 1 year month*********************************


def top_year_month_based_on_sales():
    top_year_month = (
        Order.objects.annotate(
            month=ExtractMonth("created_at"), year=ExtractYear("created_at")
        )
        .values("month", "year")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("year", "month")
        .order_by("total_sales")
        .first()
    )
    if top_year_month:
        return f"year: {top_year_month['year']} month: {top_year_month['month']} sales: {top_year_month['total_sales']}"
    else:
        return None


# *****************************the top 1 year month day ******************************
def top_sales_by_year_month_day():
    top_month_year_day = (
        Order.objects.annotate(
            month=ExtractMonth("created_at"),
            year=ExtractYear("created_at"),
            day=ExtractDay("created_at"),
        )
        .values("month", "year", "day")
        .annotate(total_sales=Sum("total_order_item_prices"))
        .order_by("year", "month", "day")
        .first()
    )
    if top_month_year_day:
        return f"year: {top_month_year_day['year']} month: {top_month_year_day['month']}  day: {top_month_year_day['day']} sales: {top_month_year_day['total_sales']}"
    else:
        return None


def demography_items():
    items = MenuItem.objects.all()
    for i in items:
        item_data = {
            "name": i.food_name,
            "age": {
                "3_8": {"man": 0, "woman": 0},
                "9_12": {"man": 0, "woman": 0},
                "13_7": {"man": 0, "woman": 0},
                "18_26": {"man": 0, "woman": 0},
                "27_40": {"man": 0, "woman": 0},
                "41_60": {"man": 0, "woman": 0},
                "61_above": {"man": 0, "woman": 0},
            },
            "man": 0,
            "woman": 0,
            "balance": 0,
            "total": 0,
        }
        order_item = OrderItem.objects.filter(menu_item__id=i.pk)
        for f in order_item:
            item_data["total"] += f.quantity
            item_data["balance"] += (f.price * f.quantity) - f.total_discounted_price
            person = f.order.customer
            person_age = datetime.datetime.now().year - person.date_of_birth.year
            person_gender = person.gender
            if 3 <= person_age <= 8:
                item_data[person_gender] += 1
                item_data["age"]["3_8"][person_gender] += 1
            elif 9 <= person_age <= 12:
                item_data[person_gender] += 1
                item_data["age"]["9_12"][person_gender] += 1
            elif 13 <= person_age <= 17:
                item_data[person_gender] += 1
                item_data["age"]["13_7"][person_gender] += 1
            elif 18 <= person_age <= 26:
                item_data[person_gender] += 1
                item_data["age"]["18_26"][person_gender] += 1
            elif 27 <= person_age <= 40:
                item_data[person_gender] += 1
                item_data["age"]["27_40"][person_gender] += 1
            elif 41 <= person_age <= 60:
                item_data[person_gender] += 1
                item_data["age"]["41_60"][person_gender] += 1
            elif 60 < person_age:
                item_data[person_gender] += 1
                item_data["age"]["61_above"][person_gender] += 1
        yield item_data
