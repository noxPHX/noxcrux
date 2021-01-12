from django import template

register = template.Library()


@register.filter
def is_password(form_field_obj):
    return form_field_obj.field.widget.__class__.__name__ == "PasswordInput"
