from django.template.defaulttags import register


@register.filter
def get_tuple(list, key):
    return [item for item in list if item[0] == key][0][1]
