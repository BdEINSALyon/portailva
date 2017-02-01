from django import template

register = template.Library()


def is_achieved(obj, association_id):
    return obj.is_achieved(association_id)

register.filter('is_achieved', is_achieved)
