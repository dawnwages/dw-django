from django import template
from home.models import ProjectIcons

register = template.Library()


@register.inclusion_tag("includes/icons-footer.html", takes_context=True)
def projecticons(context):
    return {
        "projecticons": ProjectIcons.objects.all()
    }