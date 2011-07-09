from django import template

register = template.Library()

@register.filter(name='implode')
def implode(lst, sep = ' - '):
    return str(sep).join("%s" % (v) for v in lst)

