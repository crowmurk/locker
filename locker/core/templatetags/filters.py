from django import template


register = template.Library()

@register.filter
def get_at_index0(obj, index):
    """Возвращает объект списка с определенным индексом.
    Индексация списка 0...n
    """
    try:
        return obj[index]
    except IndexError:
        return None

@register.filter
def get_at_index(obj, index):
    """Возвращает объект списка с определенным индексом.
    Индексация списка 1...n
    """
    try:
        return obj[index - 1]
    except IndexError:
        return None
