from django import template

register = template.Library()


@register.filter('endswith')
def startswith(text, ends):
    if isinstance(text, str):
        return text.endswith(ends)
    return False
