from django import template

register = template.Library()


@register.filter
def inc(value, arg):
    return int(value) + int(arg)


@register.simple_tag
def division(a, b, to_int=False):
    res = int(a) / int(b)
    return int(res) if to_int else res
