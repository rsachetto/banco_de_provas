from django.template import Library
import decimal
register = Library()

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter_function
def hash(h, key):
    return h[key]


@register.filter_function
def sub_comma_to_point(s):
    a = s
    if(type(s) == decimal.Decimal):
        a = str(s)
    return a.replace(',', '.')