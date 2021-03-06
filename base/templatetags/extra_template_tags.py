from django import template
from django.contrib.auth.models import Group
from community.models import GameCategory

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


@register.inclusion_tag('base/categories.html')
def show_categories():
    categories = GameCategory.objects.all()
    return {'categories': categories}
