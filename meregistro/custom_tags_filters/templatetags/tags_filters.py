from django import template

register = template.Library()

@register.filter(name = 'implode')
def implode(lst, sep = ' - '):
    return str(sep).join("%s" % (v) for v in lst)

"""
Tag que devuelve un atributo class con el texto pasado
"""
@register.tag(name = 'css_classes')
def css_classes(parser, token):
    try:
        tag_name, classes = token.split_contents()
    except ValueError:
        raise Exception(1)
    return CssClassesNode(classes)

class CssClassesNode(template.Node):
    def __init__(self, classes):
        self.classes = classes
    def render(self, context):
        if len(self.classes) == 0:
            return ''
        return ' class=' + str(self.classes) + ''
