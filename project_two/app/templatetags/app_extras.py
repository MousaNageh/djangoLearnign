from django import template

register = template.Library()


@register.filter
def addsomevalue(value):
    return int(value) + 100
