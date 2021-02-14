from django import template

register = template.Library()


@register.filter
def get_friend_requests(reverse_friends):
    return reverse_friends.filter(validated=False).count()
