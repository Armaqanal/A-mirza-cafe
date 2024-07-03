from .models import Order
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay


# *************************Total sales by year ****************************
def total_sales_by_year():
    sales_by_year = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(total_sales=Sum(
        'total_order_item_prices'
    )).order_by('year')
    return sales_by_year


# *************************Total sales by month and year *******************

def total_sales_by_month_year():
    sales_by_month_year = Order.objects.annotate(month=ExtractMonth('created_at'),
                                                 year=ExtractYear('created_at')).values('month', 'year').annotate(
        total_sales=Sum(

            'total_order_item_prices')).order_by('year', 'month')
    return sales_by_month_year


# *************************Total sales by month and year and day *******************
def total_sales_by_year_month_day():
    sales_by_month_year_day = Order.objects.annotate(month=ExtractMonth('created_at'),
                                                     year=ExtractYear('created_at'),
                                                     day=ExtractDay('created_at')).values('month', 'year',
                                                                                          'day').annotate(
        total_sales=Sum(

            'total_order_item_prices')).order_by('year', 'month', 'day')
    return sales_by_month_year_day


# ****************************The Top 1 year ***************************************
def top_year_based_on_sales():
    top_year = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(total_sales=Sum(
        'total_order_item_prices'
    )).order_by('-total_sales').first()
    if top_year:
        return f"year: {top_year['year']} sales: {top_year['total_sales']}"
    else:
        return None


# *****************************The Top 1 year month*********************************

def top_year_month_based_on_sales():
    top_year_month = Order.objects.annotate(month=ExtractMonth('created_at'),
                                            year=ExtractYear('created_at')).values('month', 'year').annotate(
        total_sales=Sum(

            'total_order_item_prices')).order_by('year', 'month').order_by('total_sales').first()
    if top_year_month:
        return f"year: {top_year_month['year']} month: {top_year_month['month']} sales: {top_year_month['total_sales']}"
    else:
        return None


# *****************************the top 1 year month day ******************************
def top_sales_by_year_month_day():
    top_month_year_day = Order.objects.annotate(month=ExtractMonth('created_at'),
                                                year=ExtractYear('created_at'),
                                                day=ExtractDay('created_at')).values('month', 'year',
                                                                                     'day').annotate(
        total_sales=Sum(

            'total_order_item_prices')).order_by('year', 'month', 'day').first()
    if top_month_year_day:
        return (
            f"year: {top_month_year_day['year']} month: {top_month_year_day['month']}  day: {top_month_year_day['day']} sales: {top_month_year_day['total_sales']}")
    else:
        return None
