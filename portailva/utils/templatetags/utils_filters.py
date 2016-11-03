from django.template.defaulttags import register


@register.filter
def get_tuple(items, key):
    return [item for item in items if item[0] == key][0][1]
